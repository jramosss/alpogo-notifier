# Use an official Python image
FROM python:3.11

# Set the working directory
WORKDIR /code

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set PYTHONPATH to ensure modules are discoverable
ENV PYTHONPATH=/code

# Run pytest when the container starts
#CMD ["pytest", "-s", "tests/scrapers/test_places_scraper.py"]
