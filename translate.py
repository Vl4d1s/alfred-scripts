#!/usr/bin/env python3

import os
import sys
import argparse
from dotenv import load_dotenv  # For .env support
from openai import OpenAI

# Load environment variables from .env file if present
load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="Correct and improve English grammar using OpenAI GPT-3.5-turbo."
    )
    parser.add_argument(
        "text",
        type=str,
        help="Text to correct and improve. Enclose in quotes if it contains spaces.",
    )
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that helps users to correct grammar mistakes, typos, factual errors, translate and improve their text. "
                        "Please generate text when the user asks for help. Write in Markdown format and keep Slack mentions (@user) intact. "
                        "Do not fix any code but add new lines where necessary. Only reply with the corrected text; witout any prefix."
                    ),
                },
                {
                    "role": "user",
                    "content": f"correct and improve the following text to standard English:\nText: {args.text}\n",
                },
            ],
            max_tokens=2000,
            temperature=0.5,
            top_p=1,
            frequency_penalty=1.3,
            presence_penalty=1.3,
        )
        print(response.choices[0].message.content, end="")
    except Exception as e:
        print("ERROR:", str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 