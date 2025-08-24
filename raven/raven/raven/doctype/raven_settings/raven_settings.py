# Copyright (c) 2023, The Commit Company and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class RavenSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from raven.raven_integrations.doctype.raven_hr_company_workspace.raven_hr_company_workspace import (
			RavenHRCompanyWorkspace,
		)

		auto_add_system_users: DF.Check
		auto_create_department_channel: DF.Check
		company_workspace_mapping: DF.Table[RavenHRCompanyWorkspace]
		config: DF.SmallText | None
		department_channel_type: DF.Literal["Public", "Private"]
		enable_ai_integration: DF.Check
		enable_google_apis: DF.Check
		enable_local_llm: DF.Check
		enable_openai_services: DF.Check
		enable_video_calling_via_livekit: DF.Check
		google_processor_location: DF.Literal["us", "eu"]
		google_project_id: DF.Data | None
		google_service_account_json_key: DF.Password | None
		livekit_api_key: DF.Data | None
		livekit_api_secret: DF.Password | None
		livekit_url: DF.Data | None
		local_llm_api_url: DF.Data | None
		local_llm_provider: DF.Literal["LM Studio", "Ollama", "LocalAI"]
		oauth_client: DF.Link | None
		openai_api_key: DF.Password | None
		openai_organisation_id: DF.Data | None
		openai_project_id: DF.Data | None
		push_notification_api_key: DF.Data | None
		push_notification_api_secret: DF.Password | None
		push_notification_server_url: DF.Data | None
		push_notification_service: DF.Literal["Frappe Cloud", "Raven"]
		show_if_a_user_is_on_leave: DF.Check
		show_raven_on_desk: DF.Check
		tenor_api_key: DF.Data | None
		vapid_public_key: DF.Data | None
                # Azure fields
		enable_azure_ai: DF.Check
		azure_api_key: DF.Password | None
		azure_endpoint: DF.Data | None
		azure_api_version: DF.Data | None
		azure_deployment_name: DF.Data | None

	# end: auto-generated types

	def validate(self):
		if self.auto_create_department_channel:
			if not self.company_workspace_mapping:
				frappe.throw(_("Please map the companies to the workspace before enabling this feature."))

			for row in self.company_workspace_mapping:
				# Check if the company exists since it's a Data field
				if not frappe.db.exists("Company", row.company):
					frappe.throw(f"Company {row.company} does not exist.")

		if self.push_notification_service == "Raven":
			if not self.push_notification_server_url:
				frappe.throw(_("Please enter the Push Notification Server URL"))
			if not self.push_notification_api_key:
				frappe.throw(_("Please enter the Push Notification API Key"))
			if not self.push_notification_api_secret:
				frappe.throw(_("Please enter the Push Notification API Secret"))
		if self.openai_organisation_id:
			self.openai_organisation_id = self.openai_organisation_id.strip()

		if self.openai_project_id:
			self.openai_project_id = self.openai_project_id.strip()

		if self.enable_google_apis:
			if not self.google_project_id:
				frappe.throw(_("Please enter the Google Project ID"))
			if not self.google_service_account_json_key:
				frappe.throw(_("Please add the Google Service Account JSON Key"))
			if not self.google_processor_location:
				frappe.throw(_("Please select the Google Processor Location"))


		if self.enable_azure_ai:
			if not self.azure_api_key:
				frappe.throw(_("Please enter the Azure API Key"))
			if not self.azure_endpoint:
				frappe.throw(_("Please enter the Azure Endpoint"))
			if not self.azure_api_version:
				frappe.throw(_("Please enter the Azure API Version"))
			if not self.azure_deployment_name:
				frappe.throw(_("Please enter the Azure Deployment Name"))
