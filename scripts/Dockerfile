# Dockerfile for sales_data_gen
FROM python:3.9-slim

WORKDIR /app


RUN pip install Faker clickhouse-driver


# Copy scripts and data
COPY scripts /app/scripts
COPY data /app/data

# Set the default command to run the script
CMD ["python", "/app/scripts/generate_data.py"]

