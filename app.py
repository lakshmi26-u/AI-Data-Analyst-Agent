
import streamlit as st
import pandas as pd
import agent


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

try:
    client = agent.get_gemini_client()

except Exception:
    st.error(
        "Gemini API key is not configured. "
        "Please add GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()


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
        df = pd.read_csv(uploaded_file)

        if df.empty:
            st.error("The uploaded CSV file is empty.")
            st.stop()

        # --------------------------------------------------
        # 4. DATA PREPARATION
        # --------------------------------------------------

        # Convert dates
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
                pd.to_numeric(df["Quantity"], errors="coerce")
                *
                pd.to_numeric(df["Unit_Price"], errors="coerce")
            )

        # Convert Revenue to numeric
        if "Revenue" in df.columns:

            df["Revenue"] = pd.to_numeric(
                df["Revenue"],
                errors="coerce"
            )

        # --------------------------------------------------
        # 5. DATA VALIDATION
        # --------------------------------------------------

        required_columns = [
            "Order_ID",
            "Order_Date",
            "Product",
            "Category",
            "Revenue"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:

            st.error(
                f"Missing required columns: {missing_columns}"
            )
            st.stop()

        # Check missing and invalid values
        if df[required_columns].isnull().any().any():

            st.error(
                "Required columns contain missing or invalid values."
            )
            st.stop()

        # Check infinite revenue values
        if not df["Revenue"].replace(
            [float("inf"), float("-inf")],
            pd.NA
        ).notna().all():

            st.error("Revenue contains invalid values.")
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

                except Exception as error:

                    st.error(
                        f"Analysis failed: {error}"
                    )

    except Exception as error:

        st.error(
            f"Could not process the CSV file: {error}"
        )

else:

    st.info(
        "Please upload a CSV file to get started."
    )


