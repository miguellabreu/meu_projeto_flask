# Use Python slim image as base
FROM python:3.10-slim

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install required system packages including Fortran
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    gfortran \
    libgfortran5 \
    liblapack-dev \
    libblas-dev \
    libquadmath0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create fortran_codes directory and set permissions
RUN mkdir -p /app/fortran_codes && \
    chmod 755 /app/fortran_codes

# Copy only necessary files
COPY app/ /app/app/
COPY run.py /app/
COPY celery_worker.py /app/
COPY fortran_codes/write_xy_em_memoria.so /app/fortran_codes/
COPY fortran_codes/write_xy_em_memoria.f90 /app/fortran_codes/

# Set correct permissions
RUN chmod -R 755 /app/fortran_codes && \
    chmod 644 /app/fortran_codes/write_xy_em_memoria.f90

# Set up Fortran library paths
ENV LD_LIBRARY_PATH=/usr/lib:/usr/lib/x86_64-linux-gnu:/app/fortran_codes:$LD_LIBRARY_PATH

# Create necessary symlinks for Fortran libraries
RUN ln -sf /usr/lib/x86_64-linux-gnu/libgfortran.so.5 /usr/lib/libgfortran.so.5

# Expose Flask port
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run Flask
CMD ["python3", "-m", "flask", "run"]