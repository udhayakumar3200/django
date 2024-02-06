FROM python:3.10.6-buster

# Set unbuffered output for python
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Bundle app source
COPY . .

# Set execution permissions for the script
RUN chmod +x /app/django.sh

# Expose port
EXPOSE 8000

# entrypoint to run the django.sh file
ENTRYPOINT ["/app/django.sh"]
