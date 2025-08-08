import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.identity import EnvironmentCredential

class AzureEnvLoader:
    def __init__(self, env_path=".env"):
        # Initialize the loader with a specific .env file path
        self.env_path = env_path
        self.load_env()

    def load_env(self):
        # Load environment variables from the specified .env file
        load_dotenv(self.env_path)

    def resolve(self, key):
        """
        Resolve the value of a configuration key based on its mode.
        Supports per-variable mode using prefixes:
        - 'env:' means use the value directly from the .env file
        - 'system:' means treat the value as a reference to a system environment variable
        If no prefix is found, the raw value is returned as-is.
        """
        raw_value = os.getenv(key)
        if not raw_value:
            raise ValueError(f"Missing config value for {key}")

        if raw_value.startswith("env:"):
            return raw_value[4:]
        elif raw_value.startswith("system:"):
            system_key = raw_value[7:]
            resolved = os.environ.get(system_key)
            if not resolved:
                raise ValueError(f"System environment variable '{system_key}' (from {key}) is not set")
            return resolved
        else:
            return raw_value  # fallback to raw value

    def get_variable(self, key):
        # Public method to resolve and return any specific variable
        return self.resolve(key)

    def get_credentials(self, prefix=None):
        """
        Retrieve Azure credentials using optional prefix.
        If a prefix is provided, keys are prefixed accordingly (e.g., 'FOUNDRY_AZURE_CLIENT_ID').
        """
        tenant_id = self.resolve(f"{prefix}_AZURE_TENANT_ID" if prefix else "AZURE_TENANT_ID")
        client_id = self.resolve(f"{prefix}_AZURE_CLIENT_ID" if prefix else "AZURE_CLIENT_ID")
        client_secret = self.resolve(f"{prefix}_AZURE_CLIENT_SECRET" if prefix else "AZURE_CLIENT_SECRET")

        return ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )

    def get_env_azure_credentials(self, prefix=None):
        """
        Add Azure credentials to system env and retrieve it using optional prefix.
        If a prefix is provided, keys are prefixed accordingly (e.g., 'FOUNDRY_AZURE_CLIENT_ID').
        """
        tenant_id = self.resolve(f"{prefix}_AZURE_TENANT_ID" if prefix else "AZURE_TENANT_ID")
        client_id = self.resolve(f"{prefix}_AZURE_CLIENT_ID" if prefix else "AZURE_CLIENT_ID")
        client_secret = self.resolve(f"{prefix}_AZURE_CLIENT_SECRET" if prefix else "AZURE_CLIENT_SECRET")

        # Manually set environment variables
        os.environ["AZURE_CLIENT_ID"] = client_id
        os.environ["AZURE_TENANT_ID"] = tenant_id
        os.environ["AZURE_CLIENT_SECRET"] = client_secret

        return EnvironmentCredential()

    def get_openai_config(self, prefix=None):
        """
        Retrieve Azure OpenAI configuration using optional prefix.
        Returns a dictionary with endpoint, api_key, and api_version.
        """
        return {
            "endpoint": self.resolve(f"{prefix}_AZURE_OPENAI_ENDPOINT" if prefix else "AZURE_OPENAI_ENDPOINT"),
            "api_key": self.resolve(f"{prefix}_AZURE_OPENAI_API_KEY" if prefix else "AZURE_OPENAI_API_KEY"),
            "api_version": self.resolve(f"{prefix}_AZURE_OPENAI_API_VERSION" if prefix else "AZURE_OPENAI_API_VERSION")
        }

