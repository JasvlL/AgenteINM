from typing import Dict, List
import logging
from integrations.openrouter import OpenRouterLLM
from integrations.serper import SerperSearch
from utils.helpers import log_agent_thought

class LegalAgent:
    def __init__(self, llm: OpenRouterLLM, search: SerperSearch):
        self.llm = llm
        self.search = search
        self.logger = logging.getLogger(__name__)

    def analyze_legal_aspects(self, query: str) -> str:
        """
        Analiza los aspectos legales de la consulta usando el LLM.
        """
        prompt = f"""
        Como experto legal inmobiliario, analiza esta consulta:
        "{query}"
        
        Piensa en voz alta sobre:
        - Qué aspectos legales son relevantes
        - Qué normativas o regulaciones debemos considerar
        - Qué información legal necesitamos buscar
        
        Responde como si estuvieras analizando el caso con tus colegas.
        """
        return self.llm.generate_text(prompt)

    def determine_legal_searches(self, query: str) -> List[str]:
        # Primero analizar los aspectos legales
        legal_analysis = self.analyze_legal_aspects(query)
        log_agent_thought(self.logger, "Experto Legal", legal_analysis)
        """
        Determina las búsquedas legales necesarias para responder la consulta.
        """
        prompt = f"""
        Para responder a la siguiente consulta legal inmobiliaria, necesito que me ayudes a determinar qué búsquedas específicas debo realizar.
        Genera una lista de búsquedas que me ayuden a obtener información legal relevante y actualizada.

        Consulta: {query}

        Por ejemplo, si la consulta es sobre requisitos legales para comprar una propiedad, podrías sugerir búsquedas como:
        - requisitos legales compraventa inmobiliaria chile
        - documentos necesarios escritura propiedad chile
        - normativa actual compraventa inmuebles chile
        """
        
        # Generar pensamiento sobre las búsquedas necesarias
        search_thought = self.llm.generate_text(f"""
        Basado en mi análisis legal:
        {legal_analysis}
        
        ¿Qué información específica necesito buscar para dar una respuesta completa?
        Piensa en las búsquedas más relevantes para este caso.
        """)
        log_agent_thought(self.logger, "Experto Legal", search_thought)
        
        # Extraer las búsquedas sugeridas
        suggestions = self.llm.generate_text(prompt)
        queries = [line.strip('- ').strip() for line in suggestions.split('\n') if line.strip().startswith('-')]
        result_queries = queries if queries else [query]
        return result_queries

    def search_and_analyze_legal(self, query: str) -> str:
        # Pensar sobre el enfoque de análisis
        approach_thought = self.llm.generate_text(f"""
        Para esta consulta:
        "{query}"
        
        ¿Cómo debería enfocar mi análisis legal? ¿Qué aspectos son críticos?
        Expresa tus pensamientos sobre la mejor manera de abordar este análisis.
        """)
        log_agent_thought(self.logger, "Experto Legal", approach_thought)
        """
        Realiza búsquedas legales inteligentes y analiza la información encontrada.
        """
        # Determinar las búsquedas necesarias
        search_queries = self.determine_legal_searches(query)
        
        # Realizar búsquedas
        all_results = []
        for search_query in search_queries:
            search_thought = self.llm.generate_text(f"""
            Voy a buscar información sobre: "{search_query}"
            ¿Qué espero encontrar con esta búsqueda? ¿Qué aspectos son cruciales?
            """)
            log_agent_thought(self.logger, "Experto Legal", search_thought)
            
            # Búsquedas y análisis de resultados
            web_results = self.search.search(search_query, num_results=3)
            all_results.extend([r["snippet"] for r in web_results])
            
            if "ley" in search_query.lower() or "normativa" in search_query.lower():
                news_results = self.search.get_news(search_query + " legal inmobiliario", num_results=2)
                all_results.extend([r["snippet"] for r in news_results])
        
        # Combinar y analizar la información recopilada
        context = "\n".join(all_results)
        
        prompt = f"""
        Como experto legal inmobiliario, analiza la siguiente información y genera una respuesta definitiva y completa.
        La respuesta debe ser clara, precisa y proporcionar toda la información necesaria sin necesidad de consultas adicionales.
        
        Consulta original: {query}
        
        Información recopilada:
        {context}
        
        Importante:
        - Proporciona una respuesta definitiva y concluyente
        - Explica los conceptos legales de forma clara y accesible
        - Detalla todos los requisitos y plazos relevantes
        - Si hay diferentes interpretaciones legales, explica la más aceptada y por qué
        - Incluye información sobre normativas recientes o cambios pendientes
        - NO sugieras consultar con otros profesionales
        """
        
        # Analizar la información recopilada
        analysis_thought = self.llm.generate_text(f"""
        He encontrado información relevante. Déjame analizarla:
        {' '.join(all_results[:200])}...
        
        ¿Qué conclusiones legales puedo extraer? ¿Qué implicaciones tiene esto?
        """)
        log_agent_thought(self.logger, "Experto Legal", analysis_thought)
        
        # Pensar sobre la respuesta final
        final_thought = self.llm.generate_text(f"""
        Basado en toda la información recopilada y analizada, ¿cuál es mi conclusión legal final?
        ¿Qué recomendaciones específicas puedo dar?
        """)
        log_agent_thought(self.logger, "Experto Legal", final_thought)
        
        # Generar respuesta final
        response = self.llm.generate_text(prompt)
        return response

    def handle_query(self, query: str) -> str:
        """
        Punto de entrada principal para manejar consultas legales.
        """
        return self.search_and_analyze_legal(query)
