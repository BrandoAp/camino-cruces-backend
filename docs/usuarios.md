### 👤 Usuarios API

Endpoints para registro, autenticación y consulta de usuarios.

---

### 🔸 POST `/api/registro/`

**Descripción:** Registrar un nuevo usuario.

**Body esperado (JSON):**
```json
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juanperez@mail.com",
  "contraseña": "123456"
}
```

**Respuesta (201 Created):**
```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juanperez@mail.com",
  "rol": "USER"
}
```

---

### 🔸 GET `/api/usuario/<id>/`

**Descripción:** Obtener los datos de un usuario por su ID.

**Ejemplo:** `/api/usuario/1/`

**Respuesta (200 OK):**
```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juanperez@mail.com",
  "rol": "USER"
}
```

---

### 🔸 POST `/api/login/`

**Descripción:** Autenticación del usuario y generación de token JWT.

**Body esperado (JSON):**
```json
{
  "email": "juanperez@mail.com",
  "contraseña": "123456"
}
```

**Respuesta (200 OK):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJh... (JWT)",
  "nombre": "Juan",
  "apellido": "Pérez",
  "rol": "USER",
  "id": 1
}
```

**Errores comunes:**
```json
{
  "detail": "Usuario no encontrado"
}
```
```json
{
  "detail": "Contraseña incorrecta"
}
```