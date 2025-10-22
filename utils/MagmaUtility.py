import requests
import json
from datetime import datetime

magma_subdomain_dict = {
    "dev": "ct-watsonx-dev.15l8cdl6hzlf",
    "int": "ct-watsonx-int.16hmpwlba9hn",
    "stg": "ct-watsonx-stg.16htok1ckcqz",
}

# ENTER YOUR AUTHORIZATION TOKEN HERE!
# in the format of 'Basic <BASE64-STRING>'
# echo -n "<CLIENT-ID>:<SECRET>" | base64

magma_auth = "Basic MWExMmEwZDItYmNiMC00MTVjLTk5M2YtNGRjMzM5ODFkMjdlOk5tVTBOamcyTTJZdE1XRm1ZeTAwTm1KaUxXRmtPV1l0TkRZell6QTJNelkyTURRMw=="
headers = {"Content-Type": "application/json", "Authorization": magma_auth}


def execute_toolchain(
    env,
    toolchain,
    input,
    config_id,
    config={},
    verbose=False,
):
    base_url = (
        f"https://{magma_subdomain_dict[env]}.us-south.codeengine.appdomain.cloud"
    )
    full_url = f"{base_url}/api/v2/toolchains/{toolchain}/execute"

    if verbose:
        full_url += "?verbose=true"

    timeStr = datetime.now().isoformat()[:19].replace("-", "").replace(":", "")
    payload = {
        "client_metadata": {
            "application_name": "magma_test",
            "case_number": "api_test_" + timeStr,
        },
        "config_id": config_id,
        "config": config,
        "input": input,
    }

    try:
        print(f"Calling Magma with the following URL:\n {full_url}\n")
        print("and the following payload:\n")
        print(json.dumps(payload, indent=2), "\n\n")

        response = requests.post(full_url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()
    except Exception as ex:
        return "Error encountered: " + str(ex.response.text)


def configuration_request(env, verb, api_path, payload):
    base_url = (
        f"https://{magma_subdomain_dict[env]}.us-south.codeengine.appdomain.cloud"
    )
    full_url = f"{base_url}/api/v2/{api_path}"

    try:
        print(f"Calling Magma with the following URL:\n {verb}  {full_url}\n")

        if payload:
            print("and the following payload:\n")
            print(json.dumps(payload, indent=2), "\n\n")

        response = requests.request(
            verb,
            headers=headers,
            url=full_url,
            json=payload,
        )

        response.raise_for_status()

        return response.json()
    except Exception as ex:
        return "Error encountered: " + str(ex.response.text)
