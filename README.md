# OpenRouter Prompt Companion

A Python shell Companion that uses the OpenRouter API to generate responses to user queries.

## Features

* Uses the OpenRouter API to generate responses to user queries
* Allows users to enter a custom system prompt
* Allows users to save conversation history to a file
* Includes a `/help` command to display available commands
* Includes a `/reset` command to reset conversation history
* Includes a `/quit` command to quit the script

## Installation

1. Clone the repository: `git clone https://github.com/dheeraj21/open-router-prompt-companion.git`
2. Change into the cloned directory: `cd open-router-prompt-companion`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage

1. Run the script: `python main.py`
2. Enter a system prompt (optional): `Enter a system prompt (optional):`
3. Enter user input: `You:`
4. View the generated responses: `AI (Default System Prompt):` and `AI (User-Entered System Prompt):`

## Environment Variables

export OPENROUTER_API_KEY= 'Your OpenRouter API key'

## License

This project is licensed under the APACHE 2.0.


