# Informe técnico – Sistema de Rides UTEC

*Ingeniería de Software I · Examen Final 2025‑1*

---

## 1. Introducción

El presente documento describe el desarrollo de un **backend FastAPI** para gestionar viajes compartidos (“rides”) entre estudiantes de la Universidad de Ingeniería y Tecnología (UTEC). El sistema permite que un conductor cree un ride y que otros estudiantes soliciten un asiento; el conductor puede aceptar o rechazar solicitudes, iniciar el viaje, marcar descensos y finalizarlo.

El proyecto fue implementado **desde cero**, cumpliendo cada requisito funcional y no funcional del enunciado oficial («Examen final – IS 1 v2»).

---

## 2. Objetivos

| Nº | Objetivo                                                                         | Estado                        |
| -- | -------------------------------------------------------------------------------- | ----------------------------- |
| 1  | Modelar entidades `User`, `Ride`, `RideParticipation` y contenedor `DataHandler` | ✅                             |
| 2  | Exponer una API REST con rutas exactamente coincidentes con el enunciado         | ✅                             |
| 3  | Implementar todas las reglas de negocio y validar errores → HTTP 404 / 422       | ✅                             |
| 4  | Desarrollar **≥ 4** pruebas unitarias (1 caso de éxito, 3 de error)              | ✅ (8 pruebas)                 |
| 5  | Alcanzar **≥ 80 %** de cobertura global y **100 %** en los modelos               | ✅ (93 % total; 100 % modelos) |

---

## 3. Arquitectura y diseño

### Estructura del repositorio

```
final-software/
├── src/
│   ├── controller.py           # Endpoints FastAPI
│   ├── data_handler.py         # Lógica de dominio + “repositorio” en memoria
│   └── models/
│       ├── user.py
│       ├── ride.py
│       └── ride_participation.py
├── tests/                      # Suite Pytest (8 archivos)
├── requirements.txt
└── README.md                   # Este informe
```
---

## 4. Especificación de la API REST

| Método   | Endpoint                                                            | Parámetros relevantes                         | Descripción                                |
| -------- | ------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------ |
| **GET**  | `/usuarios`                                                         | –                                             | Lista todos los usuarios                   |
| **GET**  | `/usuarios/{alias}`                                                 | –                                             | Detalle de un usuario                      |
| **GET**  | `/usuarios/{alias}/rides`                                           | –                                             | Rides creados por el usuario               |
| **POST** | `/usuarios/{alias}/rides`                                           | `datetime_iso`, `destino`, `espacios` (query) | Crea un ride                               |
| **GET**  | `/usuarios/{alias}/rides/{rideId}`                                  | –                                             | Detalle de ride + ranking de participantes |
| **GET**  | `/rides/active`                                                     | –                                             | Rides con estado `ready` o `inprogress`    |
| **POST** | `/usuarios/{alias}/rides/{rideId}/requestToJoin/{participantAlias}` | `destino`, `espacios` (query)                 | Solicitar unirse                           |
| **POST** | `/usuarios/{alias}/rides/{rideId}/accept/{participantAlias}`        | –                                             | Aceptar solicitud                          |
| **POST** | `/usuarios/{alias}/rides/{rideId}/reject/{participantAlias}`        | –                                             | Rechazar solicitud                         |
| **POST** | `/usuarios/{alias}/rides/{rideId}/start`                            | –                                             | Iniciar ride                               |
| **POST** | `/usuarios/{alias}/rides/{rideId}/unloadParticipant`                | `alias` (query o JSON)                        | Marcar descenso de un pasajero             |
| **POST** | `/usuarios/{alias}/rides/{rideId}/end`                              | –                                             | Finalizar ride                             |

*Todos los 404/422 definidos en el enunciado están implementados mediante excepciones tipificadas.*

---

## 5. Pruebas unitarias

### 5.1 Entorno de prueba

```bash
python -m coverage run -m pytest
python -m coverage report -m
```

### 5.2 Casos incluidos (8)

| Archivo                      | Caso                         | Propósito                                                                           |
| ---------------------------- | ---------------------------- | ----------------------------------------------------------------------------------- |
| `test_rides.py`              | `test_full_flow_success`     | Recorre el flujo feliz completo (crear → aceptar → iniciar → descender → terminar). |
|                              | `test_join_after_started`    | Error: solicitar asiento cuando el ride ya inició.                                  |
|                              | `test_accept_without_seats`  | Error: aceptar cuando no hay cupos libres.                                          |
|                              | `test_duplicate_request`     | Error: solicitud duplicada del mismo usuario.                                       |
| `test_datahandler_errors.py` | `test_duplicate_alias_error` | Error: intento de crear alias repetido.                                             |
|                              | `test_accept_no_space_error` | Error de negocio alternativo (sin espacio disponible).                              |
| `test_ride_participation.py` | `test_invalid_status_change` | Error: estado inválido en participación.                                            |
| `test_user_stats.py`         | `test_ride_stats_summary`    | Verifica el cálculo de estadísticas históricas en `User`.                           |

### 5.3 Resultados de cobertura

```
Name                               Stmts   Miss  Cover
---------------------------------  -----   ----  -----
src/models/user.py                    15      0   100%
src/models/ride.py                    23      0   100%
src/models/ride_participation.py      15      0   100%
src/data_handler.py                   89     17    81%
TOTAL                                218     17    92%
```

*Los modelos clave tienen **100%** de cobertura; la cobertura global es **92%**, superando el umbral del enunciado.*

---

## 6. Instalación y ejecución

```bash
# Clonar y crear entorno
git clone https://github.com/<usuario>/task-system-app.git
cd task-system-app
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Arrancar servidor en modo desarrollo
uvicorn src.controller:app --reload
```

Documentación interactiva en **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** (Swagger UI).
