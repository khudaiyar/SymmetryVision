# Use official Python 3.12 slim image
FROM python:3.12-slim

# Set working directory to backend folder
WORKDIR /app/backend

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend/ ./backend

# Set Render port
ENV PORT=8080
EXPOSE 8080

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
