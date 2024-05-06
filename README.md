# Project Setup Instructions

Welcome to our project! To get everything running smoothly, please follow the steps below carefully.

## Getting Started

To ensure the program runs smoothly, you need to perform a couple of setup steps after cloning the repository.

### 1. Set Up the Environment File

First, you'll need to create a `.env` file in the root directory of the project (DjangoChatBot). This file will store sensitive information such as API keys. Add the following line to the `.env` file, replacing `YOUR_API_KEY_HERE` with your actual OpenAI API key:

```OPENAI_API_KEY="YOUR_API_KEY_HERE"```

### 2. Install Dependencies

Before running the application, make sure to install all the necessary dependencies. You can do this by running the following command in your terminal:

```pip install -r requirements.txt```

This command will install all the Python packages listed in `requirements.txt`, ensuring that all the project's dependencies are met.

## Running the Application

Once you have completed the setup, you can start the server by running the following command:

```python3 manage.py runserver```

## Running the Application with Docker

Use Docker to deploy the application consistently across any environment. Follow these steps and commands:

### Build the Docker Image
Build the Docker image containing all necessary components with the following command:

```
docker build -t satbot .
```

### Run the Application in a Docker Container
Start the application in a Docker container to keep deployment portable and isolated:

```
docker run -d -p 8000:8000 satbot
```

This command runs the `satbot` container in detached mode, making it accessible at `http://localhost:8000`.
