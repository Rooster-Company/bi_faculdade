# Use Python slim para uma imagem mais leve
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala apenas as dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos primeiro (para melhor cache)
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto da aplicação
COPY . .

# Expõe a porta do Streamlit
EXPOSE 8501

# Define variáveis de ambiente do Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "app.py"]
