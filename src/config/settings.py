import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    CLICKUP_WORKSPACE_ID = os.getenv("CLICKUP_WORKSPACE_ID")
    CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")

    # Configuraciones adicionales
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Configuraciones de los agentes
    LEGAL_AGENT_MODEL = os.getenv("LEGAL_AGENT_MODEL", "gpt-3.5-turbo")
    MARKET_AGENT_MODEL = os.getenv("MARKET_AGENT_MODEL", "gpt-3.5-turbo")

    # Configuraciones de ClickUp
    CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")

    @classmethod
    def validate(cls):
        """
        Valida que todas las configuraciones requeridas estén presentes.
        """
        required_settings = [
            "COMPOSIO_API_KEY",
            "SERPER_API_KEY",
            "OPENROUTER_API_KEY",
            "CLICKUP_WORKSPACE_ID",
            "CLICKUP_API_KEY"
        ]
        
        for setting in required_settings:
            if not getattr(cls, setting):
                raise ValueError(f"La configuración {setting} es requerida y no está definida.")

# Validar configuraciones al importar el módulo
Settings.validate()
