from fastmcp import FastMCP
from typing import Dict, Any
import json
from magma_toolchain_wrapper import run_rag_toolchain, get_magma_configuration

mcp = FastMCP("magma-rag-server")

@mcp.tool(
    name="run_rag",
    description="Run Magma RAG toolchain. Inputs: query (str), config_id (str, optional), config (dict, optional)."
)
def run_rag(
    query: str,
    config_id: str = "rag_toolchain",
    config: Dict[str, Any] = None,
    env: str = None,
) -> Dict[str, Any]:
    """
    Always uses env='dev' internally to avoid WatsonX sending invalid env.
    """
    try:
        # Force env to 'dev' regardless of WatsonX input
        result = run_rag_toolchain(
            query=query,
            config_id=config_id,
            config=config,
            env="dev",
            verbose=False
        )
        return result
    except Exception as e:
        return {"error": str(e)}

@mcp.tool(
    name="get_config",
    description="Get a Magma configuration. Input: api_path (str). Always uses env='dev'."
)
def get_config(api_path: str, env: str = None) -> Dict[str, Any]:
    """
    Force env='dev' to prevent WatsonX from sending invalid environment values.
    Accepts an optional env parameter from the caller to avoid validation errors.
    """
    try:
        result = get_magma_configuration(env="dev", api_path=api_path)
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)
