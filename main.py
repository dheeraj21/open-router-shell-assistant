import requests
import json
from rich.console import Console
from rich.theme import Theme
from rich.text import Text
from rich.panel import Panel
from dotenv import load_dotenv
import os
import html

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Set up a Rich theme
theme = Theme({
    "user": "#87ceeb",  # Sky blue
    "ai": "#87ceeb",  # Lime green  #32cd32
    "border": "#87ceeb",  # Bright red
    "panel.title": "#ffa07a",  # Bright orange
    "panel.border": "#66d9ef",  # Pastel blue
    "error": "bold red"
})

# Create a Rich console
console = Console(theme=theme)

# model = "meta-llama/llama-3.1-8b-instruct:free"
model = "nousresearch/hermes-3-llama-3.1-405b"

# Start a Rich console session
welcome_panel = Panel(
    f"""

[ai]Model: {model}[/ai]

[border]Available commands:[/border]

• [border]/help[/border] - Show list of available commands
• [border]/reset[/border] - Reset the conversation history
• [border]/save[/border] - Save the conversation history to a file
• [border]/quit[/border] - Quit the chat session

[border]How it works:[/border]

• This code uses the OpenRouter API to generate responses to user queries.
• It takes a user query as input and generates two responses:
    - One response is based on a default system prompt, which is a generic prompt that doesn't take into account the user's previous queries.
    - The second response is based on a user-entered system prompt, which is a prompt that the user can customize to fit their specific needs.
• The code prints both responses to the console for the user to see.

""",
    title="[ai]Open Router Prompt Companion[/ai]",
    border_style="border"
)
console.print(welcome_panel)

# Default system prompt
default_system_prompt = "You are an AI chat assistant. Respond to the user's queries."

# Prompt for system input
system_input = console.input("Enter a system prompt (optional): ")

# Print the user-entered system prompt inside the box
if system_input:
    system_panel = Panel(system_input, title="[border]User-Entered System Prompt[/border]", border_style="border")
    console.print(system_panel)
else:
    system_panel = Panel(default_system_prompt, title="[border]Default System Prompt[/border]", border_style="border")
    console.print(system_panel)

# Initialize conversation history for default system prompt
default_conversation_history = []

if system_input:
    # Add system input to conversation history for user-entered system prompt
    user_conversation_history = [{"role": "system", "content": system_input}]
else:
    # Add default system prompt to conversation history for default system prompt
    default_conversation_history.append({"role": "system", "content": default_system_prompt})
    # Add default system prompt to conversation history for user-entered system prompt
    user_conversation_history = [{"role": "system", "content": default_system_prompt}]

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
        default_conversation_history = [{"role": "system", "content": default_system_prompt}]
        user_conversation_history = [{"role": "system", "content": system_input if system_input else default_system_prompt}]
        console.print("Conversation history reset!", style="bold green")
        continue

    elif user_input == "/save":
        with open("conversation_history.json", "w") as f:
            json.dump(default_conversation_history, f, indent=4)
        console.print("Conversation history saved to conversation_history.json!", style="bold green")
        continue

    # Create a new list for the default system prompt
    new_default_conversation_history = default_conversation_history.copy()
    new_default_conversation_history.append({"role": "user", "content": user_input})

    # Send the entire conversation history to the OpenRouter API for the default system prompt
    response_default = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": model,  # Optional
            "messages": new_default_conversation_history
        })
    )

    # Check the response status code for the default system prompt
    if response_default.status_code == 200:
        try:
            # Load the JSON response for the default system prompt
            response_json_default = response_default.json()

            # Extract the content value from the response for the default system prompt
            content_default = response_json_default["choices"][0]["message"]["content"]

            # Check if the response is not empty
            if content_default.strip():
                # Create a RichText object for the AI's response for the default system prompt
                text_default = Text(content_default)

                # Create a Rich panel for the AI's response for the default system prompt
                panel_default = Panel(text_default, title="[border]AI (Default System Prompt)[/border]", border_style="border")

                # Print the AI's response to the console for the default system prompt
                console.print(panel_default)

                # Update the default conversation history with the AI's response
                default_conversation_history.append({"role": "assistant", "content": content_default})
            else:
                # Print an error message to the console for the default system prompt
                console.print("Error: Empty response from OpenRouter API for default system prompt", style="error")
        except KeyError as e:
            console.print("Error: KeyError (Default System Prompt)", e, style="error")
        except Exception as e:
            console.print("Error:", e, style="error")
    else:
        # Print an error message to the console for the default system prompt
        console.print("Error:", response_default.status_code, style="error")

    # Create a new list for the user-entered system prompt
    new_user_conversation_history = user_conversation_history.copy()
    new_user_conversation_history.append({"role": "user", "content": user_input})

    # Send the entire conversation history to the OpenRouter API for the user-entered system prompt
    response_user = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": model,  # Optional
            "messages": new_user_conversation_history
        })
    )

    # Check the response status code for the user-entered system prompt
    if response_user.status_code == 200:
        try:
            # Load the JSON response for the user-entered system prompt
            response_json_user = response_user.json()

            # Extract the content value from the response for the user-entered system prompt
            content_user = response_json_user["choices"][0]["message"]["content"]

            # Remove HTML tags from the output text
            content_user = html.unescape(content_user)
            content_user = content_user.replace("<thinking>", "").replace("</thinking>", "")
            content_user = content_user.replace("<output>", "").replace("</output>", "")

            # Check if the response is not empty
            if content_user.strip():
                # Create a RichText object for the AI's response for the user-entered system prompt
                text_user = Text(content_user)

                # Create a Rich panel for the AI's response for the user-entered system prompt
                panel_user = Panel(text_user, title=f"[border]AI (User-Entered System Prompt: {system_input if system_input else default_system_prompt})[/border]", border_style="border")

                # Print the AI's response to the console for the user-entered system prompt
                console.print(panel_user)

                # Update the user-entered conversation history with the AI's response
                user_conversation_history.append({"role": "assistant", "content": content_user})
            else:
                # Print an error message to the console for the user-entered system prompt
                console.print("Error: Empty response from OpenRouter API for user-entered system prompt", style="error")
        except KeyError as e:
            console.print("Error: KeyError (User-Entered System Prompt)", e, style="error")
        except Exception as e:
            console.print("Error:", e, style="error")
    else:
        # Print an error message to the console for the user-entered system prompt
        console.print("Error:", response_user.status_code, style="error")
