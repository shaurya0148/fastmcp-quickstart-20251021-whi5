from typing import Any, Dict
import json
from utils.MagmaUtility import execute_toolchain, configuration_request

def run_rag_toolchain(query: str, config_id: str = None,
                      config: Dict[str, Any] = None, env: str = None,
                      verbose: bool = False) -> Dict[str, Any]:
    env = "dev"
    config_id = "rag_toolchain"

    payload = {"query": query}
    result = execute_toolchain(
        env=env,
        toolchain="rag",
        input=payload,
        config_id=config_id,
        config=(config or {}),
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
