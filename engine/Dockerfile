# Phase D-prep: run the Governed Project Memory engine (API + web Cockpit) anywhere.
#   docker build -t gpm-engine -f engine/Dockerfile .
#   docker run -p 8777:8777 -v "$PWD:/app" gpm-engine
# → open http://localhost:8777
FROM python:3.11-slim
WORKDIR /app
COPY engine/requirements.txt engine/requirements.txt
RUN pip install --no-cache-dir -r engine/requirements.txt
COPY . .
EXPOSE 8777
ENV PORT=8777 ROOT=/app
CMD ["python", "engine/api.py"]
