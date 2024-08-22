# Open Router Shell Assistant

A Python shell AI  assistant that uses the OpenRouter API to generate responses to user input.

## License
Apache License 2.0

## Installation

### Step 1: Clone the repository
```bash
git clone https://github.com/dheeraj21/open-router-shell-assistant.git
```
### Step 2: Install the required libraries
```bash
cd open-router-shell-assistant
pip install -r requirements.txt
```
### Step 3: Set the OpenRouter API key
```bash
rename .env.example file to .env and add your open router api key
```
### Step 4: Run the shell assistant
```bash
python main.py
```

## Commands

* `/help`: Display list of available commands
* `/reset`: Reset the conversation history
* `/save`: Save the conversation history to a file
* `/quit`: Quit the chat session

## Model

The shell assistant uses the `nousresearch/hermes-3-llama-3.1-405b` model by default, but you can change it easily by modifying the `model` variable in the `main.py` file.

## Dependencies

* `requests`
* `json`
* `rich`
* `dotenv`

## License
Apache License 2.0
