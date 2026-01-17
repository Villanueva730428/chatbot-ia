# agents.md
# Proyecto: Actividad 2 - Chatbot inteligente con Azure OpenAI
# Contexto:
# - Plataforma: Windows
# - IDE: Visual Studio Code
# - Lenguaje: Python
# - Objetivo: Implementar un chatbot funcional que use Azure OpenAI, con bucle interactivo y salida con "salir".
# - Enfoque: Desarrollo incremental (con pruebas en cada paso).
#
# NOTA IMPORTANTE:
# Este archivo guía a Copilot (asistente de código) para construir el proyecto por etapas,
# validando cada componente antes de avanzar al siguiente. Debe mantenerse actualizado conforme evoluciona el proyecto.


## 1) Reglas de nomenclatura y variables (OBLIGATORIO)
# - Usar snake_case para variables, funciones, archivos y módulos.
# - Nombres entendibles, sin abreviaturas:
#   - ✅ conversation_history
#   - ✅ azure_openai_endpoint
#   - ❌ conv_hist
#   - ❌ ep
# - Constantes en MAYÚSCULAS con snake_case:
#   - ✅ DEFAULT_TEMPERATURE
# - Evitar nombres ambiguos como "data", "temp", "obj" si se puede ser específico.


## 2) Arquitectura del proyecto (OBLIGATORIO)
# Mantenerlo simple y práctico. Estructura sugerida:

# /actividad2_chatbot_azure_openai
# ├─ agents.md
# ├─ chatbot.py
# ├─ requirements.txt
# ├─ .env.example
# ├─ .gitignore
# ├─ README.md
# └─ docs/
#    ├─ screenshots/
#    └─ informe.md  (opcional: base del informe para luego exportar a PDF)

# Principios:
# - Un solo archivo ejecutable principal: chatbot.py
# - Configuración por variables de entorno (no hardcodear secretos).
# - Comentarios en el código explicando la funcionalidad (para aprendizaje y auditoría).


## 3) Requisitos funcionales (según enunciado)
# El chatbot debe:
# 1) Configurarse con endpoint y clave API de Azure OpenAI.
# 2) Permitir entrada de texto del usuario en un bucle y responder usando el modelo configurado.
# 3) Terminar la ejecución si el usuario escribe "salir".
# 4) Definir roles: system, user, assistant.
# 5) Permitir personalizar parámetros: temperature, max_tokens, top_p.
#
# Requisitos de calidad:
# - Manejo básico de errores (credenciales faltantes, errores de red, respuesta vacía).
# - No imprimir secretos (API keys) en consola.
# - Salidas legibles y consistentes.


## 4) Configuración (Azure OpenAI) - Variables esperadas
# Usar variables de entorno (ej. en PowerShell o con archivo .env que NO se sube al repo).
#
# Variables sugeridas:
# - AZURE_OPENAI_ENDPOINT         (ej. https://<recurso>.openai.azure.com/)
# - AZURE_OPENAI_API_KEY          (secreto)
# - AZURE_OPENAI_DEPLOYMENT_NAME  (nombre del deployment del modelo en Azure)
# - AZURE_OPENAI_API_VERSION      (ej. 2024-xx-xx)
#
# Nota:
# El nombre de "deployment" en Azure es clave. No asumir que sea el nombre del modelo.


## 5) Estrategia de desarrollo incremental (OBLIGATORIO)
# Regla: NO avanzar de fase si la fase actual no se probó y validó.
#
# FASE 1 - Entorno local
# - Crear venv
# - Instalar openai
# - requirements.txt
# Validación:
# - python --version
# - pip show openai
#
# FASE 2 - Configuración segura
# - Crear .env.example
# - Leer variables de entorno en Python
# Validación:
# - script confirma que variables existen (sin imprimir valores sensibles)
#
# FASE 3 - Chat mínimo funcional
# - chatbot.py con bucle
# - "salir" termina
# - primera llamada a Azure OpenAI
# Validación:
# - conversación simple funciona
#
# FASE 4 - Parámetros (temperature, max_tokens, top_p)
# - Exponer parámetros como constantes o configuración
# - Comentar claramente su efecto
# Validación:
# - cambiar parámetros afecta respuesta
#
# FASE 5 - Pruebas documentadas (3 escenarios)
# - recomendaciones de libros
# - respuestas técnicas
# - generación creativa
# Validación:
# - capturas en docs/screenshots + notas
#
# FASE 6 - Optimización/coste
# - limitar historial
# - controlar max_tokens
# - proponer estrategias
# Validación:
# - sección escrita en docs/informe.md o README
#
# FASE 7 - Entrega
# - README con ejecución
# - base del informe para PDF (mínimo 5 páginas)


## 6) Instrucciones a Copilot (plantillas de prompts por fase)
# NOTA:
# Guillermo (usuario) copiará y pegará estos prompts a Copilot conforme avance.
# Los prompts están diseñados para que Copilot genere código alineado con la rúbrica.

### Prompt Copilot - FASE 1 (Entorno y dependencias)
# "Crea los pasos para Windows/VSCode para:
# 1) crear y activar un entorno virtual en la carpeta del proyecto,
# 2) instalar la librería openai,
# 3) generar requirements.txt,
# 4) proponer un .gitignore básico para Python.
# Mantén los comandos listos para PowerShell."

### Prompt Copilot - FASE 2 (Configuración por variables de entorno)
# "Genera un archivo .env.example con las variables:
# AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_API_VERSION.
# Además, en chatbot.py crea una función load_configuration() que lea estas variables del entorno,
# valide que existan y regrese un diccionario; si falta algo, mostrar un error claro y terminar.
# NO imprimir valores sensibles."

### Prompt Copilot - FASE 3 (Chatbot mínimo funcional)
# "Implementa chatbot.py mínimo funcional:
# - main() con bucle input() para leer al usuario
# - si el usuario escribe 'salir' (ignorando mayúsculas/minúsculas y espacios) termina limpiamente
# - llama a Azure OpenAI para responder usando roles system/user
# - muestra la respuesta del asistente en consola
# Agrega comentarios explicando cada sección del código."

### Prompt Copilot - FASE 4 (Parámetros)
# "Extiende chatbot.py para incluir parámetros configurables:
# DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, DEFAULT_TOP_P.
# Permite ajustar estos parámetros fácilmente y documenta con comentarios qué hace cada uno.
# Agrega validación básica de rangos."

### Prompt Copilot - FASE 5 (Casos de uso)
# "Genera en docs/informe.md una sección 'Pruebas' con 3 escenarios:
# 1) Recomendación de libros
# 2) Respuesta técnica
# 3) Generación creativa
# Incluye una tabla por escenario con: objetivo, prompt, parámetros usados, resultado observado, conclusión.
# Deja espacio para insertar capturas en docs/screenshots/."

### Prompt Copilot - FASE 6 (Optimización y coste)
# "En docs/informe.md agrega sección 'Optimización y costes':
# - explica estrategias para reducir consumo de tokens (limitar historial, resumir contexto, controlar max_tokens)
# - agrega una lista de acciones concretas para este proyecto
# - agrega un checklist final de buenas prácticas."


## 7) Convenciones de comentarios dentro del código (OBLIGATORIO)
# - Cada función debe tener docstring breve.
# - Bloques importantes deben tener comentarios que describan:
#   - Qué hace
#   - Por qué existe
#   - Cómo se prueba
# - Mantener comentarios prácticos (no filosofía).
#
# Ejemplo:
# # Lee la configuración desde variables de entorno.
# # Prueba: borrar AZURE_OPENAI_ENDPOINT y verificar que el programa termina con un mensaje claro.


## 8) Checklist de rúbrica (control interno)
# (1) Configuración correcta del entorno:
# - venv creado y activado
# - openai instalado
# - variables Azure definidas
#
# (2) Implementación técnica:
# - chatbot.py funcional
# - llamadas a Azure OpenAI correctas
# - parámetros configurables
#
# (3) Documentación de pruebas:
# - 3 escenarios
# - capturas + análisis
#
# (4) Optimización de recursos:
# - estimación de costo (calculadora Azure)
# - propuestas para reducir tokens
#
# (5) Formato y claridad:
# - README claro
# - informe con estructura y redacción consistente


## 9) Registro de cambios (CHANGELOG)
# Mantener un resumen corto por versión.
#
# - v0.1: Estructura inicial + venv + dependencias
# - v0.2: Configuración por entorno + validaciones
# - v0.3: Chat mínimo funcional (bucle + salir)
# - v0.4: Parámetros (temperature/max_tokens/top_p)
# - v0.5: Pruebas documentadas (3 escenarios)
# - v0.6: Optimización de tokens/coste + checklist final
