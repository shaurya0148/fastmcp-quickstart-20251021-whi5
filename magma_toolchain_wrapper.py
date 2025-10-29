from typing import Any, Dict
import json
from utils.MagmaUtility import execute_toolchain, configuration_request

def run_rag_toolchain(query: str, config_id: str = None,
                      config: Dict[str, Any] = None, env: str = None,
                      verbose: bool = False) -> Dict[str, Any]:
    env = "dev"
    config_id = "rag_toolchain"
    
    default_config = {
        "output_field_mapping": {
            "keys": ["generated_answer", "context"]
        },
        "retriever": {
            "dense": {
                "collections": [
                    {
                        "collection_name": "mmas_360_docs",
                        "filters": [{"filter_type": "product_names", "items": ["MaaS360", "IBM MaaS360"]}]
                    },
                ]
            }
        },
        "render_prompt": {
            "context_prompt_template": {
                "value": "Source: {url}\nDocument: {page_content}",
                "input_variables": {
                    "page_content": "page_content",
                    "url": "metadata.source"
                }
            },
            "prompt_template": {
                "value": "some prompt here that references {context} and {query}",
                "input_variables": ["context", "query"]
            }
        }
    }

    payload = {"query": query}
    result = execute_toolchain(
        env=env,
        toolchain="rag",
        input=payload,
        config_id=config_id,
        config=(config or default_config),
        verbose=verbose,
    )
    if isinstance(result, str):
        try:
            return json.loads(result)
        except Exception:
            return {"raw": result}
    return result

def get_magma_configuration(env: str = None, api_path: str = None) -> Dict[str, Any]:
    env = "dev"
    result = configuration_request(env=env, verb="GET", api_path=api_path or "", payload={})
    if isinstance(result, str):
        try:
            return json.loads(result)
        except Exception:
            return {"raw": result}
    return result
