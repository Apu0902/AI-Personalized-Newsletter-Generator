# Use a slim version of Python 3.9 as the base image.
FROM python:3.9-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy all files from the current directory to the container.
COPY . /app

# Install the required dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the Streamlit app.
CMD ["streamlit", "run", "app.py"]
