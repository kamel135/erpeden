import frappe
import openai

from raven.ai.handler import get_variables_for_instructions


@frappe.whitelist()
def get_instruction_preview(instruction):
    """
    Function to get the rendered instructions for the bot
    """
    frappe.has_permission(doctype="Raven Bot", ptype="write", throw=True)

    instructions = frappe.render_template(instruction, get_variables_for_instructions())
    return instructions


@frappe.whitelist()
def get_saved_prompts(bot: str = None):
    """
    API to get the saved prompt for a user/bot/global
    """
    or_filters = [["is_global", "=", 1], ["owner", "=", frappe.session.user]]

    prompts = frappe.get_list(
        "Raven Bot AI Prompt", or_filters=or_filters, fields=["name", "prompt", "is_global", "raven_bot"]
    )

    # Order by ones with the given bot
    prompts = sorted(prompts, key=lambda x: x.get("raven_bot") == bot, reverse=True)

    return prompts


@frappe.whitelist()
def get_open_ai_version():
    """
    API to get the version of the OpenAI Python client
    """
    frappe.has_permission(doctype="Raven Bot", ptype="read", throw=True)
    return openai.__version__


@frappe.whitelist()
def get_openai_available_models():
    """
    API to get the available OpenAI models for assistants
    """
    frappe.has_permission(doctype="Raven Bot", ptype="read", throw=True)
    from raven.ai.openai_client import get_openai_models

    models = get_openai_models()

    valid_prefixes = ["gpt-4", "gpt-3.5", "o1", "o3-mini"]

    # Model should not contain these words
    invalid_models = ["realtime", "transcribe", "search", "audio"]

    compatible_models = []

    for model in models:
        if any(model.id.startswith(prefix) for prefix in valid_prefixes):
            if not any(word in model.id for word in invalid_models):
                compatible_models.append(model.id)

    return compatible_models


@frappe.whitelist()
def test_llm_configuration(
    provider: str = "OpenAI",
    api_url: str = None,
    api_key: str = None,
    endpoint: str = None,
    api_version: str = None,
    deployment_name: str = None
):
    """
    Test LLM configuration (OpenAI, Azure AI, Local LLM)
    """
    frappe.has_permission(doctype="Raven Settings", ptype="write", throw=True)

    try:
        if provider == "Local LLM" and api_url:
            # Test local LLM endpoint
            import requests
            response = requests.get(f"{api_url}/models", timeout=5)
            if response.status_code == 200:
                models = response.json()
                return {
                    "success": True,
                    "message": f"Successfully connected to {api_url}",
                    "models": models.get("data", []),
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to connect to {api_url}. Status: {response.status_code}",
                }

        elif provider == "Azure AI":
            #  Log values received from UI
            frappe.log_error(
                "Azure Debug",
                f"api_key={api_key}\nendpoint={endpoint}\napi_version={api_version}\ndeployment={deployment_name}"
            )

            from openai import AzureOpenAI
            if not all([api_key, endpoint, deployment_name, api_version]):
                return {"success": False, "message": "Azure settings missing"}

            client = AzureOpenAI(
                api_key=api_key,
                azure_endpoint=endpoint.rstrip("/"),
                api_version=api_version
            )

            try:
                # اختبار فعلي باستخدام الـ deployment name
                resp = client.chat.completions.create(
                    model=deployment_name,
                    messages=[{"role": "user", "content": "ping"}],
                    max_tokens=5
                )
                return {
                    "success": True,
                    "message": "Successfully connected to Azure AI",
                    "models": [deployment_name]
                }
            except Exception as e:
                # نطبع الرسالة زي ما هي عشان نعرف السبب
                return {"success": False, "message": f"Azure connection failed: {e}"}

        elif provider == "OpenAI":
            from raven.ai.openai_client import get_open_ai_client
            client = get_open_ai_client()
            models = client.models.list()
            return {
                "success": True,
                "message": "Successfully connected to OpenAI",
                "models": [{"id": m.id} for m in models.data[:5]],
            }

    except Exception as e:
        return {"success": False, "message": f"Connection failed: {str(e)}"}
