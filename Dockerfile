# app/Dockerfile

FROM python:3.12.3

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/yanufo/Row_APP_V1.5.git .

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app_prototype.py", "--server.port=8501", "--server.address=0.0.0.0"]