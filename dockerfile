# Pull this image as a foundation for our container's image 
FROM ubuntu

# Work will happen in a newly made "app" directory
WORKDIR /app 

# Always copy the requirements into the current working directory
COPY requirements.txt ./

# Install the requirements via this command
RUN pip install -r requirements.txt

# Copy over all local files to container... except the ones in the dockerignore file
COPY . .

# Create an environment + expose port
ENV PORT=5000

EXPOSE 5000

# Only 1 command per dockerfile
CMD ["python", "main.py"] # Exec form of running a command. This reduces overhead bc a normal command has to run a shell session
