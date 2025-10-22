"""
FastMCP server exposing Magma RAG notebook as tools
"""

from fastmcp import FastMCP
from typing import Dict, Any
import json
from utils.MagmaUtility import execute_toolchain, configuration_request

mcp=FastMCP("Magma RAG Server")

@mcp.tool(
    name="run_rag",
    description="Tool to interact with Magma RAG notebook, input: query (str)",
)

def run_rag(query: str) -> Dict[str, Any]:
    """Executes your Magma RAG toolchain and returns JSON output"""
    try:
        input_payload = {"query": query}
        config_id = 'rag_toolchain'
        config = {
            "output_field_mapping": {
                "keys": ["generated_answer", "context"]
            },
            "retriever": {
                "dense": {
                    "collections": [
                        {
                            "collection_name": "ibm_docs_slate",
                            "filters": [{"filter_type": "digital_content_codes", "items": ["SS8H2S"]}]
                        },
                        {
                            "collection_name": "marketing_docs_slate",
                            "filters": [{"filter_type": "ut_30", "items": ["30BIB"]}]
                        }
                    ]
                }
            }
        }
        result = execute_toolchain(
            env='dev',
            toolchain='rag',
            input=input_payload,
            config_id=config_id,
            config=config,
            verbose=False
        )
        if isinstance(result, str):
            try:
                return json.loads(result)
            except Exception:
                return {"raw": result}
        return result
    except Exception as e:
        return {"error": str(e)}