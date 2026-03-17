from fastmcp import FastMCP
import importlib
import pkgutil
from pathlib import Path
import json
import logging
logging.basicConfig(level=logging.INFO)

top_mcp = FastMCP(name = "MCP server proxy", on_duplicate_tools="error")

def load_tools(package):
    package_name = package
    package = importlib.import_module(package_name)
    mcps = {}
    for _, name, _ in pkgutil.iter_modules(package.__path_):
        full_name = f"{package_name}.{name}"
        module = importlib.import_module(full_name)
        if hasattr(module, 'mcp'):
            obj = getattr(module, 'mcp')
            logging.info(f"Found object 'mcp' in module '{name}': {obj}")
            mcps[name] = obj
        else:
            logging.error(f"Can't find FAST MCP app 'mcp' in module '{name}'")
    return mcps

def register_tools(mcp_server):
    if _package_:
        tool_module = 'app.tools'
    else:
        tool_module = 'tools'
    mcp_apps = load_tools(tool_module)
    for name, app in mcp_apps.items():
        mcp_server.mount(app)

def register_proxy(mcp_server):
    root_path = Path(_file_).absolute().parent
    with open(f"{root_path}/mcp_servers.json", 'r', encoding='utf-8') as file:
        config = json.load(file)
        if config:
            proxy_server = FastMCP.as_proxy(config, name="remote")
            mcp_server.mount(proxy_server)


register_tools(top_mcp)
register_proxy(top_mcp)


if _name_ == "_main_":
    top_mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)