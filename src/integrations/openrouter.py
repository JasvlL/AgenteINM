import requests
from typing import Dict, List

class OpenRouterLLM:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_text(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        """
        Genera texto utilizando el modelo especificado de OpenRouter.
        """
        url = f"{self.base_url}/chat/completions"
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()["choices"][0]["message"]["content"]

    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analiza el sentimiento del texto proporcionado.
        """
        prompt = f"Analiza el sentimiento del siguiente texto y clasifícalo como positivo, negativo o neutral: '{text}'"
        result = self.generate_text(prompt)
        # TODO: Procesar el resultado para extraer la clasificación del sentimiento
        return {"sentiment": result}

    def summarize_text(self, text: str, max_length: int = 100) -> str:
        """
        Resume el texto proporcionado.
        """
        prompt = f"Resume el siguiente texto en no más de {max_length} palabras: '{text}'"
        return self.generate_text(prompt)

    def answer_question(self, context: str, question: str) -> str:
        """
        Responde una pregunta basada en el contexto proporcionado.
        """
        prompt = f"Contexto: {context}\n\nPregunta: {question}\n\nRespuesta:"
        return self.generate_text(prompt)
