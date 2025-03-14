import requests
from typing import Dict, List
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class SerperSearch:
    def __init__(self, api_key: str):
        """
        Inicializa el wrapper de Serper.
        """
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

    def search(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Realiza una búsqueda web utilizando Serper.
        """
        payload = {
            'q': query,
            'gl': 'cl',  # Localización: Chile
            'num': num_results
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json()
            
            organic_results = results.get('organic', [])
            return [
                {
                    "title": r.get("title", ""),
                    "snippet": r.get("snippet", ""),
                    "link": r.get("link", "")
                }
                for r in organic_results[:num_results]
            ]
        except Exception as e:
            print(f"Error en búsqueda: {str(e)}")
            return []

    def get_news(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Obtiene noticias relacionadas con la consulta.
        """
        payload = {
            'q': query,
            'gl': 'cl',
            'num': num_results,
            'type': 'news'
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json()
            
            news_results = results.get('news', [])
            return [
                {
                    "title": n.get("title", ""),
                    "snippet": n.get("snippet", ""),
                    "link": n.get("link", "")
                }
                for n in news_results[:num_results]
            ]
        except Exception as e:
            print(f"Error en búsqueda de noticias: {str(e)}")
            return []

    def get_local_results(self, query: str, location: str, num_results: int = 5) -> List[Dict]:
        """
        Obtiene resultados locales para una consulta y ubicación específicas.
        """
        local_query = f"{query} en {location}"
        payload = {
            'q': local_query,
            'gl': 'cl',
            'num': num_results,
            'type': 'places'
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json()
            
            local_results = results.get('places', [])
            return [
                {
                    "name": r.get("title", ""),
                    "address": r.get("address", ""),
                    "rating": r.get("rating", "N/A")
                }
                for r in local_results[:num_results]
            ]
        except Exception as e:
            print(f"Error en búsqueda local: {str(e)}")
            return []

    def get_real_estate_info(self, location: str, property_type: str = None) -> List[Dict]:
        """
        Búsqueda especializada en información inmobiliaria.
        """
        # Construir query específica para inmuebles
        query_parts = [f"mercado inmobiliario {location}"]
        if property_type:
            query_parts.append(property_type)
        query_parts.append("precio actual")
        
        query = " ".join(query_parts)
        payload = {
            'q': query,
            'gl': 'cl',
            'num': 5
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json()
            
            organic_results = results.get('organic', [])
            return [
                {
                    "title": r.get("title", ""),
                    "snippet": r.get("snippet", ""),
                    "link": r.get("link", ""),
                    "location": location,
                    "property_type": property_type
                }
                for r in organic_results[:5]
            ]
        except Exception as e:
            print(f"Error en búsqueda inmobiliaria: {str(e)}")
            return []

    def get_images(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Obtiene imágenes relacionadas con la consulta.
        """
        payload = {
            'q': query,
            'gl': 'cl',
            'num': num_results,
            'type': 'images'
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json()
            
            image_results = results.get('images', [])
            return [
                {
                    "title": img.get("title", ""),
                    "thumbnail": img.get("thumbnail", ""),
                    "original": img.get("original", "")
                }
                for img in image_results[:num_results]
            ]
        except Exception as e:
            print(f"Error en búsqueda de imágenes: {str(e)}")
            return []
