# pdf2jpg-service

Microservicio FastAPI que convierte PDF → JPG y devuelve un ZIP.

## Uso local (Docker)
```bash
docker build -t pdf2jpg .
docker run -p 8000:8000 pdf2jpg
