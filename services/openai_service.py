from __future__ import annotations

from openai import AzureOpenAI

from config.settings import settings


def get_openai_client():
    if not settings.openai_is_configured():
        raise ValueError("Azure OpenAI environment settings are missing or incomplete.")

    return AzureOpenAI(
        azure_endpoint=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        api_version=settings.azure_openai_api_version,
    )


def generate_risk_summary(project_name: str, signals: dict, risk_score: int) -> str:
    client = get_openai_client()

    response = client.responses.create(
        model=settings.azure_openai_deployment_name,
        input=[
            {
                "role": "system",
                "content": "You are a project risk analyst. Summarize why a project is at risk based on evidence and suggest practical actions.",
            },
            {
                "role": "user",
                "content": (
                    f"Project name: {project_name}\n"
                    f"Risk score: {risk_score}\n"
                    f"Signals: {signals}"
                ),
            },
        ],
    )

    return response.output_text.strip()
