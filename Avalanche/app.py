# import packages
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.llm import get_response
import os


# Helper function to get dataset path
def get_dataset_path():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "data", "customer_reviews.csv")
    return csv_path


st.title("🔍 GenAI Sentiment Analysis Dashboard")
st.write("This is your GenAI-powered data processing app.")

# Layout two buttons side by side
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Load Dataset"):
        try:
            csv_path = get_dataset_path()
            df = pd.read_csv(csv_path)
            st.session_state["df"] = df.head(10)
            st.success("Dataset loaded successfully!")
            st.session_state["summary"] = df["SUMMARY"]
            st.session_state["score"] = df["SENTIMENT_SCORE"]
        except FileNotFoundError:
            st.error("Dataset not found. Please check the file path.")

with col2:
    if st.button("🧹 Sentiment Analysis"):
        if "df" in st.session_state:
            with st.spinner("Analyzing sentiment..."):
                st.session_state["df"]["Sentiment"] = st.session_state["df"].apply(
                    lambda row: get_response(row["SUMMARY"], row["SENTIMENT_SCORE"]),
                    axis=1
            )
            st.success("Sentimant Analysis completed")
        else:
            st.warning("Please ingest the dataset first.")


# Display the dataset if it exists
if "df" in st.session_state:
    # Product filter dropdown
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
    st.subheader(f"📁 Reviews for {product}")

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)


    # Ensure sentiment analysis has been completed
    if "Sentiment" in st.session_state["df"].columns:
        st.subheader(f"📊 Sentiment Breakdown for {product}")

        # Use filtered_df from earlier selection
        df_viz = filtered_df.copy()

        # Count sentiment per product
        sentiment_per_product = df_viz.groupby(["PRODUCT", "Sentiment"]).size().reset_index(name="Count")

        # Add overall sentiment counts
        overall_counts = df_viz["Sentiment"].value_counts().reset_index()
        overall_counts.columns = ["Sentiment", "Count"]
        overall_counts["PRODUCT"] = "All Products"

        # Combine both
        combined_df = pd.concat([sentiment_per_product, overall_counts], ignore_index=True)

        # Ensure consistent sentiment order
        sentiment_order = ["Positive", "Neutral", "Negative"]
        combined_df["Sentiment"] = pd.Categorical(combined_df["Sentiment"], categories=sentiment_order, ordered=True)
        combined_df = combined_df.sort_values(["PRODUCT", "Sentiment"])

        # Plotly grouped bar chart
        fig = px.bar(
            combined_df,
            x="PRODUCT",
            y="Count",
            color="Sentiment",
            barmode="group",
            title="Sentiment Count per Product",
            color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"},
            category_orders={"Sentiment": sentiment_order}
        )

        fig.update_layout(xaxis_title="Product", yaxis_title="Count", legend_title="Sentiment")
        st.plotly_chart(fig, use_container_width=True)


