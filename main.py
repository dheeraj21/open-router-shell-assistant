#main.py
import requests
import json
from rich.console import Console
from rich.theme import Theme
from rich.markdown import Markdown
from rich.panel import Panel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Set up a Rich theme
theme = Theme({
    "user": "#87ceeb",  # Sky blue
    "ai": "#87ceeb",  # Lime green  #32cd32
    "border": "#87ceeb",  # Bright red
    "panel.title": "#ffa07a",  # Bright orange
    "panel.border": "#66d9ef"  # Pastel blue
})

# Create a Rich console
console = Console(theme=theme)

#model = "meta-llama/llama-3.1-8b-instruct:free"
model = "nousresearch/hermes-3-llama-3.1-405b"


# Start a Rich console session
welcome_panel = Panel(
    f"""

[ai]Model: {model}[/ai]

[border]Available commands:[/border]

• [border]/help[/border] - Show list of available commands
• [border]/reset[/border] - Reset the conversation history
• [border]/save[/border] - Save the conversation history to a file
• [border]/quit[/border] - Quit the chat session""",
    title="[ai]Open Router Shell Assistant[/ai]",
    border_style="border"
)
console.print(welcome_panel)

# Initialize conversation history
conversation_history = []

while True:
    # Get user input
    user_input = console.input("You: ")

    if user_input == "/quit":
        console.print("Goodbye!", style="bold green")
        break

    elif user_input == "/help":
        console.print("Available commands:", style="bold cyan")
        console.print("/help - Show list of available commands")
        console.print("/quit - Quit the chat session")
        console.print("/reset - Reset the conversation history")
        console.print("/save - Save the conversation history to a file")
        continue

    elif user_input == "/reset":
        conversation_history = []
        console.print("Conversation history reset!", style="bold green")
        continue

    elif user_input == "/save":
        with open("conversation_history.json", "w") as f:
            json.dump(conversation_history, f, indent=4)
        console.print("Conversation history saved to conversation_history.json!", style="bold green")
        continue

    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Send the entire conversation history to the OpenRouter API
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": model,  # Optional
            "messages": conversation_history
        })
    )

    # Check the response status code
    if response.status_code == 200:
        # Load the JSON response
        response_json = response.json()

        # Extract the content value from the response
        content = response_json["choices"][0]["message"]["content"]

        # Add the AI's response to the conversation history
        conversation_history.append({"role": "assistant", "content": content})

        # Render the Markdown content using rich.markdown
        markdown = Markdown(content)

        # Create a Rich panel for the AI's response
        panel = Panel(markdown, title="[border]AI", border_style="border")

        # Print the AI's response to the console
        console.print(panel)
    else:
        # Print an error message to the console
        console.print("Error:", response.status_code, style="error")
