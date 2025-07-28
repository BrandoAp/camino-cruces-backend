
# Dashboard - Parque Nacional Camino de Cruces

## 📊 Endpoints del Dashboard

### 1. Visitas Recientes
**GET** `/dashboard/visitas-recientes/`

Obtiene las últimas 50 visitas registradas con información completa para mostrar en una tabla del dashboard.

#### Respuesta Exitosa (200 OK)
```json
[
  {
    "fecha": "2025-07-24",
    "nombre": "María González",
    "adulto": 1,
    "nino": 0,
    "nacionalidad": "Panamá",
    "motivo_visita": "Turismo recreativo",
    "sendero": "Sendero Las Cruces",
    "hora_entrada": "14:30:25",
    "telefono": "6123-4567"
  },
  {
    "fecha": "2025-07-24",
    "nombre": "Carlos Rodríguez",
    "adulto": 1,
    "nino": 0,
    "nacionalidad": "Costa Rica",
    "motivo_visita": "Investigación científica",
    "sendero": "Sendero El Charco",
    "hora_entrada": "09:15:42",
    "telefono": "6987-6543"
  },
  {
    "fecha": "2025-07-23",
    "nombre": "Ana Martínez",
    "adulto": 0,
    "nino": 1,
    "nacionalidad": "Colombia",
    "motivo_visita": "Visita familiar",
    "sendero": "Sendero La Cascada",
    "hora_entrada": "16:45:12",
    "telefono": "6456-7890"
  }
]
```

#### Campos de Respuesta
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `fecha` | string | Fecha de la visita (YYYY-MM-DD) |
| `nombre` | string | Nombre del visitante (desencriptado) |
| `adulto` | integer | 1 si es adulto, 0 si no |
| `nino` | integer | 1 si es niño, 0 si no |
| `nacionalidad` | string | País de origen (desencriptado) |
| `motivo_visita` | string | Razón de la visita |
| `sendero` | string | Nombre del sendero visitado |
| `hora_entrada` | string | Hora de entrada (HH:MM:SS) |
| `telefono` | string | Teléfono de contacto (desencriptado) |

#### Respuesta de Error (500)
```json
{
  "error": "Error al obtener visitas recientes",
  "detalle": "Descripción técnica del error"
}
```

---

### 2. Visitantes de Hoy
**GET** `/dashboard/visitantes-hoy/`

Retorna el número total de visitantes que han ingresado en el día actual.

#### Respuesta Exitosa (200 OK)
```json
{
  "visitantes_hoy": 15
}
```

#### Campos de Respuesta
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `visitantes_hoy` | integer | Número de visitantes del día actual |

#### Respuesta de Error (500)
```json
{
  "error": "Error al contar visitantes de hoy",
  "detalle": "Descripción técnica del error"
}
```

#### Notas Técnicas
- Utiliza timezone-aware datetime para contar correctamente
- Considera la zona horaria configurada en Django
- Se basa en el campo `fecha_visita` de `RegistroVisita`

---

### 3. Encuestas de Hoy
**GET** `/dashboard/encuestas-hoy/`

Retorna el número de encuestas completadas en el día actual.

#### Respuesta Exitosa (200 OK)
```json
{
  "encuestas_hoy": 8
}
```

#### Campos de Respuesta
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `encuestas_hoy` | integer | Número de encuestas completadas hoy |

#### Respuesta de Error (500)
```json
{
  "error": "Error al contar encuestas de hoy",
  "detalle": "Descripción técnica del error"
}
```

#### Notas Técnicas
- Se basa en la fecha de la visita asociada a cada encuesta
- Filtro: `visita__fecha_visita__date=hoy`

---

### 4. Visitantes por País
**GET** `/dashboard/visitantes-por-pais/`

Retorna estadísticas de visitantes agrupados por nacionalidad, ordenados por cantidad descendente.

#### Respuesta Exitosa (200 OK)
```json
[
  {
    "pais": "Panamá",
    "cantidad": 45
  },
  {
    "pais": "Costa Rica",
    "cantidad": 12  
  },
  {
    "pais": "Colombia",
    "cantidad": 8
  },
  {
    "pais": "Estados Unidos",
    "cantidad": 5
  },
  {
    "pais": "México",
    "cantidad": 3
  },
  {
    "pais": "Brasil",
    "cantidad": 2
  }
]
```

#### Campos de Respuesta
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `pais` | string | Nombre del país/nacionalidad |
| `cantidad` | integer | Número total de visitantes de ese país |

#### Características
- **Ordenamiento:** Por cantidad descendente (mayor a menor)
- **Encriptación:** Los datos se desencriptan automáticamente
- **Cobertura:** Incluye todos los países registrados en el sistema
- **Agrupación:** Basada en el campo `nacionalidad` del modelo `Visitante`

#### Respuesta de Error (500)
```json
{
  "error": "Error al obtener visitantes por país",
  "detalle": "Descripción técnica del error"
}
```

---

### 5. Visitantes por Sendero
**GET** `/dashboard/visitantes-por-sendero/`

Retorna estadísticas de visitantes agrupados por sendero visitado, ordenados por popularidad.

#### Respuesta Exitosa (200 OK)
```json
[
  {
    "sendero": "Sendero Las Cruces",
    "cantidad": 25
  },
  {
    "sendero": "Sendero El Charco", 
    "cantidad": 18
  },
  {
    "sendero": "Sendero La Cascada",
    "cantidad": 12
  },
  {
    "sendero": "Sendero Mirador",
    "cantidad": 8
  },
  {
    "sendero": "Sendero Bosque Húmedo",
    "cantidad": 5
  }
]
```

#### Campos de Respuesta
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `sendero` | string | Nombre del sendero |
| `cantidad` | integer | Número total de visitas a ese sendero |

#### Características
- **Ordenamiento:** Por popularidad descendente (más visitado a menos visitado)
- **Fuente de datos:** Basado en `RegistroVisita.sendero_visitado`
- **Utilidad:** Identificar senderos más populares para gestión y mantenimiento
- **Histórico:** Incluye todas las visitas registradas, no solo del día actual

#### Respuesta de Error (500)
```json
{
  "error": "Error al obtener visitantes por sendero",
  "detalle": "Descripción técnica del error"
}
```
### 6. Reporte Completo en Excel

**GET** `/reporte-excel/`

Genera y descarga un archivo Excel con información detallada del sistema, incluyendo visitantes, visitas, senderos, encuestas y estadísticas relevantes.

#### Descripción

Este endpoint genera un **reporte completo en formato `.xlsx`** estructurado en múltiples hojas, útil para análisis administrativos, presentaciones o respaldo de datos.

#### Hojas del Reporte

| Hoja | Título                | Contenido                                                            |
| ---- | --------------------- | -------------------------------------------------------------------- |
| 1    | Resumen Ejecutivo     | Métricas clave del sistema (visitantes, visitas, encuestas, etc.)    |
| 2    | Visitantes            | Detalles individuales de cada visitante, incluyendo total de visitas |
| 3    | Registro de Visitas   | Historial completo de visitas con fecha, hora y sendero visitado     |
| 4    | Senderos              | Información de senderos, dificultad, visitas y valoración            |
| 5    | Encuestas             | Resumen de encuestas completadas con respuestas truncadas            |
| 6    | Estadísticas por País | Agrupación de visitantes y visitas por nacionalidad                  |
| 7    | Usuarios del Sistema  | Listado de usuarios con información de roles y comentarios           |

#### Parámetros

No requiere parámetros.

#### Respuesta Exitosa (200 OK)

* **Tipo de contenido:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
* **Encabezado:**
  `Content-Disposition: attachment; filename="reporte_completo_centro_visitantes_YYYYMMDD_HHMMSS.xlsx"`

> Se descarga automáticamente un archivo Excel con las hojas detalladas anteriormente.

#### Respuesta de Error (500)

```json
{
  "error": "Error al generar el reporte completo",
  "detalle": "Descripción técnica del error"
}
```

#### Características Técnicas

* Los datos sensibles son desencriptados automáticamente antes de exportarse.
* El archivo se genera en tiempo real, sin almacenarse en disco.
* Las hojas tienen encabezados estilizados y celdas con bordes para una mejor visualización.
* El nombre del archivo incluye la fecha y hora de generación.
---

## 🔧 Códigos de Estado HTTP

| Código | Descripción | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | Solicitud procesada exitosamente |
| 500 | Internal Server Error | Error en el procesamiento de datos o consulta a BD |

---

## ⚠️ Manejo de Errores

### Estructura de Error Estándar
```json
{
  "error": "Descripción general del error",
  "detalle": "Información técnica específica del error"
}
```

### Errores Comunes

#### Error de Base de Datos
```json
{
  "error": "Error al obtener visitas recientes",
  "detalle": "relation 'app_registrovisita' does not exist"
}
```

#### Error de Desencriptación
```json
{
  "error": "Error al obtener visitantes por país", 
  "detalle": "Invalid token or corrupted data"
}
```

#### Error de Configuración
```json
{
  "error": "Error al contar visitantes de hoy",
  "detalle": "timezone settings not configured properly"
}
```

---

## 💡 Notas Técnicas Importantes

### Encriptación de Datos
- Los campos sensibles se desencriptan automáticamente en las respuestas
- La clave de encriptación debe estar configurada en las variables de entorno
- Los datos encriptados incluyen: nombres, teléfonos, cédulas y nacionalidades

### Rendimiento
- **Visitas recientes:** Limitado a 50 registros para optimizar performance
- **Consultas agregadas:** Se procesan en memoria debido a la encriptación
- **Caché:** Considerar implementar caché para consultas frecuentes

### Zona Horaria
- Todas las consultas de "hoy" respetan la configuración de timezone de Django
- Importante configurar correctamente `TIME_ZONE` en settings.py

---

## 🧪 Ejemplos de Prueba en Postman

### Configuración de Variables
```
base_url = http://localhost:8000
```

### Request Headers
```
Content-Type: application/json
Accept: application/json
```


---

**Última actualización:** Julio 2025  
**Versión:** 2.0
