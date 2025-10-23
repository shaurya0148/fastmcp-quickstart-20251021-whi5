from typing import Any, Dict
import json
from utils.MagmaUtility import execute_toolchain, configuration_request

def run_rag_toolchain(query: str,
                      config_id: str = "rag_toolchain",
                      config: Dict[str, Any] = None,
                      env: str = "dev",
                      verbose: bool = False) -> Dict[str, Any]:
    """
    Executes the Magma RAG toolchain for a given query.
    """
    payload = {"query": query}
    try:
        result = execute_toolchain(
            env=env,
            toolchain="rag",
            input=payload,
            config_id=config_id,
            config=config or {},
            verbose=verbose,
        )

        if isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"raw_result": result}

        return result or {"message": "Empty response from toolchain"}

    except Exception as e:
        return {"error": f"run_rag_toolchain failed: {str(e)}"}


def get_magma_configuration(env: str, api_path: str) -> Dict[str, Any]:
    """
    Fetches configuration details from Magma backend.
    """
    try:
        result = configuration_request(
            env=env,
            verb="GET",
            api_path=api_path,
            payload={}
        )

        if isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                return {"raw_result": result}

        return result or {"message": "Empty configuration response"}

    except Exception as e:
        return {"error": f"get_magma_configuration failed: {str(e)}"}
