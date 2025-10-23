from typing import Any, Dict
import json
from utils.MagmaUtility import execute_toolchain, configuration_request

def run_rag_toolchain(query: str, config_id: str = "rag_toolchain",
                      config: Dict[str, Any] = None, env: str = "dev",
                      verbose: bool = False) -> Dict[str, Any]:
    payload = {"query": query}
    result = execute_toolchain(
        env=env,  # always dev
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

def get_magma_configuration(env: str, api_path: str) -> Dict[str, Any]:
    result = configuration_request(env=env, verb="GET", api_path=api_path, payload={})
    if isinstance(result, str):
        try:
            return json.loads(result)
        except Exception:
            return {"raw": result}
    return result
