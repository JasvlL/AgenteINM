import requests
from typing import Dict, List
from config.settings import Settings

class ClickUpIntegration:
    def __init__(self, workspace_id: str):
        self.workspace_id = workspace_id
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": Settings.CLICKUP_API_KEY,
            "Content-Type": "application/json"
        }
        print("ClickUp Integration inicializada con Workspace ID:", workspace_id)
        
    def test_connection(self):
        """
        Prueba la conexión con ClickUp y verifica los permisos.
        """
        try:
            # Obtener equipos
            url = f"{self.base_url}/team"
            print("\nProbando conexión con ClickUp...")
            print(f"URL: {url}")
            print(f"Headers: {self.headers}")
            
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                print("\nConexión exitosa con ClickUp")
                teams = response.json().get("teams", [])
                for team in teams:
                    print(f"Equipo encontrado: {team.get('name')} (ID: {team.get('id')})")
                    # Obtener espacios del equipo
                    self.get_team_spaces(team.get('id'))
            else:
                print(f"\nError en la conexión: Status Code {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except Exception as e:
            print(f"\nError al probar la conexión: {str(e)}")

    def get_team_spaces(self, team_id: str):
        """
        Obtiene los espacios de un equipo.
        """
        try:
            url = f"{self.base_url}/team/{team_id}/space"
            print(f"\nObteniendo espacios del equipo {team_id}...")
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                spaces = response.json().get("spaces", [])
                for space in spaces:
                    print(f"Espacio encontrado: {space.get('name')} (ID: {space.get('id')})")
                    # Obtener listas del espacio
                    self.get_space_lists(space.get('id'))
            else:
                print(f"Error al obtener espacios: Status Code {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except Exception as e:
            print(f"Error al obtener espacios: {str(e)}")

    def get_space_lists(self, space_id: str):
        """
        Obtiene las listas de un espacio.
        """
        try:
            url = f"{self.base_url}/space/{space_id}/list"
            print(f"\nObteniendo listas del espacio {space_id}...")
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                lists = response.json().get("lists", [])
                for list_item in lists:
                    print(f"Lista encontrada: {list_item.get('name')} (ID: {list_item.get('id')})")
            else:
                print(f"Error al obtener listas: Status Code {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except Exception as e:
            print(f"Error al obtener listas: {str(e)}")

    def get_tasks(self, list_id: str) -> List[Dict]:
        """
        Obtiene las tareas de una lista específica en ClickUp.
        """
        try:
            url = f"{self.base_url}/list/{list_id}/task"
            print(f"\nObteniendo tareas de la lista {list_id}...")
            print(f"URL: {url}")
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error en la respuesta: Status Code {response.status_code}")
                print(f"Respuesta: {response.text}")
                return []
                
            data = response.json()
            tasks = data.get("tasks", [])
            print(f"Tareas obtenidas: {len(tasks)}")
            return tasks
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener tareas: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta detallada: {e.response.text}")
            return []

    def create_task(self, list_id: str, task_data: Dict) -> Dict:
        """
        Crea una nueva tarea en una lista específica de ClickUp.
        """
        try:
            url = f"{self.base_url}/list/{list_id}/task"
            response = requests.post(url, headers=self.headers, json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al crear tarea: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta detallada: {e.response.text}")
            raise

    def update_task(self, task_id: str, task_data: Dict) -> Dict:
        """
        Actualiza una tarea existente en ClickUp.
        """
        try:
            url = f"{self.base_url}/task/{task_id}"
            response = requests.put(url, headers=self.headers, json=task_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al actualizar tarea: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta detallada: {e.response.text}")
            raise

    def get_comments(self, task_id: str) -> List[Dict]:
        """
        Obtiene los comentarios de una tarea específica en ClickUp.
        """
        try:
            url = f"{self.base_url}/task/{task_id}/comment"
            print(f"\nObteniendo comentarios de la tarea {task_id}...")
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error en la respuesta: Status Code {response.status_code}")
                print(f"Respuesta: {response.text}")
                return []
                
            data = response.json()
            comments = data.get("comments", [])
            print(f"Comentarios obtenidos: {len(comments)}")
            return comments
            
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener comentarios: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta detallada: {e.response.text}")
            return []

    def upload_attachment(self, task_id: str, file_path: str) -> Dict:
        """
        Sube un archivo como adjunto a una tarea específica de ClickUp.
        """
        try:
            url = f"{self.base_url}/task/{task_id}/attachment"
            headers = {
                "Authorization": Settings.CLICKUP_API_KEY
            }  # No incluir Content-Type para subida de archivos
            
            with open(file_path, 'rb') as file:
                files = {
                    'attachment': (file_path.split('/')[-1], file, 'text/markdown')
                }
                print(f"\nSubiendo archivo {file_path} a la tarea {task_id}...")
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                return response.json()
                
        except requests.exceptions.RequestException as e:
            print(f"Error al subir archivo: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta detallada: {e.response.text}")
            raise

    def create_comment(self, task_id: str, comment_text: str) -> Dict:
        """
        Crea un nuevo comentario en una tarea específica de ClickUp.
        """
        try:
            url = f"{self.base_url}/task/{task_id}/comment"
            comment_data = {"comment_text": comment_text}
            print(f"\nCreando comentario en la tarea {task_id}...")
            response = requests.post(url, headers=self.headers, json=comment_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al crear comentario: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Respuesta detallada: {e.response.text}")
            raise
