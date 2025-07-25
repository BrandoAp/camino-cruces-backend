# 🌿 Sistema de Gestión - Parque Nacional Camino de Cruces

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![API](https://img.shields.io/badge/API-REST-orange.svg)](https://restframework.djangorest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descripción del Proyecto

Sistema web integral para la gestión de visitantes, senderos y análisis estadístico del Parque Nacional Camino de Cruces. Incluye funcionalidades de registro de visitantes, encuestas de satisfacción, dashboard administrativo y gestión de senderos con sus respectivas fotografías.
## Información General

**Base URL:** `http://localhost:8000/api/dashboard/`  
**Formato de respuesta:** JSON  
**Método de autenticación:** Pendiente de implementar


---

---
## 🏗️ Arquitectura del Sistema
```
proyecto-api/
├── 📁 api/                          # Aplicación principal Django
│   ├── 📁 migrations/               # Migraciones de base de datos
│   ├── 📁 services/                 # Capa de servicios (lógica de negocio)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 comentario_service.py  # Gestión de comentarios
│   │   ├── 📄 dashboard_service.py   # Métricas y dashboard
│   │   ├── 📄 foto_sendero_service.py # Management de fotos
│   │   ├── 📄 sendero_service.py     # Lógica de senderos
│   │   ├── 📄 usuario_service.py     # Gestión de usuarios
│   │   └── 📄 valoracion_service.py  # Sistema de valoraciones
│   ├── 📄 __init__.py
│   ├── 📄 admin.py                  # Configuración admin Django
│   ├── 📄 apps.py                   # Configuración de la app
│   ├── 📄 models.py                 # Modelos de datos (ORM)
│   ├── 📄 serializers.py            # Serializadores DRF
│   ├── 📄 tests.py                  # Tests unitarios
│   ├── 📄 urls.py                   # Rutas de la API
│   └── 📄 views.py                  # Vistas y endpoints
├── 📁 docs/                         # Documentación del proyecto
│   └── 📄 dashboard.md              # Documentación del dashboard
├── 📁 parque_api/                   # Configuración principal del proyecto
│   ├── 📄 __init__.py
│   ├── 📄 asgi.py                   # Configuración ASGI
│   ├── 📄 settings.py               # Configuración Django
│   ├── 📄 urls.py                   # URLs principales
│   └── 📄 wsgi.py                   # Configuración WSGI
├── 📄 .gitignore                    # Archivos ignorados por Git
├── 📄 README.md                     # Documentación principal
├── 📄 manage.py                     # Script de gestión Django
└── 📄 requirements.txt              # Dependencias del proyecto
```
---

### 🗂️ Índice de Documentación

| Sección | Descripción | Enlace |
|---------|-------------|--------|
| 📊 **Dashboard API** | Endpoints para estadísticas y reportes | [📄 Dashboard](docs/dashboard.md) |
| 📊 **Registro-Visita API** | Endpoints para visitantes y registro de visitantes | [📄 RegistroVisitante](docs/registro_visita.md) |
| 👤 **Usuarios API** | Endpoints para Registro, autenticación y consulta de usuarios | [📄 Usuarios](docs/usuarios.md) |
| 🏞️ **Senderos API** | Endpoints para Información de senderos | [📄 Senderos](docs/senderos.md) |
| 📋 **Encuestas API** | Endpoints para Registro de encuestas asociadas a visitas | [📄 Encuestas](docs/encuestas.md) |
| 📝 **Comentarios API** | Endpoints para Agregar y listar comentarios (por sendero) | [📄 Comentarios](docs/comentarios.md) |
| ⭐ **Valoraciones API** | Endpoints para Obtener valoraciones promedio de un sendero | [📄 Valoraciones](docs/valoraciones.md) |

---
## 🌐 API Endpoints

### 📊 Dashboard (Estadísticas)
```
GET /api/dashboard/visitas-recientes/     # Últimas visitas
GET /api/dashboard/visitantes-hoy/        # Conteo diario
GET /api/dashboard/encuestas-hoy/         # Encuestas completadas
GET /api/dashboard/visitantes-por-pais/   # Estadísticas geográficas
GET /api/dashboard/visitantes-por-sendero/ # Popularidad de rutas
```

### 📊 Registro-Visitante (Registrar visitas y Obtener visita mediante cedula)
```
POST /api/registrar_visitante_y_visita/   # Registra un visitante nuevo junto a su primera visita
POST /api/registrar-visita/               # Registra una visita de un visitante existente
POST /api/registrar-visita-id/            # Registra una visita por ID de visitante
GET  /api/visitante/cedula/<cedula>/      # Consulta un visitante por su cédula/pasaporte
```


### 👤 Usuarios

```
POST /api/registro/            # Registrar un nuevo usuario
GET  /api/usuario/<id>/        # Obtener usuario por ID
POST /api/login/               # Autenticación y generación de token JWT
```

### 🏞️ Senderos

```
GET /api/sendero/<id>/         # Obtener información de un sendero por ID
GET /api/senderos/             # Listar todos los senderos registrados
```

### 📋 Encuestas

```
POST /api/encuestas/registrar/  # Registrar una encuesta asociada a una visita
```

### 📝 Comentarios
```
POST /api/comentarios/agregar/                         # Agrega un comentario a un sendero (con o sin imagen)
GET  /api/comentarios/sendero/<sendero_id>/            # Lista todos los comentarios de un sendero
```

### ⭐ Valoraciones
```
GET  /api/valoracion-promedio/<sendero_id>/            # Obtiene la valoración promedio de un sendero
GET  /api/comentarios/<sendero_id>/valoraciones/       # Obtiene la distribución de valoraciones (1 a 5 estrellas) de un sendero
```
---
**Última actualización:** Julio 2025  
**Versión:** 1.0.
