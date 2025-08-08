# Lab 03d-use-local-mcp-server-tools

## Learning Objective
By the end of this lab, you will:
- Understand how to run a local MCP (Model Context Protocol) server.
- Test your Python environment and IDE setup using a simple client.
- Interact with the MCP server using a full-featured client as per the lab instructions.



## Files in This Lab
### **server.py**
- Implements an MCP server using `FastMCP`.
- Tools:
  - `get_inventory_levels()`: Returns current inventory.
  - `get_weekly_sales()`: Returns weekly sales.
  - `add(a, b)`: Adds two integers.
- Resource:
  - `greeting(name)`: Returns a greeting message.

### **simple_client.py**
- Starts the MCP server automatically.
- Lists available tools.
- Calls the `add` tool with sample inputs (5 + 7).
- Purpose: **Verify your IDE and virtual environment setup before running the full lab.**

### **client.py**
- Connects to the MCP server and retrieves available tools.
- Wraps MCP tools as **FunctionTool** objects for Azure AI Foundry.
- Creates an **Azure AI Foundry Agent** using:
  - `AgentsClient` from `azure.ai.agents`.
  - Model deployment and endpoint from environment variables.
- Agent instructions:
  - Recommend **restock** if inventory < 10 and weekly sales > 15.
  - Recommend **clearance** if inventory > 20 and weekly sales < 5.
- Enables **auto function calling** so the agent can invoke MCP tools dynamically.
- Provides an interactive chat loop:
  - You enter prompts like:  
    ```
    Which products need restocking?
    ```
  - The agent decides which MCP tools to call, retrieves data, and responds intelligently.

---

