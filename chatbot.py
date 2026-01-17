r"""Chatbot con Azure OpenAI (Actividad 2).

FASE 2: configuración segura por variables de entorno.
- Lee endpoint, api key, deployment y api version desde el entorno.
- Valida que existan.
- NO imprime valores sensibles (como la API key).

FASE 3: chat mínimo funcional.
- Bucle interactivo con input().
- Si el usuario escribe 'salir' (ignorando mayúsculas/minúsculas y espacios) termina.
- Llama a Azure OpenAI para responder usando roles: system/user/assistant.

Prueba rápida (PowerShell):
- Activar venv: `\.\.venv\Scripts\Activate.ps1`
- Definir variables (reales): `$Env:AZURE_OPENAI_ENDPOINT=...` etc.
- Ejecutar: `python chatbot.py`

Opción 3 (recomendado): archivo .env
- Copia .env.example a .env y completa los valores reales.
- El programa carga .env automáticamente (sin imprimir secretos).
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List

import openai
from openai import AzureOpenAI
from dotenv import load_dotenv


REQUIRED_ENV_VARS = (
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_DEPLOYMENT_NAME",
    "AZURE_OPENAI_API_VERSION",
)


# Parámetros de generación (FASE 4)
# Ajusta estos valores para controlar el estilo y coste (tokens) de las respuestas.
# - temperature: 0.0 a 2.0 (más alto = más creatividad/variación)
# - top_p: 0.0 a 1.0 (muestreo nucleus; alternativa/complemento a temperature)
# - max_tokens: límite de tokens de salida (más bajo = menor coste y respuestas más cortas)
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 300
DEFAULT_TOP_P = 1.0


SYSTEM_PROMPT = (
    "Eres un asistente útil y claro. Responde en español y de forma concisa, "
    "y si falta información pide una aclaración."
)


def load_configuration() -> Dict[str, str]:
    """Lee y valida la configuración desde variables de entorno.

    Returns:
        Dict[str, str]: Diccionario con la configuración necesaria para Azure OpenAI.

    Side effects:
        - Si falta alguna variable requerida, imprime un error claro y termina el programa.

    Prueba:
        - Borra AZURE_OPENAI_ENDPOINT del entorno y ejecuta `python chatbot.py`.
          Debe finalizar con un mensaje que indique cuál variable falta.
    """

    # Carga variables desde un archivo .env local (si existe).
    # - override=False: si ya tienes variables definidas en el sistema, tienen prioridad.
    # Prueba: crea .env con las variables y ejecuta `python chatbot.py`.
    load_dotenv(override=False)

    configuration: Dict[str, str] = {}
    missing_variables = []

    for variable_name in REQUIRED_ENV_VARS:
        raw_value = os.getenv(variable_name)
        value = raw_value.strip() if raw_value is not None else ""

        if not value:
            missing_variables.append(variable_name)
            continue

        configuration[variable_name] = value

    if missing_variables:
        missing_list = ", ".join(missing_variables)
        print(
            "Error: faltan variables de entorno requeridas: " + missing_list,
            file=sys.stderr,
        )
        print(
            "Solución: define las variables en tu sistema o crea un archivo .env basado en .env.example.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    # Normalización ligera (no sensible): asegurar que el endpoint termine con '/'
    endpoint = configuration["AZURE_OPENAI_ENDPOINT"]
    if not endpoint.endswith("/"):
        configuration["AZURE_OPENAI_ENDPOINT"] = endpoint + "/"

    return {
        "azure_openai_endpoint": configuration["AZURE_OPENAI_ENDPOINT"],
        "azure_openai_api_key": configuration["AZURE_OPENAI_API_KEY"],
        "azure_openai_deployment_name": configuration["AZURE_OPENAI_DEPLOYMENT_NAME"],
        "azure_openai_api_version": configuration["AZURE_OPENAI_API_VERSION"],
    }


def create_azure_openai_client(configuration: Dict[str, str]) -> AzureOpenAI:
    """Crea el cliente de Azure OpenAI a partir de la configuración validada.

    Prueba:
        - Con variables definidas, ejecutar el programa y enviar un mensaje.
    """

    return AzureOpenAI(
        api_key=configuration["azure_openai_api_key"],
        azure_endpoint=configuration["azure_openai_endpoint"],
        api_version=configuration["azure_openai_api_version"],
    )


def normalize_user_input(user_input: str) -> str:
    """Normaliza la entrada del usuario para comandos como 'salir'."""

    return user_input.strip().lower()


def validate_generation_parameters(
    temperature: float,
    max_tokens: int,
    top_p: float,
) -> None:
    """Valida rangos básicos de parámetros de generación.

    Prueba:
        - Cambia DEFAULT_TEMPERATURE a 3.0 y ejecuta: debe fallar con error claro.
    """

    if not (0.0 <= temperature <= 2.0):
        raise ValueError("temperature debe estar entre 0.0 y 2.0")

    if not (0.0 <= top_p <= 1.0):
        raise ValueError("top_p debe estar entre 0.0 y 1.0")

    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens debe ser un entero mayor a 0")


def load_generation_parameters() -> Dict[str, float | int]:
    """Carga parámetros de generación desde constantes y valida rangos.

    Nota:
        - En este proyecto se exponen como constantes para que sea fácil modificarlos.
    """

    validate_generation_parameters(
        temperature=float(DEFAULT_TEMPERATURE),
        max_tokens=int(DEFAULT_MAX_TOKENS),
        top_p=float(DEFAULT_TOP_P),
    )

    return {
        "temperature": float(DEFAULT_TEMPERATURE),
        "max_tokens": int(DEFAULT_MAX_TOKENS),
        "top_p": float(DEFAULT_TOP_P),
    }


def request_assistant_reply(
    client: AzureOpenAI,
    configuration: Dict[str, str],
    conversation_history: List[Dict[str, str]],
    generation_parameters: Dict[str, float | int],
) -> str:
    """Solicita una respuesta del asistente a Azure OpenAI.

    - Incluye siempre el rol system.
    - Envía el historial para mantener contexto.

    Manejo de errores:
        - Errores de red, autenticación o cuota se reportan con un mensaje legible.
    """

    messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(conversation_history)

    response = client.chat.completions.create(
        model=configuration["azure_openai_deployment_name"],
        messages=messages,
        temperature=float(generation_parameters["temperature"]),
        top_p=float(generation_parameters["top_p"]),
        max_tokens=int(generation_parameters["max_tokens"]),
    )

    content = (response.choices[0].message.content or "").strip() if response.choices else ""
    if not content:
        raise ValueError("Respuesta vacía del modelo.")

    return content


def run_chat_loop() -> None:
    """Ejecuta el bucle interactivo del chatbot.

    Prueba:
        - Escribe un saludo y verifica respuesta.
        - Escribe 'salir' y verifica que termina limpiamente.
    """

    configuration = load_configuration()
    client = create_azure_openai_client(configuration)
    generation_parameters = load_generation_parameters()

    conversation_history: List[Dict[str, str]] = []

    print("Chat iniciado. Escribe tu mensaje (o 'salir' para terminar).")

    while True:
        try:
            user_input = input("Tú: ")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if normalize_user_input(user_input) == "salir":
            print("Saliendo...")
            break

        if not user_input.strip():
            continue

        conversation_history.append({"role": "user", "content": user_input.strip()})

        try:
            assistant_reply = request_assistant_reply(
                client=client,
                configuration=configuration,
                conversation_history=conversation_history,
                generation_parameters=generation_parameters,
            )
        except (openai.OpenAIError, ValueError) as error:
            print("Error al contactar Azure OpenAI:", str(error), file=sys.stderr)
            print(
                "Sugerencia: revisa endpoint/deployment/api_version y conectividad. No se imprimen secretos.",
                file=sys.stderr,
            )
            continue

        conversation_history.append({"role": "assistant", "content": assistant_reply})
        print("Asistente:", assistant_reply)


def main() -> None:
    """Punto de entrada del script (FASE 3)."""

    run_chat_loop()


if __name__ == "__main__":
    main()
