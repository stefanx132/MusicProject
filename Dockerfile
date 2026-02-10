FROM python:3.11-slim

WORKDIR /app

# Copiem fișierele
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Port Streamlit
EXPOSE 8501

# Comanda corectă pentru Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]