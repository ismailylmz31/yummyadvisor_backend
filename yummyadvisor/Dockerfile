# Python slim imajını kullan
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt requirements.txt
COPY . .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Django için ortam değişkenlerini ayarla
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Django statik dosyalarını topla
RUN python manage.py collectstatic --noinput

# Django uygulamasını Gunicorn ile çalıştır
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8080", "--timeout=60", "yummyadvisor.wsgi:application"]

