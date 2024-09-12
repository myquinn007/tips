# Use python 3.7.2 container image
FROM python:3.9-slim

# Set the working Directory
WORKDIR /app

# Copy the current directory to container
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]
