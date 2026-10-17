
import streamlit as st
import requests
import pandas as pd

from database import (
    create_feedback_table,
    save_feedback,
    load_feedback,
)

st.set_page_config(
    page_title="Customer Feedback Analysis",
    page_icon="💬",
    layout="centered",
)

API_URL = "http://127.0.0.1:8000/analyze"

# Create database table
create_feedback_table()

st.title("💬 Customer Feedback Analysis")


# Store analysis results across Streamlit reruns
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "review_text" not in st.session_state:
    st.session_state.review_text = ""

review = st.text_area(
    "Enter customer review",
    placeholder="The product is excellent and delivery was fast!",
    height=130,
)

if st.button("Analyze Sentiment", type="primary"):
    if not review.strip():
        st.warning("Please enter a customer review.")
    else:
        try:
            with st.spinner("Analyzing review..."):
                response = requests.post(
                    API_URL,
                    json={"text": review},
                    timeout=60,
                )
                response.raise_for_status()

            st.session_state.analysis_result = response.json()
            st.session_state.review_text = review
            st.success("Analysis completed!")

        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")

# Display analysis result
result = st.session_state.analysis_result

if result:
    st.subheader("Analysis Result")

    st.write("**Review:**", st.session_state.review_text)
    st.write("**Sentiment:**", result["label"].title())
    st.metric("Score", f'{result["score"]}/5')
    st.write("**Theme:**", result["theme"])

    # Save current result to SQLite
    if st.button("💾 Save Result"):
        try:
            save_feedback(
                review=st.session_state.review_text,
                label=result["label"],
                score=result["score"],
                theme=result["theme"],
            )
            st.success("Result saved to database!")
        except Exception as e:
            st.error(f"Could not save result: {e}")

st.divider()

# Show saved database records
if st.button("📋 Show Database Records"):
    st.session_state.show_records = True

if st.session_state.get("show_records", False):
    st.subheader("Saved Feedback Records")

    records = load_feedback()

    if records:
        df = pd.DataFrame(
            records,
            columns=["Review", "Sentiment", "Score", "Theme"],
        )
        df.index = df.index + 1
        df.index.name = "Record"
        st.dataframe(df, use_container_width=True)
        st.write(f"**Total records:** {len(records)}")
    else:
        st.info("No feedback records saved yet.")
