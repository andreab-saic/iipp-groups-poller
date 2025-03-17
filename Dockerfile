FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# install prerequisites arcgis-api
RUN apt-get update && apt-get install libkrb5-dev build-essential -y

# Update pip
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and related files
COPY poll_arcgis_groups.py /app

# Expose the application port
EXPOSE 80

# Command to run the app

CMD ["python3", "poll_arcgis_groups.py"]
