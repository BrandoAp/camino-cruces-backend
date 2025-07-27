# Registro de Visitas - Parque Nacional Camino de Cruces

## 📝 Endpoints de Registro de Visitas

### 1. Registrar Visitante Nuevo y su Visita

**POST** `/api/registrar_visitante_y_visita/`

Registra un nuevo visitante junto con su primera visita al parque. Los datos sensibles del visitante se guardan cifrados.

#### Cuerpo de Petición (JSON)

```json
{
  "cedula_pasaporte": "A123456789",
  "nombre_visitante": "Ana Ruiz",
  "nacionalidad": "Panameña",
  "adulto_nino": "Adulto",
  "telefono": "60000000",
  "genero": "Femenino",
  "razon_visita": "Turismo ecológico",
  "sendero_visitado": "Sendero Las Cruces"
}
```

#### Respuesta Exitosa (201 Created)

```json
{
  "mensaje": "Visitante y visita registrados correctamente."
}
```

---

### 2. Registrar Visita para Visitante Existente

**POST** `api/registro-visita/`

Registra una nueva visita para un visitante previamente registrado en el sistema.

#### Cuerpo de Petición (JSON)

```json
{
  "cedula_pasaporte": "A123456789",
  "razon_visita": "Educativo",
  "sendero_visitado": "Sendero El Charco"
}
```

#### Respuesta Exitosa (201 Created)

```json
{
  "mensaje": "Visita registrada correctamente."
}
```

---

### 3. Registrar Visita por ID de Visitante

**POST** `/api/registrar-visita-id/`

Registra una visita utilizando el `id` interno del visitante en la base de datos.

#### Cuerpo de Petición (JSON)

```json
{
  "visitante_id": 3,
  "razon_visita": "Investigación científica",
  "sendero_visitado": "Sendero Mirador"
}
```

#### Respuesta Exitosa (201 Created)

```json
{
  "mensaje": "Visita registrada correctamente."
}
```

---

### 4. Consultar Nombre del Visitante

**GET** `/api/visitante/cedula/A123456789/`

Devuelve el visitante completo correspondiente a la cédula proporcionada.

#### Respuesta Exitosa (200 OK)

```json
{
  "id": 3,
  "cedula_pasaporte": "A123456789",
  "nombre_visitante": "Ana Ruiz",
  "nacionalidad": "Panameña",
  "adulto_nino": "Adulto",
  "telefono": "60000000",
  "genero": "Femenino"
}
```

---

## 🔧 Notas Técnicas Importantes

- Los campos sensibles como nombre, cédula, nacionalidad y teléfono se almacenan cifrados usando Fernet.
- `fecha_visita` y `hora_entrada` se generan automáticamente.
- El sistema permite múltiples visitas por visitante.
- Todos los errores siguen la estructura estándar:

```json
{
  "detail": "Descripción del error"
}
```

---

**Última actualización:** Julio 2025  
**Versión:** 1.1