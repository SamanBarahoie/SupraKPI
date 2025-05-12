FROM apache/superset

# Switch to root user to install dependencies
USER root

# Update system and install necessary build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    pkg-config \
    libzstd-dev \
 && apt-get clean

# Install required Python packages with specific SQLAlchemy version
RUN pip install --upgrade pip
RUN pip install clickhouse-connect clickhouse-sqlalchemy zstandard "sqlalchemy<2.0"

# Switch back to the superset user
USER superset

