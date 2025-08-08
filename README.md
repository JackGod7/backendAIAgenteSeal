# 🧠 Backend IA - Agente Seal (FastAPI + SQL Server)

Este proyecto es un backend desarrollado en **FastAPI** que permite realizar un CRUD completo sobre una base de datos SQL Server. Integra procesamiento semántico utilizando FAISS para búsquedas vectoriales en los comentarios.

## 📁 Estructura del Proyecto

backendAIAgenteSeal/
│
├── app/
│ ├── main.py # Punto de entrada del backend
│ ├── database.py # Conexión a la base de datos SQL Server
│ ├── models.py # Modelos ORM
│ ├── schemas.py # Esquemas Pydantic (entrada/salida)
│ ├── crud.py # Funciones CRUD
│ ├── config.py # Variables de configuración
│ └── init.py
│
├── .env # Variables de entorno (credenciales)
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo

yaml
Copy
Edit

---

## 🚀 ¿Cómo ejecutar este backend localmente?

### 1. Clonar el repositorio

```bash
git clone https://github.com/JackGod7/backendAIAgenteSeal.git
cd backendAIAgenteSeal
2. Crear entorno virtual (recomendado)
bash
Copy
Edit
python -m venv env
O si usas Conda:

bash
Copy
Edit
conda create -n env_nlp python=3.10.4
conda activate env_nlp
3. Instalar dependencias
bash
Copy
Edit
pip install -r requirements.txt
4. Configurar variables de entorno
Crea un archivo .env con este contenido (rellena tus propios datos):

ini
Copy
Edit
SERVER=your-sqlserver-hostname
DATABASE=your-database-name
USERNAME=your-username
PASSWORD=your-password
PORT=1433
⚠️ Nunca subas tus credenciales reales al repositorio.

5. Ejecutar el backend
bash
Copy
Edit
uvicorn app.main:app --reload
Accede desde el navegador a:

bash
Copy
Edit
http://localhost:8000/docs
Aquí encontrarás la documentación interactiva Swagger generada automáticamente por FastAPI.

🔎 Funcionalidades
✔️ CRUD completo sobre tabla qa_data_model

✔️ Conexión con SQL Server (AWS RDS u on-premise)

✔️ Vectorización semántica con FAISS (próxima etapa)

✔️ API RESTful documentada

✔️ Listo para producción y despliegue futuro en servicios cloud

🧪 Requisitos Previos
Python 3.10.4

Node.js (si deseas conectar con frontend Angular)

SQL Server (en AWS o local)

Git

🧠 Futuro / To-Do
Implementar FAISS para búsquedas semánticas

Dockerización para despliegue más simple

CI/CD con GitHub Actions

Protección con autenticación JWT

Endpoint de salud (/healthcheck)

👨‍💻 Autor
JackGod7 (@JackGod7)

Desarrollador Fullstack / IA / NLP / Energía / Contrataciones Públicas y Privadas