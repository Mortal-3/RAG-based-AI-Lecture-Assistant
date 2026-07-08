FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY aienv/ ./aienv/
COPY videos/ ./videos/
COPY audios/ ./audios/
COPY jsons/ ./jsons/

ENV OLLAMA_URL=http://host.docker.internal:11434/api/embed
ENV BACKEND_PORT=5051
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 5051

CMD ["python", "backend/app.py"]
