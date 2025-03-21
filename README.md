# Sistema de Agentes Inmobiliarios Inteligentes (Agentes-Inmobiliaria)

## Descripción General
Este proyecto desarrolla un sistema inteligente de agentes colaborativos para la gestión inmobiliaria, integrado con ClickUp. Utiliza IA avanzada para automatizar y optimizar procesos de gestión inmobiliaria a través de diferentes roles especializados.

## Objetivo Principal
Crear un ecosistema de agentes de IA que trabajen colaborativamente para gestionar tareas inmobiliarias en ClickUp, respondiendo a consultas y ejecutando acciones de manera natural y eficiente, simulando un equipo humano real.

## Características Principales
- Integración con ClickUp para gestión de tareas y comentarios
- Procesamiento de lenguaje natural avanzado utilizando OpenRouter
- Agentes especializados: Legal y de Mercado
- Búsquedas web en tiempo real para validación de información utilizando Serper
- Sistema de menciones para activar agentes (@AI)

## Requisitos
- Python 3.8+
- Pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
   ```
   git clone https://github.com/tu-usuario/agentes-inmobiliaria.git
   cd agentes-inmobiliaria
   ```

2. Crear un entorno virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno:
   Copia el archivo `.env.example` a `.env` y completa las variables con tus propias claves API y configuraciones.

## Configuración
Asegúrate de tener las siguientes claves API y configuraciones en tu archivo `.env`:
- COMPOSIO_API_KEY: Tu clave API de Composio
- SERPER_API_KEY: Tu clave API de Serper
- OPENROUTER_API_KEY: Tu clave API de OpenRouter
- CLICKUP_WORKSPACE_ID: ID de tu espacio de trabajo en ClickUp
- CLICKUP_LIST_ID: ID de la lista en ClickUp donde se gestionarán las tareas

## Uso
Para ejecutar el sistema:
```
python src/main.py
```

El sistema iniciará y estará listo para procesar menciones (@AI) en las tareas de ClickUp dentro del espacio de trabajo y lista especificados.

## Desarrollo
Para ejecutar las pruebas:
```
pytest
```

### Estructura del Proyecto
```
agentes-inmobiliaria/
├── .env                    # Variables de entorno (no incluido en el repositorio)
├── requirements.txt        # Dependencias del proyecto
├── README.md               # Este archivo
├── src/
│   ├── __init__.py
│   ├── main.py             # Punto de entrada principal
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py     # Configuraciones del proyecto
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── legal.py        # Agente Legal
│   │   └── market.py       # Agente de Mercado
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── clickup.py      # Integración con ClickUp
│   │   ├── openrouter.py   # Integración con OpenRouter (LLM)
│   │   └── serper.py       # Integración con Serper (búsqueda web)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py      # Funciones auxiliares
└── tests/
    └── test_basic.py       # Pruebas básicas del sistema
```

## Contribución
Las contribuciones son bienvenidas. Por favor, sigue estos pasos para contribuir:
1. Haz un fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/AmazingFeature`)
3. Haz tus cambios y commitea (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Por favor, asegúrate de actualizar las pruebas según corresponda y de seguir las convenciones de estilo del proyecto.

## Licencia
[MIT](https://choosealicense.com/licenses/mit/)

## Contacto
Jeferson Zelaya - jeferson.zelayae@gmail.com

Link del Proyecto: [https://github.com/tu-usuario/agentes-inmobiliaria](https://github.com/tu-usuario/agentes-inmobiliaria)
