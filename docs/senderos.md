### 🏞️ Senderos API

Endpoints relacionados con la información de senderos turísticos.

---

### 🔸 GET `/api/sendero/<id>/`

**Descripción:** Obtener los detalles de un sendero por ID (no sirve porque esta info se pone directamente en el front).

**Ejemplo:** `/api/sendero/5/`

**Respuesta (200 OK):**
```json
{
  "id": 5,
  "nombre": "Sendero del Jaguar",
  "descripcion": "Sendero con avistamiento de fauna silvestre",
  "longitud": 2.3
}
```

---

### 🔸 GET `/api/senderos/`

**Descripción:** Listar todos los senderos registrados en la base de datos. IMPORTANTE, tienen que decidir el id de cada sendero para crearlos en la bd y al poner id:1 en el front sea el sendero del jaguar y en la bd tambien.

**Respuesta (200 OK):**
```json
[
  {
    "id": 1,
    "nombre": "Sendero del Jaguar",
    "descripcion": "Sendero con avistamiento de fauna silvestre",
    "longitud": 2.3
  },
  {
    "id": 2,
    "nombre": "Sendero del Puma",
    "descripcion": "Sendero de alta dificultad",
    "longitud": 3.5
  }
]
```