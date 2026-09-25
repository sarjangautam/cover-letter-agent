import os

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from .env
load_dotenv()

# Check that the API key exists without displaying it
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY was not found. "
        "Check that your .env file exists and contains the API key."
    )

print("API key found.")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Test the API
response = client.responses.create(
    model="gpt-5.6-luna",
    input="Reply with exactly: OpenAI API connection successful."
)

print(response.output_text)