FROM python:3.13-slim

# Install system dependencies (including Graphviz)
RUN apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run your app 
CMD ["streamlit", "run", "app.py", "--server.port=10000", "--server.address=0.0.0.0"]
