import os, time
import asyncio
import json
import sys
from pathlib import Path
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from contextlib import AsyncExitStack

# Add references
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, MessageRole, ListSortOrder

from common.auth.credential_loader import AzureEnvLoader

# Clear the console
os.system('cls' if os.name=='nt' else 'clear')

# Load environment variables from .env file
loader = AzureEnvLoader()
project_endpoint= loader.get_variable("AGENT_AZURE_PROJECT_ENDPOINT")
model_deployment = loader.get_variable("AGENT_AZURE_MODEL_DEPLOYMENT_NAME")


async def connect_to_server(exit_stack: AsyncExitStack):
    print("Starting MCP server...")

    # Ensure we point to the server sitting next to this client
    server_path = Path(__file__).with_name("server.py")
    if not server_path.exists():
        raise FileNotFoundError(f"Server script not found: {server_path}")

    # Use the SAME interpreter as the client (your venv's python)
    # Also force unbuffered mode so stdio flushes immediately
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-u", str(server_path)],
        env={**os.environ, "PYTHONUNBUFFERED": "1"}
    )

    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport

    print("Transport established. Reading raw server output...")
    try:
        # Read a few lines from the server to see what it's sending
        for _ in range(5):
            line = await stdio.readline()
            print(f"SERVER OUTPUT: {line}")
    except Exception as e:
        print(f"Error reading from server: {e}")

    print("Creating ClientSession...")
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))
    print("Initializing session...")
    await session.initialize()
    print("Session initialized.")
    return session


async def chat_loop(session):

    # Connect to the agents client
    agents_client = AgentsClient(
        endpoint=project_endpoint,
        credential=loader.get_env_azure_credentials("APP1")
    )    

    # List tools available on the server
    response = await session.list_tools()
    tools = response.tools    

    # Build a function for each tool
    def make_tool_func(tool_name):
        async def tool_func(**kwargs):
            result = await session.call_tool(tool_name, kwargs)
            return result
            
        tool_func.__name__ = tool_name
        return tool_func

    functions_dict = {tool.name: make_tool_func(tool.name) for tool in tools}
    mcp_function_tool = FunctionTool(functions=list(functions_dict.values()))    

    # Create the agent
    agent = agents_client.create_agent(
        model=model_deployment,
        name="inventory-agent",
        instructions="""
        You are an inventory assistant. Here are some general guidelines:
        - Recommend restock if item inventory < 10  and weekly sales > 15
        - Recommend clearance if item inventory > 20 and weekly sales < 5
        """,
        tools=mcp_function_tool.definitions
    )    

    # Enable auto function calling
    agents_client.enable_auto_function_calls(tools=mcp_function_tool)    

    # Create a thread for the chat session
    thread = agents_client.threads.create()    

    while True:
        user_input = input("Enter a prompt for the inventory agent. Use 'quit' to exit.\nUSER: ").strip()
        if user_input.lower() == "quit":
            print("Exiting chat.")
            break

        # Invoke the prompt
        message = agents_client.messages.create(
            thread_id=thread.id,
            role=MessageRole.USER,
            content=user_input,
        )
        run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)

        # Monitor the run status
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
            tool_outputs = []

            if run.status == "requires_action":

                tool_calls = run.required_action.submit_tool_outputs.tool_calls

                for tool_call in tool_calls:

                    # Retrieve the matching function tool
                    function_name = tool_call.function.name
                    args_json = tool_call.function.arguments
                    kwargs = json.loads(args_json)
                    required_function = functions_dict.get(function_name)

                    # Invoke the function
                    output = await required_function(**kwargs)                    

                    # Append the output text
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output.content[0].text,
                    })                    
                
                # Submit the tool call output
                agents_client.runs.submit_tool_outputs(thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs)

        # Check for failure
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        # Display the response
        messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        for message in messages:
            if message.text_messages:
                last_msg = message.text_messages[-1]
                print(f"{message.role}:\n{last_msg.text.value}\n")        

    # Delete the agent when done
    print("Cleaning up agents:")
    agents_client.delete_agent(agent.id)
    print("Deleted inventory agent.")


async def main():
    import sys
    exit_stack = AsyncExitStack()
    try:
        session = await connect_to_server(exit_stack)
        await chat_loop(session)
    finally:
        await exit_stack.aclose()

if __name__ == "__main__":
    os.environ["MCP_LOG_LEVEL"] = "DEBUG"
    asyncio.run(main())
