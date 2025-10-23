from typing import Any, Dict
import json
from utils.MagmaUtility import execute_toolchain, configuration_request

def run_rag_toolchain(query: str, config_id: str = None,
                      config: Dict[str, Any] = None, env: str = None,
                      verbose: bool = False) -> Dict[str, Any]:
    env = "dev"
    config_id = "rag_toolchain"
    
    # Default config with your collections
    default_config = {
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
