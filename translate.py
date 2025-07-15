#!/usr/bin/env python3

import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Translate Hebrew to English and/or correct English text.")
    parser.add_argument("text", help="Text to translate or correct.", type=str)
    args = parser.parse_args()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert translator and editor. "
                    "If the input contains Hebrew, translate it into clear, professional, and natural English suitable for workplace communication. "
                    "If the input is English with errors, correct and improve it for clarity and professionalism, but keep the tone friendly and easy to understand—not overly formal. "
                    "If the input mixes Hebrew and English, translate the Hebrew parts and correct the English parts as above. "
                    "Always respond in English only. "
                    "Preserve the original meaning, intent, and tone. "
                    "Keep any @mentions, formatting, or code unchanged. "
                    "Only return the improved text—no explanations or prefixes."
                )
            },
            {"role": "user", "content": args.text}
        ],
        max_tokens=2000,
        temperature=0.2
    )
    
    result = response.choices[0].message.content
    print(result.strip() if result else "")

if __name__ == "__main__":
    main() 