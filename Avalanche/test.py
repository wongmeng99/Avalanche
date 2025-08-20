# import packages
import streamlit as st
import pandas as pd
import re
import os
import string
import matplotlib.pyplot as plt


# Removing punctuation, lowercasting everything, stripped whitespace - GENAI
def clean_text(text):
    """
    Cleans input text by:
    - Removing punctuation
    - Converting to lowercase
    - Stripping leading/trailing whitespace
    """
    if not isinstance(text, str):
        return ""
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Convert to lowercase and strip whitespace
    return text.lower().strip()


# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "data", "customer_reviews.csv")
    return os.path.normpath(csv_path)


st.title("Hello, GenAI!")
st.write("This is your GenAI-powered data processing app.")

# Layout 2 buttons side by side
col1, col2 = st.columns(2)

# Button to Ingest data
with col1:
    if st.button("📥 Ingest Dataset"):
        try:
            csv_path = get_dataset_path()
            # Stores the df as a cache
            st.session_state["df"] = pd.read_csv(csv_path)
            st.success ("Dataset loaded successfully")
        except FileNotFoundError:
            st.error("Dataset not found. Please check the file path")

# Button to parse data
with col2:
    if st.button("🧹 Parse Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.success("Reviews Parsed & Cleaned")
        else:
            st.warning("Please ingest the dataset first.")

# Display the dataset if it exists
if "df" in st.session_state:
    # Product filter dropdown
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
    
    # Display dataset
    st.subheader(f"📁 Reviews for {product}")
    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)

    # Visualization
    st.subheader("Sentiment Score by Product")
    grouped = st.session_state["df"].groupby(["PRODUCT"])["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)

    fig, ax = plt.subplots(figsize=(10,6))
    ax.hist(st.session_state["df"]["SENTIMENT_SCORE"], bins=10, edgecolor='black',alpha=0.7)
    ax.set_xlabel('Sentiment Score')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Sentiment Scores')
    st.pyplot(fig)





