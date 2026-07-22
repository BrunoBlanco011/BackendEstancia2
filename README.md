# Backend de Encuestas (transcriptor-backend)

API REST construida con **FastAPI** para gestionar encuestas: creación de encuestas, preguntas, opciones de respuesta, respuestas de usuarios, subida de archivos y utilidades de procesamiento de lenguaje natural (NLP) sobre texto libre.

## Estado de verificación

Verificado el 2026-07-13 corriendo el servidor localmente contra MySQL local:

| Componente | Estado |
|---|---|
| Dependencias (`requirements.txt`) | ✅ Instaladas, sin conflictos |
| Conexión a MySQL | ✅ OK (pool de conexiones) |
| Esquema de base de datos | ✅ Tablas creadas (`create_tables.sql`) |
| `GET /health` | ✅ 200 |
| Crear usuario / Login (JWT) | ✅ Probado end-to-end |
| Crear encuesta | ✅ Probado end-to-end |
| Extracción de keywords (NLP) | ✅ Probado end-to-end (incluye fix de ranking por frecuencia, ver más abajo) |
| Subida de archivos a Cloudinary | ⚠️ Credenciales configuradas correctamente; la subida en sí no se pudo probar por un error de verificación SSL del entorno de pruebas local (no del código ni de las credenciales) |
| Protección JWT en rutas | ✅ Corregida y enganchada (ver "Autenticación y rutas protegidas") |

## Stack técnico

- **Framework**: FastAPI + Uvicorn
- **Base de datos**: MySQL (vía `mysql-connector-python`, pool de conexiones)
- **Autenticación**: JWT (HS256) con `python-jose`, contraseñas hasheadas con `bcrypt`
- **Almacenamiento de archivos**: Cloudinary (imágenes, documentos, audio, video)
- **NLP**: `nltk` (tokenización, stopwords en español/inglés) para extracción de palabras clave y frases
- **Validación**: Pydantic v2

## Arquitectura

El código sigue **arquitectura hexagonal / clean architecture**, repetida por cada módulo de negocio dentro de `src/<modulo>/`:

```
src/<modulo>/
├── domain/            # Reglas de negocio puras: entidades, DTOs, interfaces de repositorio
│   ├── entities/
│   ├── dto/
│   └── I<Modulo>Repository.py     # Puerto (interfaz) que define qué necesita el dominio
├── application/        # Casos de uso (orquestan el dominio, no saben de HTTP ni de SQL)
│   └── Create/Get/Update/Delete...UseCase.py
└── infrastructure/     # Detalles técnicos: HTTP y persistencia real
    ├── adapters/        # Implementación del repositorio contra MySQL
    ├── controllers/      # Traducen HTTP <-> casos de uso
    ├── routes/            # Definición de rutas FastAPI
    └── dependencies.py     # Wiring: arma controllers con sus casos de uso y repos
```

La idea: el dominio no depende de FastAPI ni de MySQL — solo de sus propias interfaces (`I<Modulo>Repository`). `infrastructure/adapters` es la única capa que sabe hablar SQL, así que en teoría se podría cambiar de MySQL a otra base sin tocar la lógica de negocio.

`main.py` es el punto de entrada: crea la app FastAPI, abre el pool de conexión a MySQL, llama a `init_<modulo>()` de cada módulo (que arma toda la cadena de dependencias) y registra todas las rutas bajo el prefijo `/api`.

## Módulos y modelo de datos

```
users ──< survey ──< questions ──< question_options
  │           │           │              │
  │           └──< responses ──< answers ──< answer_options
  └──< files
```

- **users**: cuentas de la aplicación (nombre, email único, password hasheado, `role_id`, imagen de perfil). *`role_id` es un entero libre — no existe tabla `roles` ni lógica de autorización basada en rol todavía.*
- **survey**: encuestas, cada una asociada a un `created_by` (usuario).
- **questions**: preguntas de una encuesta (`question_type`, si es obligatoria, orden).
- **question_options**: opciones de respuesta para preguntas de tipo selección.
- **responses**: un envío de respuestas a una encuesta (por usuario registrado o por email de invitado).
- **answers**: cada respuesta individual dentro de un `response` (texto libre, opción seleccionada, o valor de escala).
- **answer_options**: para preguntas de selección múltiple, relaciona una respuesta con varias opciones elegidas.
- **files**: metadatos de archivos subidos (el archivo en sí vive en Cloudinary).
- **nlp**: módulo sin persistencia — solo procesa texto que se le manda en el request.

Todas las relaciones tienen `FOREIGN KEY` con `ON DELETE CASCADE`/`RESTRICT`/`SET NULL` según corresponda (ver `create_tables.sql`).

## Autenticación y rutas protegidas

Todas las rutas que requieren token usan `Depends(get_current_user)` (`src/core/security/jwt_middleware.py`), que valida el header `Authorization: Bearer <token>`. Sin token válido responden `401`/`403`.

**🔒 Protegidas** (requieren login):
- Usuarios: `GET/PUT/DELETE /users/{id}`, `GET /users`
- Encuestas: `POST/PUT/DELETE /surveys`, `GET /users/{id}/surveys`
- Preguntas y opciones: creación/edición/borrado (`POST/PUT/DELETE /questions`, `/question-options`)
- Respuestas (regla de negocio: **solo usuarios registrados pueden responder encuestas**): todas las rutas de `/responses`, `/answers`, `/answer-options`
- Archivos: todas las rutas de `/files`
- NLP: `POST /nlp/extract-keywords`, `/nlp/extract-ranked-keywords`, `/nlp/extract-phrases`

**🌐 Públicas** (sin token):
- `POST /users` (registro), `POST /auth/login`
- `GET /health`, `GET /docs`, `GET /nlp/health`
- `GET /surveys` (catálogo público de encuestas), `GET /surveys/{id}`, `GET /surveys/{id}/questions`, `GET /questions/{id}/options` — para poder mostrar una encuesta antes de que el usuario inicie sesión

**Pendiente:** la protección solo verifica que el token sea válido, no que el usuario autenticado sea el dueño del recurso (por ejemplo, cualquier usuario logueado puede borrar la encuesta de otro). Si se necesita, hay que comparar `current_user.user_id` contra `created_by`/`uploaded_by` dentro de cada controller.

## Endpoints

Prefijo común: `/api`

**Usuarios y auth**
- `POST /users` (multipart/form-data: name, lastName, email, password, roleId, profileImage?)
- `GET /users`, `GET /users/{id}`, `PUT /users/{id}`, `DELETE /users/{id}`
- `POST /auth/login` (JSON: email, password) → devuelve JWT

**Encuestas**
- `POST /surveys`, `GET /surveys`, `GET /surveys/{id}`, `GET /users/{id}/surveys`, `PUT /surveys/{id}`, `DELETE /surveys/{id}`

**Preguntas y opciones**
- `POST /questions`, `GET /questions`, `GET /questions/{id}`, `GET /surveys/{id}/questions`, `PUT /questions/{id}`, `DELETE /questions/{id}`
- `POST /question-options`, `GET /question-options`, `GET /question-options/{id}`, `GET /questions/{id}/options`, `PUT /question-options/{id}`, `DELETE /question-options/{id}`

**Respuestas**
- `POST /responses`, `GET /responses`, `GET /responses/{id}`, `GET /surveys/{id}/responses`, `GET /users/{id}/responses`, `DELETE /responses/{id}`
- `POST /answers`, `GET /answers`, `GET /answers/{id}`, `GET /responses/{id}/answers`, `GET /questions/{id}/answers`, `PUT /answers/{id}`, `DELETE /answers/{id}`
- `POST /answer-options`, `GET /answer-options`, `GET /answer-options/{id}`, `GET /answers/{id}/answer-options`, `DELETE /answer-options/{id}`

**Archivos**
- `POST /files`, `GET /files`, `GET /files/{id}`, `GET /users/{id}/files`, `DELETE /files/{id}`

**NLP** (sin persistencia)
- `POST /nlp/extract-keywords`, `POST /nlp/extract-ranked-keywords`, `POST /nlp/extract-phrases`, `GET /nlp/health`

**Otros**
- `GET /health` (fuera del prefijo `/api`)
- `GET /docs` — Swagger UI autogenerado por FastAPI

## Variables de entorno (`.env`)

Ver plantilla completa en [`.env.example`](.env.example). Resumen:

```
DATABASE_URL=mysql://usuario:password@host:puerto/nombre_db
JWT_SECRET=<secreto fuerte, no el default hardcodeado>
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
ALLOWED_ORIGINS=*            # dominios del frontend separados por coma en produccion
HOST=0.0.0.0
PORT=8000
RELOAD=false
```

## Correr localmente

```bash
pip install -r requirements.txt
# Crear la base de datos y tablas:
mysql -u root -p < create_tables.sql
# Configurar .env (ver arriba)
python main.py
# o: uvicorn main:app --reload
```

Servidor en `http://127.0.0.1:8000`, docs interactivas en `/docs`.

## Cosas a revisar antes de producción (Contabo)

1. ✅ `JWT_SECRET` sale del código vía `os.getenv`; solo falta poner un valor random fuerte en el `.env` de producción (ver `.env.example`, incluye el comando para generarlo).
2. ⏳ Completar credenciales de `CLOUDINARY_*` en el `.env` de producción (las de dev ya están en `.env` local, no se suben a git).
3. ✅ `CORS` ahora lee `ALLOWED_ORIGINS` del `.env` (lista separada por coma). Por defecto sigue en `*` — cambiarlo al dominio real del frontend en producción.
4. ✅ `reload=True` ahora depende de la variable `RELOAD` (default `false`). El `Dockerfile` corre `uvicorn` directo sin reload.
5. No hay tabla `roles` ni autorización por rol — `role_id` se guarda pero no se usa para restringir nada. (Pendiente, no bloquea el despliegue.)
6. La protección JWT no valida ownership del recurso (ver sección "Autenticación y rutas protegidas" arriba). (Pendiente, no bloquea el despliegue.)
7. ✅ `spacy` y `scikit-learn` quitados de `requirements.txt` (no se usaban, `nlp` solo usa `nltk`) — imagen Docker más liviana y build más rápido.

## Despliegue en Contabo (Docker + nginx + HTTPS sin dominio propio)

Todo el stack corre en contenedores: la API (`app`), MySQL (`db`), el frontend
(`frontend`, repo aparte), un reverse proxy (`nginx`) y renovación automática de
certificados (`certbot`). Archivos relevantes: [`Dockerfile`](Dockerfile),
[`docker-compose.yml`](docker-compose.yml), [`.env.example`](.env.example),
[`deploy/nginx/templates/app.conf.template`](deploy/nginx/templates/app.conf.template)
y [`deploy/certbot/init-letsencrypt.sh`](deploy/certbot/init-letsencrypt.sh).

**¿Cómo se consigue HTTPS sin tener un dominio propio?** Usando [nip.io](https://nip.io):
un servicio de DNS gratuito que resuelve `<tu-ip>.nip.io` directamente a esa IP, sin
registrar nada. Con eso, Let's Encrypt sí puede emitir un certificado real y válido
(a diferencia de un certificado autofirmado, no muestra advertencias en el navegador).

**¿Y el frontend?** Se sirve desde el mismo dominio y el mismo `nginx`, sin necesidad
de otro dominio ni otro servidor: `nginx` enruta `/api/*` (y `/docs`, `/health`) hacia
`app`, y todo lo demás (`/`) hacia el contenedor `frontend` (una build estática del SPA
servida por su propio nginx interno). Como frontend y API quedan bajo el mismo origen
(`https://<DOMAIN>`), las llamadas del navegador a la API son *same-origin* — no hace
falta configurar CORS para que funcione. El contenedor `frontend` se buildea a partir
del repo `FrontendEstancia2`, que debe estar clonado **al lado** de este (mismo padre),
porque `docker-compose.yml` referencia `../FrontendEstancia2` como build context.

En el VPS (Ubuntu/Debian):

```bash
# 1. Instalar Docker y Docker Compose (si no están)
curl -fsSL https://get.docker.com | sh

# 2. Clonar AMBOS repos, uno al lado del otro
git clone <url-del-repo-backend> backend
git clone <url-del-repo-frontend> FrontendEstancia2
cd backend

# 3. Configurar variables de entorno de producción
cp .env.example .env
nano .env
# completar: JWT_SECRET, CLOUDINARY_*, MYSQL_ROOT_PASSWORD, ALLOWED_ORIGINS,
# LETSENCRYPT_EMAIL y DOMAIN (usa la IP pública del VPS, ej: 203.0.113.42.nip.io)
# DOMAIN se usa tanto para el certificado como para bakear VITE_API_URL del
# frontend en build time (https://<DOMAIN>/api) — no hace falta tocar nada
# en el repo del frontend.

# 4. Abrir los puertos 80 y 443 en el firewall del VPS (si usas ufw)
sudo ufw allow 80,443/tcp

# 5. Levantar la app, la base de datos y el frontend (create_tables.sql se ejecuta
# solo la primera vez)
docker compose up -d --build db app frontend

# 6. Verificar que la API responde internamente
docker compose exec app curl http://127.0.0.1:8000/health

# 7. Emitir el certificado HTTPS (solo la primera vez)
bash deploy/certbot/init-letsencrypt.sh

# 8. Levantar el resto del stack (nginx + renovación automática de certbot)
docker compose up -d
```

A partir de ahí, el frontend queda disponible en `https://<DOMAIN>` y la API en
`https://<DOMAIN>/api` (ej. `https://203.0.113.42.nip.io`). Los puertos 8000 (`app`) y
80 de `frontend` ya no se publican al exterior — solo `nginx` es accesible desde fuera
del VPS, y hace de proxy hacia ambos dentro de la red interna de Docker.
El servicio `certbot` corre en segundo plano y renueva el certificado automáticamente
antes de que expire (cada 12h revisa si toca renovar).

Si en el futuro consigues un dominio propio, solo cambia `DOMAIN` en el `.env`, corre
`docker compose up -d --build frontend` (para rebakear `VITE_API_URL`) y vuelve a
correr `init-letsencrypt.sh` (bórralo antes de `deploy/certbot/conf/live/<dominio-viejo>`
si cambias de dominio).

Para actualizar tras un cambio de código:
- Backend: `git pull && docker compose up -d --build app`
- Frontend: `cd ../FrontendEstancia2 && git pull && cd ../backend && docker compose up -d --build frontend`
