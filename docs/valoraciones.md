### ⭐ Valoraciones API

Endpoints para crear y listar comentarios relacionados a los senderos. Se puede incluir una imagen opcional y una valoración entre 1 y 5 estrellas.

---

### 🔸 GET `api/valoracion-promedio/<int:sendero_id>/`

**Descripción:** Obtiene el promedio valorado de cada sendero.

**Cuerpo de la solicitud (JSON):**
```json
{
    "sendero_id": 1,
    "valoracion_promedio": 2.7
}
```

---

### 🔸 GET `/api/comentarios/<int:sendero_id>/valoraciones/`

**Descripción:** Lista los comentarios, con su usuario y sus debidas valoraciones, de cada sendero.

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
