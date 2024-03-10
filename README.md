
# Chat-with-Code Application using RAG

Welcome to the Chat-with-Code application repository! This project utilizes Retrieval Augmented Generation techniques using LlamaIndex, LangChain, and Ollama to interact with codebases

## Setting up Environment Variables

Before running the application, ensure you have set up the following environment variables:

1. **GITHUB_TOKEN**: This token allows access to the GitHub API. Please set it in the `.env` file.
   
   Example `.env` file:
   ```
   GITHUB_TOKEN=your_github_token_here
   ```

2. **OPEN_API_KEY**: This key is used for specific functionalities, such as accessing external APIs. In Linux, you can set it using the following command:
   
   ```
   export OPEN_API_KEY=your_open_api_key_here
   ```

   For Windows users, set the environment variable using the appropriate command.
   ```
   set OPEN_API_KEY=your_open_api_key_here
   ```


## Setting up Virtual Environment and Installing Dependencies

To set up and activate the virtual environment and install all required dependencies, you can use the following commands:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate      # For Windows

# Install dependencies
pip install -r requirements.txt
```

## Setting up Ollama (Local LLM)

If you wish to use Ollama (Local Language Model) for enhanced interactions, follow these steps:

1. Install Ollama 

    ```bash 
    sudo apt install curl
    curl -fsSL https://ollama.com/install.sh | sh
    pip install -r ollama.txt
    ```

2. Once installed, pull the llama2 model 

   ```
   ollama pull llama2
   ```

3. Once the llama2 llm has been pulled execute the following command to start the server in a different terminal:
    ```bash
    ollama serve
    ```
## Usage

After setting up the environment variables and installing dependencies, you can run the Chat-with-Code application.

```bash
python src/main.py
```

Feel free to explore the functionalities and engage in interactive code discussions!

For any issues or feedback, please open an issue in this repository. Thank you for using Chat-with-Code!