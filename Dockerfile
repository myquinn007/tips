# Use python 3.7.2 container image
FROM python:3.10-slim

# Set the working Directory
WORKDIR /app

# Copy the current directory to container
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt
RUN chmod -R 755 /app
# Run the command to start uWSGI
CMD ["uwsgi", "app.ini"]
