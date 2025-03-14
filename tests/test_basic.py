import pytest
from unittest.mock import MagicMock, patch
from src.config.settings import Settings
from src.integrations.clickup import ClickUpIntegration
from src.integrations.openrouter import OpenRouterLLM
from src.integrations.serper import SerperSearch
from src.agents.legal import LegalAgent
from src.agents.market import MarketAgent
from src.main import initialize_agents, process_mention

@pytest.fixture
def mock_settings():
    return Settings()

@pytest.fixture
def mock_llm():
    return MagicMock(spec=OpenRouterLLM)

@pytest.fixture
def mock_search():
    return MagicMock(spec=SerperSearch)

def test_settings_load(mock_settings):
    """Prueba que las configuraciones se carguen correctamente."""
    assert mock_settings.COMPOSIO_API_KEY is not None
    assert mock_settings.SERPER_API_KEY is not None
    assert mock_settings.OPENROUTER_API_KEY is not None
    assert mock_settings.CLICKUP_WORKSPACE_ID is not None

def test_clickup_integration(mock_settings):
    """Prueba básica de la integración con ClickUp."""
    clickup = ClickUpIntegration(mock_settings.CLICKUP_WORKSPACE_ID)
    assert clickup.workspace_id == mock_settings.CLICKUP_WORKSPACE_ID

def test_openrouter_integration(mock_settings):
    """Prueba básica de la integración con OpenRouter."""
    llm = OpenRouterLLM(mock_settings.OPENROUTER_API_KEY)
    assert llm.api_key == mock_settings.OPENROUTER_API_KEY

def test_serper_integration(mock_settings):
    """Prueba básica de la integración con Serper."""
    search = SerperSearch(mock_settings.SERPER_API_KEY)
    assert search.api_key == mock_settings.SERPER_API_KEY

def test_legal_agent(mock_llm, mock_search):
    """Prueba básica del agente legal."""
    legal_agent = LegalAgent(mock_llm, mock_search)
    assert legal_agent.llm == mock_llm
    assert legal_agent.search == mock_search

    # Prueba de analyze_document
    mock_llm.generate_text.return_value = "Análisis del documento"
    result = legal_agent.analyze_document("Documento de prueba")
    assert "summary" in result
    assert "recommendations" in result

    # Prueba de verify_compliance
    mock_llm.generate_text.return_value = "La propiedad cumple con la zonificación y tiene los permisos en orden. No se detectan problemas legales."
    result = legal_agent.verify_compliance({"address": "123 Test St"})
    assert result["zoning_compliant"] == True
    assert result["permits_in_order"] == True
    assert result["legal_issues"] == True

def test_market_agent(mock_llm, mock_search):
    """Prueba básica del agente de mercado."""
    market_agent = MarketAgent(mock_llm, mock_search)
    assert market_agent.llm == mock_llm
    assert market_agent.search == mock_search

    # Prueba de analyze_market_trends
    mock_search.search.return_value = [{"snippet": "Tendencia del mercado"}]
    mock_llm.generate_text.return_value = "Análisis de tendencias"
    result = market_agent.analyze_market_trends("Ciudad de prueba")
    assert "location" in result
    assert "trend_summary" in result
    assert "detailed_analysis" in result

    # Prueba de evaluate_property_value
    mock_search.search.return_value = [{"snippet": "Datos del mercado"}]
    mock_llm.generate_text.return_value = "El valor estimado es $500,000"
    result = market_agent.evaluate_property_value({"location": "123 Test St"})
    assert result["estimated_value"] == 500000.0
    assert "confidence" in result
    assert "evaluation_summary" in result

def test_initialize_agents(mock_settings):
    """Prueba la inicialización de agentes."""
    with patch('src.main.OpenRouterLLM') as mock_llm, \
         patch('src.main.SerperSearch') as mock_search:
        legal_agent, market_agent = initialize_agents(mock_settings)
        assert isinstance(legal_agent, LegalAgent)
        assert isinstance(market_agent, MarketAgent)

def test_process_mention(mock_llm, mock_search):
    """Prueba el procesamiento de menciones."""
    legal_agent = LegalAgent(mock_llm, mock_search)
    market_agent = MarketAgent(mock_llm, mock_search)

    # Prueba mención legal
    mock_llm.generate_text.return_value = "Respuesta legal"
    result = process_mention({"content": "Consulta legal"}, legal_agent, market_agent)
    assert "Respuesta legal" in result

    # Prueba mención de mercado
    mock_llm.generate_text.return_value = "Respuesta de mercado"
    result = process_mention({"content": "Consulta de mercado"}, legal_agent, market_agent)
    assert "Respuesta de mercado" in result

    # Prueba mención general
    mock_llm.generate_text.side_effect = ["Respuesta legal", "Respuesta de mercado"]
    result = process_mention({"content": "Consulta general"}, legal_agent, market_agent)
    assert "Respuesta Legal:" in result
    assert "Respuesta de Mercado:" in result

if __name__ == "__main__":
    pytest.main()
