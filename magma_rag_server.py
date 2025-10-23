from fastmcp import FastMCP
from typing import Dict, Any
import json
from magma_toolchain_wrapper import run_rag_toolchain, get_magma_configuration

mcp = FastMCP("magma-rag-server")

@mcp.tool(
    name="run_rag",
    description="Run Magma RAG toolchain. Input: query (str). Uses dev environment and rag_toolchain config internally."
)
def run_rag(query: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    try:
        result = run_rag_toolchain(query=query, config=config)
        return result
    except Exception as e:
        return {"error": str(e)}

@mcp.tool(
    name="get_config",
    description="Get a Magma configuration. Input: api_path (str). Uses dev environment internally."
)
def get_config(api_path: str) -> Dict[str, Any]:
    try:
        result = get_magma_configuration(api_path=api_path)
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)
