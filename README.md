# Actividad 2 — Chatbot inteligente con Azure OpenAI (Python)

Chatbot de consola en Python que se conecta a **Azure OpenAI**, mantiene contexto con historial de conversación y finaliza al escribir **"salir"**.

- Plataforma: Windows
- IDE sugerido: Visual Studio Code
- Configuración: variables de entorno (recomendado vía archivo `.env`)

---

## Arquitectura del proyecto

Estructura simple (un ejecutable principal):

```
.
├─ agents.md
├─ chatbot.py
├─ requirements.txt
├─ .env.example
├─ .env               # local (NO subir al repo)
├─ .gitignore
└─ docs/
   └─ Evidencia-Funcionamiento/
```

Principios:
- Un solo punto de entrada: `chatbot.py`
- No hardcodear secretos (API keys)
- Manejo básico de errores y salidas claras

---

## Fases (desarrollo incremental)

Este proyecto se construye por fases (ver guía en agents.md):

- FASE 1: entorno local (`.venv`, dependencias, `requirements.txt`, `.gitignore`)
- FASE 2: configuración segura (variables de entorno / `.env`)
- FASE 3: chat mínimo funcional (bucle + salida con "salir" + llamada a Azure OpenAI)
- FASE 4: parámetros configurables (`temperature`, `max_tokens`, `top_p`) + validación
- FASE 5: pruebas documentadas (3 escenarios + capturas)
- FASE 6: optimización y coste (estrategias para reducir tokens)
- FASE 7: entrega (README final + informe)

Actualmente el repo implementa hasta **FASE 4**.

---

## Requisitos

- Python 3.12+ (recomendado)
- Cuenta de Azure con acceso a Azure OpenAI
- Un **deployment** creado en tu recurso de Azure OpenAI

---

## Instalación (Windows / PowerShell)

1) Crear y activar entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea scripts, permite solo en esta sesión:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuración de Azure (crear deployment)

1) En Azure Portal, entra a tu recurso **Azure OpenAI**.
2) Abre **Azure AI Foundry / Studio**.
3) Ve a **Deployments** → **Create deployment**.
4) Elige un modelo (chat) disponible y asigna un nombre (por ejemplo `chatbot-gpt`).

Ese nombre es el valor de `AZURE_OPENAI_DEPLOYMENT_NAME`.

---

## Configuración local con `.env` (recomendado)

- `.env.example` es una **plantilla** (sin secretos).
- `.env` contiene **tus valores reales** (secreto) y **NO debe subirse**.

1) Copia `.env.example` a `.env` (ya puede existir en tu carpeta)
2) Edita `.env` y completa:

- `AZURE_OPENAI_ENDPOINT` = `https://<tu-recurso>.openai.azure.com/`
- `AZURE_OPENAI_API_KEY` = tu API Key
- `AZURE_OPENAI_DEPLOYMENT_NAME` = nombre exacto del deployment
- `AZURE_OPENAI_API_VERSION` = versión de API (la de tu recurso/ejemplo en Studio)

Nota: el programa carga `.env` automáticamente usando `python-dotenv`.

---

## Ejecución

Con el entorno virtual activo:

```powershell
python chatbot.py
```

Uso:
- Escribe mensajes después de `Tú:`
- Para terminar: escribe `salir`

---

## Roles (system / user / assistant)

El chatbot envía mensajes a Azure OpenAI usando roles:

- `system`: instrucciones globales del asistente (variable `SYSTEM_PROMPT`)
- `user`: cada entrada del usuario
- `assistant`: cada respuesta del modelo

En el código:
- El rol `system` se agrega siempre al inicio de `messages`.
- El historial (`conversation_history`) alterna `user` y `assistant` para mantener contexto.

---

## Parámetros (temperature / max_tokens / top_p)

En `chatbot.py` se exponen como constantes para ajustar fácilmente:

- `DEFAULT_TEMPERATURE`: controla creatividad/variación (rango 0.0–2.0)
- `DEFAULT_MAX_TOKENS`: límite de tokens de salida (entero > 0)
- `DEFAULT_TOP_P`: muestreo nucleus (rango 0.0–1.0)

El programa valida rangos antes de llamar al modelo.

---

## Evidencias (capturas de funcionamiento)

Todas las capturas del proyecto se guardan en `docs/Evidencia-Funcionamiento/` y se incluyen aquí con una breve explicación.

### Configuración

**Variables de entorno**

Muestra las variables requeridas (endpoint, api key, deployment y api version) y/o cómo se cargan desde `.env`.

![Variables de entorno](docs/Evidencia-Funcionamiento/Variables%20de%20entorno.jpg)

**Configuración en Azure**

Evidencia de la creación/selección del deployment en Azure AI Foundry/Studio (o pantalla equivalente en Azure Portal).

![Configuración Azure](docs/Evidencia-Funcionamiento/Configuraci%C3%B3nAzure.jpg)

### Diseño de conversación (roles y parámetros)

**Definición de roles**

Evidencia de que el chatbot usa roles `system`, `user` y `assistant`.

![Definición del rol](docs/Evidencia-Funcionamiento/Definicion%20del%20rol.jpg)

**Definición de parámetros**

Evidencia de que el chatbot permite personalizar `temperature`, `max_tokens` y `top_p`.

![Definición de parámetros](docs/Evidencia-Funcionamiento/Definici%C3%B3n%20de%20parametros.jpg)

### Funcionamiento (conversaciones)

**Ejemplo 1: Universidades en línea**

Muestra una conversación real en consola con respuesta del asistente.

![Funcionamiento - Universidades en línea](docs/Evidencia-Funcionamiento/Funcionamiento%20-%20Universidades%20en%20l%C3%ADnea.jpg)

**Ejemplo 2: Lugares vacacionales**

Muestra una conversación creativa o de recomendación.

![Lugares vacacionales](docs/Evidencia-Funcionamiento/Lugares%20vacacionales.jpg)

**Ejemplo 3: Pregunta sobre UNIR**

Muestra una conversación informativa/técnica.

![Pregunta sobre UNIR](docs/Evidencia-Funcionamiento/Pregunta%20sobre%20UNIR.jpg)

**Salida del chatbot**

Evidencia del cierre limpio al escribir `salir`.

![Salida del chatbot](docs/Evidencia-Funcionamiento/Salida%20del%20chatbot.jpg)

---

## Reglas del proyecto (según agents.md)

- Usar `snake_case` en variables/funciones/módulos.
- Constantes en MAYÚSCULAS con snake_case (ej. `DEFAULT_TEMPERATURE`).
- No imprimir secretos en consola (por ejemplo `AZURE_OPENAI_API_KEY`).
- Manejo básico de errores: credenciales faltantes, errores de red, respuesta vacía.
- Desarrollo incremental: no avanzar de fase sin validar la anterior.

---

## Solución de problemas

### Error 404: `Resource not found`
Suele indicar que uno de estos valores no coincide:
- `AZURE_OPENAI_DEPLOYMENT_NAME` (nombre del deployment incorrecto)
- `AZURE_OPENAI_ENDPOINT` (endpoint incorrecto del recurso)
- `AZURE_OPENAI_API_VERSION` (versión no soportada)

Recomendación: copia `endpoint`, `api-version` y el nombre del deployment desde Azure AI Foundry/Studio.

### PowerShell no deja activar el venv
Ejecuta (solo en esta terminal):

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\.venv\Scripts\Activate.ps1
```

---

## Costos y optimización

### Herramientas para ver/estimar costos

- **Azure Pricing Calculator**: estimación de costo por modelo/tokens antes de usarlo.
- **Cost Management + Billing**: gasto real por día/servicio, presupuestos y alertas.
- **Azure OpenAI Quotas / Usage** (en el recurso o en Azure AI Foundry/Studio): límites, consumo y posibles bloqueos por cuota.
- **Azure Monitor / Logs (opcional)**: correlación entre volumen de llamadas y gasto (útil si habilitas diagnostic settings).

### Recomendaciones para ahorrar costos (tokens)

- **Limitar historial**: conserva solo los últimos N turnos (por ejemplo 6–10) en `conversation_history`.
- **Resumir contexto**: cuando el historial crezca, reemplaza turnos antiguos por un resumen breve.
- **Controlar `max_tokens`**: es la palanca más directa de coste; usa el mínimo que cumpla el objetivo.
- **No duplicar información**: evita repetir instrucciones largas; ponlas en `SYSTEM_PROMPT` una sola vez.
- **Prompts concisos**: pide respuestas cortas cuando aplique (ej. “responde en 5 líneas”).
- **Temperatura moderada**: en tareas deterministas, usa `temperature` baja para reducir variación y reintentos.
- **Evitar llamadas innecesarias**: valida inputs vacíos y agrega confirmaciones antes de tareas largas.
- **Caching (si aplica)**: si haces consultas repetidas, cachea respuestas localmente.

### Regla práctica

El costo depende del total de tokens: **tokens de entrada (prompt + historial)** + **tokens de salida (respuesta)**. Reducir historial y `max_tokens` suele tener el mayor impacto.

---

## Licencia

Uso académico (Actividad 2). Ajusta esta sección si tu institución lo requiere.
