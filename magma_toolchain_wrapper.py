from typing import Any, Dict
import json
from utils.MagmaUtility import execute_toolchain, configuration_request

def run_rag_toolchain(query: str, config_id: str = "rag_toolchain",
                      config: Dict[str, Any] = None, env: str = "dev",
                      verbose: bool = False) -> Dict[str, Any]:
    payload = {"query": query}
    try:
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
    except Exception as e:
        # fallback to dev environment if production fails
        if env != "dev":
            try:
                fallback_result = execute_toolchain(
                    env="dev",
                    toolchain="rag",
                    input=payload,
                    config_id=config_id,
                    config=(config or {}),
                    verbose=verbose,
                )
                if isinstance(fallback_result, str):
                    try:
                        return json.loads(fallback_result)
                    except Exception:
                        return {"raw": fallback_result, "note": f"original error: {str(e)}"}
                return {"note": f"original error: {str(e)}", **fallback_result}
            except Exception as dev_e:
                return {"error": f"run_rag_toolchain failed on production: {str(e)}, dev fallback also failed: {str(dev_e)}"}
        return {"error": str(e)}

def get_magma_configuration(env: str, api_path: str) -> Dict[str, Any]:
    try:
        result = configuration_request(env=env, verb="GET", api_path=api_path, payload={})
        if isinstance(result, str):
            try:
                return json.loads(result)
            except Exception:
                return {"raw": result}
        return result
    except Exception as e:
        # fallback to dev if production fails
        if env != "dev":
            try:
                fallback_result = configuration_request(env="dev", verb="GET", api_path=api_path, payload={})
                if isinstance(fallback_result, str):
                    try:
                        return json.loads(fallback_result)
                    except Exception:
                        return {"raw": fallback_result, "note": f"original error: {str(e)}"}
                return {"note": f"original error: {str(e)}", **fallback_result}
            except Exception as dev_e:
                return {"error": f"get_magma_configuration failed on production: {str(e)}, dev fallback also failed: {str(dev_e)}"}
        return {"error": str(e)}
