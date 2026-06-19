# Arquitectura del Backend

## Framework Principal

FastAPI

## Responsabilidades

* Exposición de endpoints.
* Validación de datos.
* Orquestación de componentes.
* Integración con OpenAI.
* Integración con el Motor Estadístico.

## Módulos Iniciales

api/

Contendrá los endpoints REST.

services/

Contendrá la lógica de negocio.

statistics/

Contendrá los cálculos estadísticos.

ai/

Contendrá la integración con OpenAI.

utils/

Funciones auxiliares.

## Principio de Diseño

Separar claramente:

* Cálculo estadístico.
* Integración IA.
* Exposición de API.

Cada componente debe tener una responsabilidad específica.
