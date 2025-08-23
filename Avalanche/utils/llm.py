import os
import openai
from dotenv import load_dotenv
import streamlit as st
from utils.prompt import build_sentiment_prompt


# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI()

# Open AI prompt
@st.cache_data(ttl=3600)
def get_response(summary, score):
    prompt = build_sentiment_prompt(summary, score)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=200
    )
    return response.choices[0].message.content