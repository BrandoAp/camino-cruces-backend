import requests
from decouple import config
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from datetime import datetime

class GitHubIssueMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        
        github_token = config('GITHUB_TOKEN')
        repo = 'BrandoAp/camino-cruces-backend'

        if not github_token or not repo:
            return
        
        title = f"Error en endpoint {request.path}"
        body = f"""Se produjo una excepcion no controlada en la API
        **Endpoint:** `{request.path}`
        **Método:** `{request.method}`  
        **Hora:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  

        **Error:** `{str(exception)}`
        **Usuario autenticado:** {request.user if request.user.is_authenticated else "Anónimo"}
        **Servidor:** {getattr(settings, 'ENVIRONMENT', 'Producción')}
        """

        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github+json"
        }

        data = {
            "title": title,
            "body": body,
            "labels": ["bug", "auto-reported"],
        }
        
        #Intentar Crear el issue
        try:
            response = requests.post(
                f"https://api.github.com/repos/{repo}/issues",
                headers=headers,
                json=data,
                timeout=10
            )
            if response.status_code != 201:
                print(f"No se pudo crear el issue: {response.text}")
        except Exception as e:
            print(f"Error al enviar issue a GitHub: {e}")

        # Django seguirá su flujo normal (mostrará el error 500)
        return None
    