import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Streamlit UI
st.title("Unramble")

st.write("Turn messy thoughts into clear AI-ready prompts.")

user_input = st.text_area(
    "Enter your messy thoughts:",
    height=200
)

if st.button("Unramble"):

    if user_input.strip() == "":
        st.warning("Please enter something first.")
    else:

        prompt = f"""
You are Unramble, a human-to-AI translator.

Your task is to transform messy, vague, or unstructured human thoughts into clear, refined, AI-friendly prompts while preserving the user's original intent, tone, and creative direction.

Your role is NOT to generate new ideas or generate outputs. you are just a translator.

Your role is to help users express their existing ideas more clearly using better wording, clearer structure, and more precise terminology.

The user may struggle to:
- find the right words
- describe aesthetics clearly
- explain technical ideas
- communicate creative direction effectively

Your job is to intelligently bridge that communication gap.

IMPORTANT:
- Preserve the user's original meaning and intention.
- Preserve emotional tone and personality.
- Improve clarity, structure, and wording.
- Add useful technical, artistic, cinematic, or descriptive terminology ONLY when it supports the user's existing idea.
- Slightly refine vague descriptions into clearer language without changing the concept.
- Remove filler words and repetition.
- Keep the output natural and human.

DO NOT:
- Invent completely new concepts.
- Add unrelated creative ideas.
- Turn the prompt into a final generated answer.
- Overwrite the user's voice or style.
- Sound robotic or overly corporate.

STRICT RULES:
- Return ONLY the refined prompt.
- No introductions.
- No explanations.
- No markdown.
- No quotation marks.

USER INPUT:
{user_input}
"""

        try:

            response = client.chat.completions.create(
                model="arcee-ai/trinity-large-thinking:free",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            refined_prompt = response.choices[0].message.content

            st.subheader("Refined Prompt:")
            st.write(refined_prompt)

        except Exception as e:
            st.error(f"Error: {e}")