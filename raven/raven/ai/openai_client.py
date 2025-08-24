import frappe
from frappe import _
from openai import OpenAI
from openai import AzureOpenAI

def get_open_ai_client():
	"""
	Get the OpenAI client
	"""

	raven_settings = frappe.get_cached_doc("Raven Settings")

	if not raven_settings.enable_ai_integration:
		frappe.throw(_("AI Integration is not enabled"))

	openai_api_key = raven_settings.get_password("openai_api_key")
	openai_organisation_id = (raven_settings.openai_organisation_id or "").strip()
	openai_project_id = (raven_settings.openai_project_id or "").strip()

	client_args = {"api_key": openai_api_key.strip(), "organization": openai_organisation_id}
	if openai_project_id:
		client_args["project"] = openai_project_id

	return OpenAI(**client_args)


def get_azure_openai_client():
    """Get Azure OpenAI client"""
    settings = frappe.get_cached_doc("Raven Settings")

    key = settings.get_password("azure_api_key")
    endpoint = (settings.azure_endpoint or "").rstrip("/")
    version = (settings.azure_api_version or "2024-12-01-preview").strip()
    deployment = (settings.azure_deployment_name or "").strip()

    if not all([key, endpoint, version, deployment]):
        frappe.throw("Azure AI settings are incomplete")

    client = AzureOpenAI(
        api_key=key,
        azure_endpoint=endpoint,
        api_version=version
    )
    return client

def get_openai_models():
	"""
	Get the available OpenAI models
	"""
	client = get_open_ai_client()
	return client.models.list()


def get_azure_openai_models():
	"""
	Get the available Azure OpenAI models
	"""
	client = get_azure_openai_client()
	return client.models.list()


code_interpreter_file_types = [
	"pdf",
	"csv",
	"docx",
	"doc",
	"xlsx",
	"pptx",
	"txt",
	"png",
	"jpg",
	"jpeg",
	"md",
	"json",
	"html",
]

file_search_file_types = ["pdf", "doc", "docx", "json", "txt", "md", "html", "pptx"]
