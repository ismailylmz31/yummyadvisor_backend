# PostGIS image'ını temel al
FROM postgis/postgis:latest

# Paketleri güncelle ve GDAL kütüphanelerini yükle
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# GDAL ortam değişkenlerini ayarla
ENV GDAL_DATA=/usr/share/gdal
ENV PATH="/usr/lib/postgresql/${PG_MAJOR}/bin:$PATH"

# Postgres kullanıcı ayarları
USER postgres

# Varsayılan çalışma dizinini ayarla
WORKDIR /var/lib/postgresql

# Portu aç
EXPOSE 5432

# Başlangıç komutunu ayarla
CMD ["postgres"]



