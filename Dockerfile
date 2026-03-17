# Use the official Python image as the base image
FROM  mn-cosi-opsmate-docker-local.artifactory-mn-espoo3.int.net.nokia.com/lyra/mcp-server-base:0.0.2

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "app/main.py"]