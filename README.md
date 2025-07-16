
## 📌 Caso de Estudio: Sistema de Gestión de Rides en UTEC

Se desarrolló una aplicación para gestionar “rides” ofrecidos por estudiantes con auto, permitiendo a otros unirse si coinciden en el camino.

---

## 🐱 Integrantes

- Bianca Brunella Aguinaga Pizarro
- Ariana Valeria Mercado Barbieri

---

## 🚀 Funcionalidades del sistema

### Usuarios
- `GET /usuarios`: Lista de usuarios
- `GET /usuarios/{alias}`: Datos de un usuario

### Rides
- `GET /usuarios/{alias}/rides`: Lista de rides creados por un usuario
- `GET /usuarios/{alias}/rides/{rideid}`: Detalles del ride (participantes, estadísticas)

### Acciones en Rides
- `POST /usuarios/{alias}/rides/{rideid}/requestToJoin/{alias}`: Solicitar unirse a un ride
- `POST /usuarios/{alias}/rides/{rideid}/accept/{alias}`: Aceptar solicitud
- `POST /usuarios/{alias}/rides/{rideid}/reject/{alias}`: Rechazar solicitud
- `POST /usuarios/{alias}/rides/{rideid}/start`: Iniciar ride
- `POST /usuarios/{alias}/rides/{rideid}/end`: Terminar ride
- `POST /usuarios/{alias}/rides/{rideid}/unloadParticipant`: Marcar bajada de ride

---

## ✅ Validaciones importantes

- Solo se puede unir a rides en estado `ready`
- Solo se puede iniciar rides si todas las solicitudes están en `rejected` o `confirmed`
- No se puede aceptar más solicitudes que la cantidad de asientos disponibles
- Al iniciar ride, participantes no presentes se marcan como `missing`
- Al finalizar el ride, los participantes en estado `inprogress` se marcan como `notmarked`

---

## 🧪 Pruebas Unitarias

Se desarrollaron 4 pruebas unitarias:
- 1 caso de éxito
- 3 casos de error (validaciones)

Las pruebas están comentadas y se ejecutaron con cobertura al 100% en las clases:
- `Usuario`
- `Ride`
- `RideParticipant`

```bash
python3 -m coverage run
python3 -m coverage report
```