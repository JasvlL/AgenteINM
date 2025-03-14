import logging
from typing import Any, Dict

def setup_logging(log_level: str = "INFO") -> None:
    """
    Configura el sistema de logging para el proyecto con salida a archivo y consola.
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')

    # Crear el logger principal
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    
    # Limpiar handlers existentes
    logger.handlers = []

    # Formato simple para los logs
    formatter = logging.Formatter('%(message)s')

    # Handler para archivo markdown
    file_handler = logging.FileHandler('conversation.md', encoding='utf-8', mode='w')
    file_handler.setLevel(numeric_level)
    
    # Escribir encabezado del archivo markdown
    with open('conversation.md', 'w', encoding='utf-8') as f:
        f.write("# 🏢 Análisis Inmobiliario - Conversación del Equipo\n\n")
        f.write("## Participantes:\n")
        f.write("- 👥 Coordinador: Líder del equipo\n")
        f.write("- ⚖️ Experto Legal: Especialista en normativas inmobiliarias\n")
        f.write("- 📊 Analista de Mercado: Experto en tendencias y valoraciones\n\n")
        f.write("## Conversación:\n\n")
    
    # Formato especial para markdown
    md_formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(md_formatter)
    logger.addHandler(file_handler)

    # Handler para consola con formato más simple
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

def log_agent_thought(logger: logging.Logger, agent: str, thought: str) -> None:
    """
    Registra el pensamiento de un agente en formato markdown.
    """
    # Asegurar que el pensamiento no esté vacío
    if not thought or thought.isspace():
        return
    
    # Formatear mensaje en markdown
    # Determinar el emoji según el agente
    emoji = "👥" if agent == "Coordinador" else "⚖️" if agent == "Experto Legal" else "📊"
    
    message = f"""
### {emoji} {agent}

{thought}

---
"""
    logger.info(message)

def get_conversation_file() -> str:
    """
    Retorna el contenido del archivo de conversación.
    """
    try:
        with open('conversation.md', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def safe_get(data: Dict[str, Any], keys: str, default: Any = None) -> Any:
    """
    Obtiene un valor de un diccionario anidado de forma segura.
    """
    keys = keys.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, {})
        else:
            return default
    return data if data != {} else default

def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Formatea un número como moneda.
    """
    return f"{currency} {amount:,.2f}"

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Trunca un texto a una longitud máxima, añadiendo '...' si es necesario.
    """
    return (text[:max_length] + '...') if len(text) > max_length else text

def parse_address(address: str) -> Dict[str, str]:
    """
    Parsea una dirección en sus componentes.
    """
    # Esta es una implementación muy básica y puede necesitar mejoras
    parts = address.split(',')
    return {
        "street": parts[0].strip() if len(parts) > 0 else "",
        "city": parts[1].strip() if len(parts) > 1 else "",
        "state": parts[2].strip() if len(parts) > 2 else "",
        "country": parts[3].strip() if len(parts) > 3 else ""
    }

def calculate_percentage(part: float, whole: float) -> float:
    """
    Calcula el porcentaje de una parte respecto al todo.
    """
    try:
        return (part / whole) * 100
    except ZeroDivisionError:
        return 0.0
