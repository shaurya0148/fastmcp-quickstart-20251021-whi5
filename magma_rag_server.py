from fastmcp import FastMCP
from typing import Dict, Any
from magma_toolchain_wrapper import run_rag_toolchain, get_magma_configuration

mcp = FastMCP("Magma RAG Server")

@mcp.tool(
    name="run_rag",
    description="Run Magma RAG toolchain. Inputs: query (str), config_id (str, optional), config (object, optional), env (str, optional).",
)
def run_rag(query: str, config_id: str = "rag_toolchain", config: Dict[str, Any] = None, env: str = "dev") -> Dict[str, Any]:
    try:
        return run_rag_toolchain(query=query, config_id=config_id, config=config, env=env)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool(
    name="get_config",
    description="Get a Magma configuration. Inputs: env (str), api_path (str)",
)
def get_config(env: str, api_path: str) -> Dict[str, Any]:
    try:
        return get_magma_configuration(env=env, api_path=api_path)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8080)
