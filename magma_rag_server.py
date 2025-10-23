from fastmcp import FastMCP
from typing import Dict, Any
import json
from magma_toolchain_wrapper import run_rag_toolchain

mcp = FastMCP("magma-rag-server")

@mcp.tool(
    name="run_rag",
    description="Search IBM MaaS360 documentation to answer ANY user question about device management, enrollment, certificates, policies, troubleshooting, configuration, or any other MaaS360 topic. Always use this tool when users ask MaaS360-related questions. Pass the user's complete question as the 'query' parameter."
)
def run_rag(
    query: str,
    config_id: str = "rag_toolchain",
    config: Dict[str, Any] = None,
    env: str = None,
) -> Dict[str, Any]:
    """
    Answer user questions by searching IBM MaaS360 documentation.
    Always uses env='dev' internally to avoid WatsonX sending invalid env.
    """
    try:
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

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)
