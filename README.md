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

Salida adicional:
- El chatbot muestra una línea de **uso de tokens** por respuesta (si la API lo reporta) y un **resumen de tokens** al final de la sesión.

---

## Tests (pytest)

Con el entorno virtual activo e instaladas las dependencias:

```powershell
pytest
```

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

---

## Mejoras solicitadas 12 febrero 2026

Esta sección documenta las mejoras aplicadas al proyecto para darle una apariencia más profesional al chatbot, sumar un extra de **tracking de tokens** y agregar una base de **tests automatizados**, sin cambiar el objetivo principal del ejercicio (chat de consola con Azure OpenAI).

### 1) Apariencia más profesional en consola

Se mejoró la experiencia de uso en la terminal (CLI) para que sea más clara y “presentable” durante una demostración:

- **Encabezado** con nombre del proyecto y guía de uso (cómo salir con `salir` o `Ctrl+C`).
- Impresión de **parámetros activos** (deployment y valores de `temperature`, `max_tokens`, `top_p`) al iniciar.
- Separadores visuales entre turnos para que se entienda mejor el flujo.
- Etiquetas de salida con color (por ejemplo `Asistente:`) usando `colorama` (ya estaba en dependencias).

Objetivo: que las evidencias/capturas de funcionamiento en consola se vean ordenadas y consistentes.

Evidencias (capturas):

![Mejora del chatbot](docs/Evidencia-Funcionamiento/Mejora%20del%20chatbot.jpg)

![Mejora del chatbot 2](docs/Evidencia-Funcionamiento/Mejora%20del%20chatbot%202.jpg)

### 2) Tracking de tokens (por turno y acumulado)

Se agregó un “extra” para observar consumo de tokens durante la sesión:

- Por cada respuesta, el chatbot intenta leer `response.usage` (si la API lo incluye) y muestra una línea:
   - `prompt`, `completion` y `total`.
- Al finalizar la sesión, muestra un **resumen acumulado** de tokens de toda la conversación.

Notas importantes:

- Si la API/SDK no devuelve el campo `usage`, el chatbot muestra “Tokens: (no disponible)” (esto evita fallos y mantiene el flujo).
- No se imprimen secretos: el tracking solo muestra métricas (tokens), nunca la API key.

### 3) Refactor mínimo para soportar métricas y pruebas

Para mantener el código testeable y con responsabilidades claras, se hicieron cambios puntuales:

- La función de solicitud al modelo ahora retorna un objeto con:
   - `content` (texto del asistente)
   - `token_usage` (si está disponible)
- La carga de configuración (`load_configuration`) permite desactivar la carga de `.env` en tests, evitando dependencias del entorno local durante la ejecución de `pytest`.

### 4) Tests automatizados (pytest)

Se añadió una suite de pruebas unitarias para validar piezas clave sin llamar a Azure (no hay costos ni dependencia de red):

- Normalización del input (por ejemplo `salir` con espacios/mayúsculas).
- Validación de rangos para `temperature`, `max_tokens` y `top_p`.
- Validación de configuración (falta de variables requeridas y normalización del endpoint).
- Extracción y acumulación de métricas de tokens (sin usar el cliente real).

Ejecución:

```powershell
pytest
```

Extracto del código de tests (pytest):

Este fragmento ejemplifica cómo se valida:

- Normalización de comandos de usuario (por ejemplo `salir`).
- Rangos válidos e inválidos de parámetros (`temperature`, `max_tokens`, `top_p`).

```python
import types

import pytest

import chatbot


def test_normalize_user_input_strips_and_lowercases() -> None:
    assert chatbot.normalize_user_input("  SaLiR  ") == "salir"


def test_validate_generation_parameters_accepts_valid() -> None:
    chatbot.validate_generation_parameters(temperature=0.0, max_tokens=1, top_p=1.0)
    chatbot.validate_generation_parameters(temperature=2.0, max_tokens=999, top_p=0.0)


@pytest.mark.parametrize(
    "temperature,max_tokens,top_p",
    [
        (-0.1, 10, 1.0),
        (2.1, 10, 1.0),
        (0.5, 0, 1.0),
        (0.5, -1, 1.0),
        (0.5, 10, -0.01),
        (0.5, 10, 1.01),
    ],
)
def test_validate_generation_parameters_rejects_invalid(
    temperature: float, max_tokens: int, top_p: float
) -> None:
    with pytest.raises(ValueError):
        chatbot.validate_generation_parameters(
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
```

### 5) Dependencias actualizadas

- Se agregó `pytest` a `requirements.txt` para que correr tests sea reproducible.

Resultado: el proyecto mantiene el comportamiento solicitado en el enunciado (bucle + `salir` + roles + parámetros), y además ahora cuenta con una presentación más profesional, métricas de tokens y una base de tests para evidenciar calidad.
