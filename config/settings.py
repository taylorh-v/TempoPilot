import os
from dataclasses import dataclass


@dataclass
class Settings:
    azure_tenant_id: str = ""
    azure_client_id: str = ""
    azure_client_secret: str = ""
    graph_scope: str = "https://graph.microsoft.com/.default"
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment_name: str = ""
    azure_openai_api_version: str = "2024-02-01"
    app_env: str = "development"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            azure_tenant_id=os.getenv("AZURE_TENANT_ID", ""),
            azure_client_id=os.getenv("AZURE_CLIENT_ID", ""),
            azure_client_secret=os.getenv("AZURE_CLIENT_SECRET", ""),
            graph_scope=os.getenv("GRAPH_SCOPE", "https://graph.microsoft.com/.default"),
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            azure_openai_deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""),
            azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            app_env=os.getenv("APP_ENV", "development"),
        )

    def graph_is_configured(self) -> bool:
        return bool(self.azure_tenant_id and self.azure_client_id and self.azure_client_secret)

    def openai_is_configured(self) -> bool:
        return bool(self.azure_openai_endpoint and self.azure_openai_api_key and self.azure_openai_deployment_name)


settings = Settings.from_env()
