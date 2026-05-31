FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Cloud Run sets the PORT environment variable dynamically.
# Streamlit will use this port.
ENV PORT=8080

EXPOSE $PORT

# Command to run the Streamlit app
CMD streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
