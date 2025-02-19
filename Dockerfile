FROM python:3.12-slim

WORKDIR /app

# Installation des dépendances système nécessaires pour PyQt5
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xinerama0 \
    libxcb-xfixes0 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Création du fichier requirements.txt avec les versions spécifiées
RUN echo "openai>=1.0.0\n\
nicegui>=1.2.0\n\
PyQt5>=5.15.0\n\
pydantic>=2.10.6\n\
uvicorn>=0.34.0\n\
fastapi>=0.115.8\n\
click>=8.1.8\n\
slowapi>=0.1.9\n\
tiktoken>=0.8.0\n\
dnspython>=2.7.0\n\
email-validator>=2.2.0\n\
llama_index==0.12.*\n\
pytest>=7.0.0\n\
flake8>=6.0.0" > requirements.txt

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code de l'application
COPY . .

# Ajout du répertoire courant au PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Port exposé par NiceGUI
EXPOSE 8080

# Variables d'environnement
ENV NICEGUI_HOST=0.0.0.0
ENV QT_QPA_PLATFORM=offscreen
ENV PYTHONUNBUFFERED=1

# Commande de démarrage
CMD ["python3", "main.py"]