FROM python:3.9-slim

#Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

#Set working directory inside the container
WORKDIR /app

#Copy and install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy Python script and model
COPY MicrobusinessDensityStateForecasts.py .
COPY microbusiness_density_state_level_model.pkl .
COPY engagement_index_state.npy .
COPY dates.csv .

#Expose the port on which FastAPI will run
EXPOSE 7000

#Command to run API using uvicorn
CMD ["uvicorn", "MicrobusinessDensityStateForecasts:app", "--host", "0.0.0.0", "--port", "7000"]