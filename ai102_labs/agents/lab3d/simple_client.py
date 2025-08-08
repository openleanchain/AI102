import asyncio, os, sys
from pathlib import Path
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

async def main():
    # Ensure we point to the server sitting next to this client
    server_path = Path(__file__).with_name("server.py")
    if not server_path.exists():
        raise FileNotFoundError(f"Server script not found: {server_path}")

    # Use the SAME interpreter as the client (your venv's python)
    # Also force unbuffered mode so stdio flushes immediately
    params = StdioServerParameters(
        command=sys.executable,
        args=["-u", str(server_path)],
        env={**os.environ, "PYTHONUNBUFFERED": "1"}
    )

    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Tools:", [t.name for t in tools.tools])

            result = await session.call_tool("add", {"a": 5, "b": 7})
            print("add(5, 7) ->", result.content)

if __name__ == "__main__":
    asyncio.run(main())
