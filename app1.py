import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Unramble",
    page_icon="🌀",
    layout="centered"
)

# ---------------- LOAD ENV ---------------- #

load_dotenv()

# ---------------- OPENROUTER CLIENT ---------------- #

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f0f14 0%,
        #161621 40%,
        #1f1f2e 100%
    );
    color: white;
    font-family: 'Inter', sans-serif;
}

/* Remove Streamlit default padding */
.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
    max-width: 850px;
}

/* Main title */
.main-title {
    font-size: 4rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.3rem;
    letter-spacing: -2px;

    background: linear-gradient(
        90deg,
        #ffffff,
        #b8b8ff,
        #8be9fd
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #b0b0c3;
    margin-bottom: 3rem;
}

/* Text area */
.stTextArea textarea {
    background-color: rgba(255,255,255,0.05);
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 20px;
    font-size: 1rem;
    backdrop-filter: blur(10px);
}

/* Text area focus */
.stTextArea textarea:focus {
    border: 1px solid #8be9fd;
    box-shadow: 0 0 15px rgba(139,233,253,0.3);
}

/* Button */
.stButton button {
    width: 100%;
    height: 55px;
    border: none;
    border-radius: 18px;

    background: linear-gradient(
        90deg,
        #7c5cff,
        #5ce1e6
    );

    color: white;
    font-size: 1rem;
    font-weight: 700;

    transition: all 0.3s ease;
}

/* Button hover */
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(92,225,230,0.25);
}

/* Output box */
.output-box {
    margin-top: 2rem;
    padding: 25px;

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 22px;

    backdrop-filter: blur(14px);

    line-height: 1.7;
    font-size: 1rem;
    color: #f2f2f2;
}

/* Small label */
.output-label {
    font-size: 0.85rem;
    color: #8be9fd;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

/* Hide Streamlit branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ---------------- #

st.markdown(
    """
    <div class="main-title">
        Unramble
    </div>

    <div class="subtitle">
        Turn messy thoughts into clear AI-ready prompts.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- INPUT ---------------- #

user_input = st.text_area(
    "",
    placeholder="Dump your chaotic thoughts here...",
    height=220
)

# ---------------- BUTTON ---------------- #

if st.button("Unramble My Thoughts"):

    if user_input.strip() == "":
        st.warning("Please enter something first.")

    else:

        prompt = f"""
You are Unramble, a human-to-AI translator.

Your task is to transform messy, vague, or unstructured human thoughts into clear, refined, AI-friendly prompts while preserving the user's original intent, tone, and creative direction.

Your role is NOT to generate new ideas or outputs.
You are only a translator.

IMPORTANT:
- Preserve the user's original meaning and tone.
- Improve wording, structure, and clarity.
- Add better terminology when useful.
- Remove repetition and filler.
- Keep it natural and human.

DO NOT:
- Invent new concepts.
- Overwrite the user's style.
- Sound robotic.

Return ONLY the refined prompt.

USER INPUT:
{user_input}
"""

        try:

            with st.spinner("Unrambling your thoughts..."):

                response = client.chat.completions.create(
                    model="arcee-ai/trinity-large-thinking:free",

                    messages=[
                        {
                            "role": "system",
                            "content": """
You are Unramble, a human-to-AI translator.
Transform messy thoughts into refined AI-ready prompts.
Never generate final outputs.
Only refine the user's existing idea.
"""
                        },

                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.6,
                    max_tokens=500
                )

                refined_prompt = response.choices[0].message.content

                st.markdown(
                    f"""
                    <div class="output-box">

                        <div class="output-label">
                            Refined Prompt
                        </div>

                        {refined_prompt}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"Error: {e}")