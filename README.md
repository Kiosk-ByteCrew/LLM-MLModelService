# LLM-MLModelService

This service is responsible for interacting with LLM and ML models responsible for easing out the self ordering systems.

# Steps to setup this service in your local:
## Set Up the Virtual Environment

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3.  Install Dependencies With the virtual environment activated, install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Set Up MongoDB

1. Install MongoDB using brew:

   ```bash
   brew tap mongodb/brew
   brew install mongodb-community@6.0
   ```

2. Start the MongoDB service:

   ```bash
   brew services start mongodb/brew/mongodb-community
   ```

To Connect Mongo db in your local to your code, edit run.py configurations and add these environment variables:
   `DATABASE_NAME=local;MONGO_URI=mongodb://localhost:27017;port=8090;HOST=localhost`
Port can be as per your choice.

## Running the FastAPI Service
Just run `run.py`

## Health API
After setting up the service, you can try hitting the health api. HealthApi URL: `http://{your_localhost}/health`

It should return a response like: `{
    "status": "LLM-MLModel Service is up and running."
}`
