# Base image
FROM python:3.10-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /workspace

# Install dependencies
COPY requirements.txt /workspace/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /workspace/requirements.txt

# Copy the project files into the container
COPY . /workspace

# Expose the application port
EXPOSE 8000

# Set the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
