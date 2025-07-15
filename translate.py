#!/usr/bin/env python3

import os
import sys
import argparse
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_system_prompt() -> str:
    """Get unified system prompt for translation and correction."""
    return (
        "You are a professional translator and editor. "
        "If the input contains Hebrew text, translate it to natural, fluent English. "
        "If the input is English with typos or grammar errors, correct and improve it. "
        "If the input contains both Hebrew and English, translate the Hebrew parts to English and correct the English parts. "
        "Always output in English only. "
        "Preserve the original meaning and tone. "
        "Keep any @mentions, formatting, or code unchanged. "
        "Only return the corrected/translated text without any prefix or explanation."
    )

def process_text(text: str, client: OpenAI) -> str:
    """Process text for translation and correction."""
    system_prompt = get_system_prompt()
    user_prompt = f"Process this text (translate Hebrew to English and/or correct English):\n\n{text}"
    
    max_tokens = min(len(text) * 3, 2000)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=max_tokens,
        temperature=0.2,
        top_p=1.0
    )
    
    return response.choices[0].message.content.strip() if response.choices[0].message.content else ""

def main():
    parser = argparse.ArgumentParser(
        description="Translate Hebrew to English and/or correct English text using OpenAI GPT-4o-mini."
    )
    parser.add_argument(
        "text",
        type=str,
        help="Text to translate or correct. Enclose in quotes if it contains spaces."
    )
    
    args = parser.parse_args()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    try:
        result = process_text(args.text, client)
        print(result)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 