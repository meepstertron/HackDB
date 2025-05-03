FROM python:3.9-slim


RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app


COPY requirements.txt .


COPY wait-for-db.sh .
RUN chmod +x wait-for-db.sh


RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .


EXPOSE 5000


ENV FLASK_RUN_HOST=0.0.0.0


CMD ["./wait-for-db.sh", "db", "gunicorn", "--capture-output", "--workers", "4", "--bind", "0.0.0.0:5000", "run:app"]
