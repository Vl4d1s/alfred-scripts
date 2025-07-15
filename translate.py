#!/usr/bin/env python3

import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Translate Hebrew to English and/or correct English text.")
    parser.add_argument("text", help="Text to translate or correct.", type=str)
    args = parser.parse_args()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional translator and editor. "
                        "If the input contains Hebrew text, translate it to natural, fluent English. "
                        "If the input is English with typos or grammar errors, correct and improve it. "
                        "If the input contains both Hebrew and English, translate the Hebrew parts to English and correct the English parts. "
                        "Always output in English only. "
                        "Preserve the original meaning and tone. "
                        "Keep any @mentions, formatting, or code unchanged. "
                        "Only return the corrected/translated text without any prefix or explanation."
                    )
                },
                {"role": "user", "content": args.text}
            ],
            max_tokens=2000,
            temperature=0.2
        )
        
        result = response.choices[0].message.content
        print(result.strip() if result else "")
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 