import requests
import traceback
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


class GitHubErrorReporter(MiddlewareMixin):
    """
    Middleware que captura excepciones y automáticamente crea issues en GitHub
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def process_exception(self, request, exception):
        """
        Se ejecuta cuando ocurre una excepción no manejada
        """
        # Solo reportar en producción (cuando DEBUG=False)
        if not settings.DEBUG:
            self.create_github_issue(request, exception)
        
        # Retornar None permite que Django maneje la excepción normalmente
        return None
    
    def create_github_issue(self, request, exception):
        """
        Crea un issue en GitHub con los detalles del error
        """
        try:
            github_token = settings.GITHUB_TOKEN
            repo = settings.GITHUB_REPO
            
            # Extraer información del error
            error_type = exception.__class__.__name__
            error_message = str(exception)
            error_traceback = ''.join(traceback.format_tb(exception.__traceback__))
            
            # Construir el cuerpo del issue
            issue_body = f"""##  Error detectado en producción (DigitalOcean)

**Tipo de error:** `{error_type}`

**Mensaje:** 
{error_message}


**Endpoint afectado:** `{request.method} {request.path}`

**Query Parameters:** `{dict(request.GET)}`

**IP del cliente:** `{self.get_client_ip(request)}`

**User Agent:** `{request.META.get('HTTP_USER_AGENT', 'N/A')[:100]}`

**Timestamp:** `{timezone.now().strftime('%Y-%m-%d %H:%M:%S')}`

### Stack Trace
{error_traceback}


---
*Issue creado automáticamente desde DigitalOcean App Platform*
            """
            
            # Datos del issue
            issue_data = {
                "title": f" {error_type} en {request.path}",
                "body": issue_body,
                "labels": ["bug", "production", "automated", "digitalocean"]
            }
            
            # Enviar request a GitHub API
            response = requests.post(
                f"https://api.github.com/repos/{repo}/issues",
                json=issue_data,
                headers={
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json"
                },
                timeout=5
            )
            
            # Log del resultado (opcional)
            if response.status_code == 201:
                print(f"✓ Issue creado en GitHub para error: {error_type}")
            else:
                print(f"✗ Error creando issue en GitHub: {response.status_code}")
                
        except Exception as e:
            # No queremos que el error reporter cause más errores
            print(f"Error en GitHubErrorReporter: {str(e)}")
    
    def get_client_ip(self, request):
        """
        Obtiene la IP real del cliente (considerando proxies)
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
