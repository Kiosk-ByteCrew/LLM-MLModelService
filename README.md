# LLM-MLModelService

This service contains for the LLM and ML models and FastApi framework to access the models.
Here is the full `README.md` code in a code block:

```markdown
# KioskLLMService

KioskLLMService is a FastAPI-based service designed to interact with a MongoDB instance, providing a health check endpoint that returns information about the LLM name. The service is intended to be run locally and comes with a pre-configured MongoDB document.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.9 or later**
- **MongoDB 6.0 or later**
- **Git**

## Clone the Repository

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/KioskLLMService.git
cd KioskLLMService
```

## Set Up the Virtual Environment

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

## Install Dependencies

With the virtual environment activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

## Set Up MongoDB

1. Install MongoDB using Homebrew:

   ```bash
   brew tap mongodb/brew
   brew install mongodb-community@6.0
   ```

2. Start the MongoDB service:

   ```bash
   brew services start mongodb/brew/mongodb-community
   ```

3. Open the MongoDB shell and insert the initial document:

   ```bash
   mongosh
   use kiosk_database
   db.mycollection.insertOne({ "LLMName": "OpenAI" })
   ```

## Running the FastAPI Service

To start the FastAPI service, run the following command:

```bash
uvicorn main:app --reload
```

If port 8000 is already in use, you can specify a different port:

```bash
uvicorn main:app --reload --port 8001
```

## Testing the Health API

You can test the health API by visiting the following URL in your browser or using `curl`:

```
http://127.0.0.1:8000/health
```

You should receive a response like this:

```json
{
  "LLMName": "OpenAI"
}
```

## Stopping MongoDB

If you need to stop the MongoDB service, run:

```bash
brew services stop mongodb/brew/mongodb-community
```

## Contributing

Feel free to open issues or submit pull requests if you'd like to contribute to this project.

## License

This project is licensed under the MIT License.

## Installing Required Libraries After Cloning

After cloning the repository, you can install all the required libraries using the `requirements.txt` file. Make sure you are in the virtual environment and run:

```bash
pip install -r requirements.txt
```

This will install all the dependencies needed to run the project.
```


