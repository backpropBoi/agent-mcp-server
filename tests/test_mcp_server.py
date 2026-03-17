rom app.main import top_mcp, register_tools,register_proxy
from fastmcp import Client
import pytest

@pytest.fixture
def get_mcp_server():
    register_tools(top_mcp)
    register_proxy(top_mcp)
    return top_mcp

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool_name, params, expected",
    [
        ("add", {"a": 3, "b": 5}, "8"),
        ("multiply", {"a": 3, "b": 5}, "15"),
    ]
)

async def test_mcp_tool_functionality(get_mcp_server, tool_name, params, expected):
    # Pass the server directly to the Client constructor
    server = get_mcp_server
    async with Client(server) as client:
        tools = await client.list_tools() 
        result = await client.call_tool(tool_name, params)
        assert result[0].text == expected