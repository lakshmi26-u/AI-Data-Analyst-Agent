
import os
import streamlit as st
import pandas as pd
import agent
from google import genai

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Data Analyst Agent")
st.write("Upload your sales CSV and ask questions using AI.")

# --------------------------------------------------
# 2. GEMINI API CONNECTION
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key is not configured.")
    st.stop()

client = genai.Client(api_key=api_key)

# --------------------------------------------------
# 3. CSV FILE UPLOAD
# --------------------------------------------------

st.sidebar.title("Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # --------------------------------------------------
        # 4. DATA PREPARATION
        # --------------------------------------------------

        # Convert Order_Date into datetime
        if "Order_Date" in df.columns:
            df["Order_Date"] = pd.to_datetime(
                df["Order_Date"],
                errors="coerce"
            )

        # Calculate Revenue if it does not exist
        if (
            "Revenue" not in df.columns
            and "Quantity" in df.columns
            and "Unit_Price" in df.columns
        ):
            df["Revenue"] = (
                df["Quantity"] * df["Unit_Price"]
            )

        # --------------------------------------------------
        # 5. DATA VALIDATION
        # --------------------------------------------------

        required = [
            "Order_ID",
            "Order_Date",
            "Product",
            "Category",
            "Revenue"
        ]

        missing = [
            col for col in required
            if col not in df.columns
        ]

        if missing:
            st.error(f"Missing required columns: {missing}")
            st.stop()

        # Check missing or invalid required values
        if df[required].isnull().any().any():
            st.error(
                "Required columns contain missing or invalid values."
            )
            st.stop()

        # Validate Revenue
        if not pd.api.types.is_numeric_dtype(df["Revenue"]):
            st.error("Revenue must be numeric.")
            st.stop()

        if not pd.Series(
            pd.to_numeric(df["Revenue"], errors="coerce")
        ).map(
            lambda x: pd.notna(x) and abs(x) != float("inf")
        ).all():
            st.error("Revenue contains invalid values.")
            st.stop()

        if df.empty:
            st.error("The uploaded CSV file is empty.")
            st.stop()

        st.success("Dataset uploaded successfully!")

        # --------------------------------------------------
        # 6. DATASET PREVIEW
        # --------------------------------------------------

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Total Rows",
            df.shape[0]
        )

        col2.metric(
            "Total Columns",
            df.shape[1]
        )

        st.divider()

        # --------------------------------------------------
        # 7. ASK YOUR DATA ANALYST
        # --------------------------------------------------

        st.subheader("💬 Ask Your Data Analyst")

        user_question = st.text_input(
            "Ask a question about your sales data:",
            placeholder="Which are my top 3 products by revenue?"
        )

        consent = st.checkbox(
            "I understand that my question, dataset schema, "
            "and analysis results will be sent to Google's Gemini API."
        )

        if st.button("Analyse", type="primary"):

            if not user_question.strip():

                st.warning("Please enter a question.")

            elif not consent:

                st.warning(
                    "Please provide consent before using AI analysis."
                )

            else:

                try:
                    with st.spinner("Analysing your data..."):

                        tool_name, result, insight = (
                            agent.answer_question(
                                df,
                                user_question,
                                client
                            )
                        )

                    # --------------------------------------------------
                    # 8. DISPLAY ANALYSIS RESULTS
                    # --------------------------------------------------

                    st.success(
                        f"Analysis completed using: {tool_name}"
                    )

                    st.subheader("📊 Analysis Results")

                    st.dataframe(
                        result,
                        use_container_width=True
                    )

                    # --------------------------------------------------
                    # 9. DISPLAY VISUALIZATION
                    # --------------------------------------------------

                    st.subheader("📈 Visualization")

                    fig = agent.display_analysis_chart(
                        tool_name,
                        result
                    )

                    if fig is not None:

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    # --------------------------------------------------
                    # 10. BUSINESS INSIGHTS
                    # --------------------------------------------------

                    st.subheader("💡 Business Insights")

                    st.write(insight)

                except Exception:

                    st.error(
                        "Analysis failed. Please check your question "
                        "and try again."
                    )

    except Exception:

        st.error(
            "Could not read the CSV file. "
            "Please upload a valid CSV file."
        )

else:

    st.info("Please upload a CSV file to get started.")

