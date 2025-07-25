### 📋 Encuestas API

Endpoints para registrar encuestas completadas por visitantes después de su recorrido.

---

### 🔸 POST `/api/encuestas/registrar/`

**Descripción:** Registrar una encuesta vinculada a una visita ya registrada, id_visita es el id de uno de los registros que se hace en la tabla registro_visita(tiene que existir un visitante y que se le haga su registro visita).

**Body esperado (JSON):**
```json
{
  "id_visita": 1, 
  "formulario": {
    "sexo": "Femenino",
    "ocupacion": "Estudiante",
    "estudios": "Universitarios",
    "visita_realiza": "con amigos",
    "actividad_experimentada": "Senderismo",
    "planea_volver": "Sí",
    "porque": "Me encantó el paisaje",
    "como_se_entero": "Redes sociales",
    "me_gusto": "La tranquilidad del lugar",
    "no_me_gusto": "La falta de señalización",
    "recomendaria": "Instalar más mapas",
    "sugerencias": "Agua potable en la entrada"
  }
}
```

**Respuesta (201 Created):**
```json
{
  "mensaje": "Encuesta registrada correctamente"
}
```

**Errores comunes:**
```json
{
  "error": "La visita no existe"
}
```
```json
{
  "error": "Datos incompletos"
}
```