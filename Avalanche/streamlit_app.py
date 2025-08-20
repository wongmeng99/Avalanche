from openai import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st 

@st.cache_data
def get_response(user_prompt, temperature):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature_slider,  # A bit of creativity
        max_tokens=100  # Limit response length
        )
    return response
import os
import streamlit as st

def get_openai_api_key():
    # Prioritize Streamlit secrets if available
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    
    # Fallback to local environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return api_key

    # Final fallback: raise error
    raise ValueError("OpenAI API key not found in Streamlit secrets or environment variables.")

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
api_key = get_openai_api_key()

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

st.title('Hello, GENAI!')
st.write('This is your first streamlit app')

# Add a text input box for user prompt
user_prompt = st.text_input("Enter your prompt:","Explain generatvive AI in one sentence.")

# Add a slider for temperature
temperature_slider = st.slider(
    "Model Temperature:",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.01,
    help='Control randomness: 0 = deterministic, 1 = very creative'
)

# Make a chat completion request
with st.spinner("AI is working..."):
    response = get_response(user_prompt, temperature_slider)

    # Print the response
    st.write(response.choices[0].message.content)
