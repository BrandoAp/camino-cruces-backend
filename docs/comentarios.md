### 📝 Comentarios API

Endpoints para crear y listar comentarios relacionados a los senderos. Se puede incluir una imagen opcional y una valoración entre 1 y 5 estrellas.

---

### 🔸 POST `/api/comentarios/agregar/`

**Descripción:** Crear un nuevo comentario para un sendero específico. foto_comentario es opcional.

**Cuerpo de la solicitud (JSON):**
```json
{
  "usuario_id": 3,
  "sendero": 1,
  "comentario": "Excelente experiencia, mucha fauna y muy buen mantenimiento.",
  "valoracion": 5,
  "foto_comentario": null
}
```

---

### 🔸 GET `/api/comentarios/sendero/<int:sendero_id>/`

**Descripción:** Lista los comentarios de un sendero en específico.

**Cuerpo de la solicitud (JSON):**
```json
{
    "usuario": "Samy Caballero",
    "sendero": 1,
    "foto_comentario": null,
    "comentario": "Muy bonito el sendero, bien cuidado.",
    "valoracion": 4
}
```
