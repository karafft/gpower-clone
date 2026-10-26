"""Real MCP stdio adapter. Engine text is identical to CLI JSON text."""
import asyncio
# Load numerical runtime before starting asynchronous stdio transport.
from scipy.stats import t as _t, nct as _nct
from scipy.optimize import brentq as _brentq
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from .engine import analyze, serialize, AnalysisError

SCHEMA = {"type": "object", "properties": {
    "test": {"type": "string"}, "mode": {"type": "string"},
    **{k: {"type": "integer"} for k in ("tails", "n1", "n2")},
    **{k: {"type": "number"} for k in ("d", "alpha", "power", "ratio", "beta_alpha_ratio")},
}, "required": ["test", "mode"], "additionalProperties": False}
DESCRIPTION = "SPEC-based independent two-sample t power calculation. All fields required by the selected mode must be explicit. No defaults."
server = Server("gpower-clone")

def calculate_text(arguments):
    try:
        return serialize(analyze(arguments)), False
    except AnalysisError as exc:
        return serialize(exc.as_dict()), True
    except Exception:
        return serialize({"error": "Internal numerical or runtime error", "code": "INTERNAL_ERROR", "field": None}), True

@server.list_tools()
async def list_tools():
    return [Tool(name="power_analysis", description=DESCRIPTION, inputSchema=SCHEMA)]

@server.call_tool(validate_input=False)
async def call_tool(name, arguments):
    from mcp.types import CallToolResult
    if name != "power_analysis":
        return CallToolResult(content=[TextContent(type="text", text=serialize({"error":"Unsupported tool", "code":"UNSUPPORTED", "field":"tool"}))], isError=True)
    text, error = calculate_text(arguments)
    return CallToolResult(content=[TextContent(type="text", text=text)], isError=error)

async def run():
    async with stdio_server() as (read, write):
        await server.run(read, write, InitializationOptions(server_name="gpower-clone", server_version="1.1.0rc4", capabilities=server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={})))

def main():
    asyncio.run(run())

if __name__ == "__main__": main()
