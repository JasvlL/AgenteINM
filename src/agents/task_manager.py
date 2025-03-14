from typing import Dict, List
from .legal import LegalAgent
from .market import MarketAgent
from integrations.openrouter import OpenRouterLLM
from integrations.serper import SerperSearch

import logging
from utils.helpers import log_agent_thought

class TaskManager:
    def __init__(self, llm: OpenRouterLLM, search: SerperSearch, legal_agent: LegalAgent, market_agent: MarketAgent):
        self.llm = llm
        self.search = search
        self.legal_agent = legal_agent
        self.market_agent = market_agent
        self.logger = logging.getLogger(__name__)

    def think_about_query(self, query: str) -> str:
        """
        Genera un pensamiento natural sobre la consulta usando el LLM.
        """
        prompt = f"""
        Como coordinador de un equipo de expertos inmobiliarios, analiza esta consulta:
        "{query}"
        
        Expresa tus pensamientos de manera natural sobre:
        - Qué aspectos de la consulta te parecen más importantes
        - Qué tipo de expertise necesitaremos
        - Cómo podríamos abordar esto en equipo
        
        Responde como si estuvieras pensando en voz alta, de manera natural y conversacional.
        """
        return self.llm.generate_text(prompt)

    def decide_team_approach(self, analysis: str) -> str:
        """
        Decide cómo abordar la consulta en equipo.
        """
        prompt = f"""
        Basado en este análisis:
        "{analysis}"
        
        Como coordinador del equipo, expresa tus pensamientos sobre:
        - Qué miembros del equipo deberían participar
        - Cómo deberíamos distribuir el trabajo
        - Qué información necesitamos recopilar
        
        Responde de manera natural, como si estuvieras planificando con tu equipo.
        """
        return self.llm.generate_text(prompt)

    def analyze_query_intent(self, query: str) -> Dict[str, bool]:
        # Generar pensamiento inicial sobre la consulta
        initial_thought = self.think_about_query(query)
        log_agent_thought(self.logger, "Coordinador", initial_thought)
        """
        Analiza la intención de la consulta para determinar qué agentes deben intervenir.
        """
        prompt = f"""
        Analiza la siguiente consulta inmobiliaria y determina qué aspectos necesitan ser abordados.
        Piensa cuidadosamente sobre qué tipo de información sería más útil para el usuario.

        Consulta: {query}

        Considera:
        - ¿La consulta involucra aspectos legales o normativos?
        - ¿Requiere información del mercado o análisis económico?
        - ¿Necesita información general del sector inmobiliario?

        Responde pensando en el beneficio para el usuario.
        """
        
        # Analizar y decidir el enfoque del equipo
        team_approach = self.decide_team_approach(initial_thought)
        log_agent_thought(self.logger, "Coordinador", team_approach)
        
        # Determinar la participación de cada agente basado en el análisis
        needs = {
            "legal": "legal" in team_approach.lower() or "normativ" in team_approach.lower() or "ley" in team_approach.lower(),
            "market": "mercado" in team_approach.lower() or "precio" in team_approach.lower() or "valor" in team_approach.lower(),
            "general": True
        }
        
        return needs

    def coordinate_response(self, query: str) -> str:
        # Pensar sobre cómo coordinar la respuesta
        coordination_thought = self.llm.generate_text(f"""
        Como coordinador, ¿cómo deberíamos abordar esta consulta?
        "{query}"
        
        Expresa tus pensamientos sobre la mejor manera de coordinar al equipo para responder.
        """)
        log_agent_thought(self.logger, "Coordinador", coordination_thought)
        """
        Coordina la obtención de respuestas de los diferentes agentes y las combina
        de manera coherente y natural.
        """
        # Analizar la intención de la consulta
        needs = self.analyze_query_intent(query)
        responses = []
        
        # Obtener respuestas de los agentes necesarios
        if needs["legal"]:
            legal_request_thought = self.llm.generate_text(f"""
            ¿Cómo debería solicitar la información legal para esta consulta?
            "{query}"
            
            Expresa tus pensamientos sobre qué necesitamos del equipo legal.
            """)
            log_agent_thought(self.logger, "Coordinador", legal_request_thought)
            
            legal_response = self.legal_agent.handle_query(query)
            responses.append(legal_response)
            
        if needs["market"]:
            market_request_thought = self.llm.generate_text(f"""
            ¿Qué información de mercado necesitamos para esta consulta?
            "{query}"
            
            Expresa tus pensamientos sobre qué necesitamos del equipo de mercado.
            """)
            log_agent_thought(self.logger, "Coordinador", market_request_thought)
            
            market_response = self.market_agent.handle_query(query)
            responses.append(market_response)
        
        # Si no hay respuestas específicas, usar al menos un agente
        if not responses:
            responses.append(self.market_agent.handle_query(query))
        
        # Combinar las respuestas en un formato natural
        prompt = f"""
        Como experto inmobiliario integral, genera una respuesta definitiva y completa que combine toda la información disponible.
        
        Consulta del cliente: {query}

        Información disponible:
        {' '.join(responses)}

        Instrucciones:
        - Proporciona una respuesta definitiva y concluyente
        - Combina la información legal y de mercado de forma coherente
        - Explica todos los aspectos relevantes con autoridad
        - Si hay información contradictoria, determina la más precisa
        - Incluye todos los detalles necesarios para tomar decisiones
        - NO sugieras consultas con otros profesionales
        - Mantén un tono profesional pero accesible
        """
        
        # Pensar sobre cómo integrar las respuestas
        integration_thought = self.llm.generate_text(f"""
        Hemos recibido las respuestas del equipo. ¿Cómo deberíamos integrar esta información?
        
        Expresa tus pensamientos sobre cómo combinar las diferentes perspectivas en una respuesta coherente.
        """)
        log_agent_thought(self.logger, "Coordinador", integration_thought)
        final_response = self.llm.generate_text(prompt)
        
        log_agent_thought(self.logger, "Coordinador", f"He preparado una respuesta completa basada en el análisis del equipo.")
        return final_response

    def handle_query(self, query: str) -> str:
        """
        Punto de entrada principal para manejar consultas.
        """
        return self.coordinate_response(query)
