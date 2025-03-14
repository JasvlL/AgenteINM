from typing import Dict, List
import logging
from integrations.openrouter import OpenRouterLLM
from integrations.serper import SerperSearch
from utils.helpers import log_agent_thought

class MarketAgent:
    def __init__(self, llm: OpenRouterLLM, search: SerperSearch):
        self.llm = llm
        self.search = search
        self.logger = logging.getLogger(__name__)

    def analyze_market_aspects(self, query: str) -> str:
        """
        Analiza los aspectos de mercado de la consulta usando el LLM.
        """
        prompt = f"""
        Como analista de mercado inmobiliario, analiza esta consulta:
        "{query}"
        
        Piensa en voz alta sobre:
        - Qué aspectos del mercado son relevantes
        - Qué tendencias o datos necesitamos considerar
        - Qué tipo de análisis sería más útil
        
        Responde como si estuvieras discutiendo el caso con tu equipo de análisis.
        """
        return self.llm.generate_text(prompt)

    def determine_search_queries(self, query: str) -> List[str]:
        # Primero analizar los aspectos de mercado
        market_analysis = self.analyze_market_aspects(query)
        log_agent_thought(self.logger, "Analista de Mercado", market_analysis)
        """
        Determina las búsquedas necesarias para responder la consulta.
        """
        prompt = f"""
        Para responder a la siguiente consulta inmobiliaria, necesito que me ayudes a determinar qué búsquedas específicas debo realizar.
        Genera una lista de búsquedas que me ayuden a obtener información relevante y actualizada.

        Consulta: {query}

        Por ejemplo, si la consulta es sobre precios de departamentos en Santiago, podrías sugerir búsquedas como:
        - precios actuales departamentos santiago chile
        - tendencias mercado inmobiliario santiago
        - valor metro cuadrado santiago por sector
        """
        
        # Generar pensamiento sobre las búsquedas necesarias
        search_thought = self.llm.generate_text(f"""
        Basado en mi análisis de mercado:
        {market_analysis}
        
        ¿Qué datos específicos necesitamos buscar? ¿Qué tendencias son más relevantes?
        Piensa en las búsquedas que nos darán la información más valiosa.
        """)
        log_agent_thought(self.logger, "Analista de Mercado", search_thought)
        
        # Extraer las búsquedas sugeridas
        suggestions = self.llm.generate_text(prompt)
        queries = [line.strip('- ').strip() for line in suggestions.split('\n') if line.strip().startswith('-')]
        result_queries = queries if queries else [query]
        return result_queries

    def search_and_analyze(self, query: str) -> str:
        # Pensar sobre el enfoque de análisis
        approach_thought = self.llm.generate_text(f"""
        Para esta consulta sobre el mercado:
        "{query}"
        
        ¿Qué enfoque de análisis sería más efectivo? ¿Qué factores son cruciales?
        Expresa tus pensamientos sobre cómo abordar este análisis de mercado.
        """)
        log_agent_thought(self.logger, "Analista de Mercado", approach_thought)
        """
        Realiza búsquedas inteligentes y analiza la información encontrada.
        """
        # Determinar las búsquedas necesarias
        search_queries = self.determine_search_queries(query)
        
        # Realizar búsquedas
        all_results = []
        for search_query in search_queries:
            search_thought = self.llm.generate_text(f"""
            Voy a investigar: "{search_query}"
            ¿Qué tipo de datos espero encontrar? ¿Qué tendencias podrían ser relevantes?
            """)
            log_agent_thought(self.logger, "Analista de Mercado", search_thought)
            
            # Búsquedas y análisis de resultados
            web_results = self.search.search(search_query, num_results=3)
            all_results.extend([r["snippet"] for r in web_results])
            
            news_results = self.search.get_news(search_query, num_results=2)
            all_results.extend([r["snippet"] for r in news_results])
            
            if "precio" in search_query.lower() or "valor" in search_query.lower():
                real_estate_results = self.search.get_real_estate_info(search_query)
                all_results.extend([r["snippet"] for r in real_estate_results])
        
        # Combinar y analizar la información recopilada
        context = "\n".join(all_results)
        
        prompt = f"""
        Como experto en el mercado inmobiliario, analiza la siguiente información y genera una respuesta definitiva y completa.
        La respuesta debe ser profesional y proporcionar toda la información necesaria sin necesidad de consultas adicionales.
        
        Consulta original: {query}
        
        Información recopilada:
        {context}
        
        Importante:
        - Proporciona una respuesta definitiva y concluyente
        - Incluye datos específicos y análisis de mercado
        - Si hay tendencias o cambios en el mercado, explícalos claramente
        - Si hay datos contradictorios, explica cuál es la información más precisa y por qué
        - Proporciona valoraciones y estimaciones concretas cuando sea relevante
        - NO sugieras consultar con otros profesionales o analistas
        """
        
        # Analizar la información recopilada
        analysis_thought = self.llm.generate_text(f"""
        He recopilado datos interesantes. Déjame analizarlos:
        {' '.join(all_results[:200])}...
        
        ¿Qué tendencias puedo identificar? ¿Qué nos dicen estos datos sobre el mercado?
        """)
        log_agent_thought(self.logger, "Analista de Mercado", analysis_thought)
        
        # Pensar sobre las conclusiones finales
        final_thought = self.llm.generate_text(f"""
        Después de analizar todos los datos del mercado, ¿cuáles son mis conclusiones principales?
        ¿Qué recomendaciones específicas puedo ofrecer basadas en las tendencias actuales?
        """)
        log_agent_thought(self.logger, "Analista de Mercado", final_thought)
        
        # Generar respuesta final
        response = self.llm.generate_text(prompt)
        return response

    def handle_query(self, query: str) -> str:
        """
        Punto de entrada principal para manejar consultas.
        """
        return self.search_and_analyze(query)
