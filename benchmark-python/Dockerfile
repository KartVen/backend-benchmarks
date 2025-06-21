FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "benchmark_python.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=4", "--threads=2"]