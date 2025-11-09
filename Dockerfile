FROM python:3.12-slim

# Set working directory to backend
WORKDIR /app/backend

# Copy requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY backend/ ./backend

# Expose Render port
ENV PORT=8080
EXPOSE 8080

# Run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
