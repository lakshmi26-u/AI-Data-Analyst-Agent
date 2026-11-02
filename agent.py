
import pandas as pd
import plotly.express as px
from google import genai
from google.genai import types
import streamlit as st

def display_analysis_chart(tool_name, result):

    if tool_name == "top_products":
        fig = px.bar(result, x="Product", y="Revenue",
                     title="Top Products by Revenue", text="Revenue")

    elif tool_name == "monthly_sales":
        fig = px.bar(result.sort_values("Order_Date"),
                     x="Order_Date", y="Revenue",
                     title="Monthly Revenue", text="Revenue")

    elif tool_name == "category_aov":
        fig = px.bar(result, x="Category",
                     y="average_order_value",
                     title="Average Order Value by Category",
                     text="average_order_value")

    elif tool_name == "detect_trends":
        fig = px.line(result, x="Order_Date", y="Revenue",
                      markers=True, title="Monthly Revenue Trend")

    else:
        return None

    return fig

def get_top_products(df, n=5):
    required_columns = ["Product", "Revenue"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    if not pd.api.types.is_numeric_dtype(df["Revenue"]):
        raise ValueError("Revenue must be numeric.")

    if n < 1:
        raise ValueError("n must be at least 1.")

    result = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )

    return result


def get_monthly_sales(df):
    required_columns = ["Order_Date", "Revenue"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    if not pd.api.types.is_datetime64_any_dtype(df["Order_Date"]):
        raise ValueError("Order_Date must be a datetime column.")

    if not pd.api.types.is_numeric_dtype(df["Revenue"]):
        raise ValueError("Revenue must be numeric.")

    monthly_sales = (
        df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    monthly_sales["Order_Date"] = monthly_sales["Order_Date"].astype(str)

    return monthly_sales


def get_category_aov(df):
    required_columns = ["Category", "Order_ID", "Revenue"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    if not pd.api.types.is_numeric_dtype(df["Revenue"]):
        raise ValueError("Revenue must be numeric.")

    if df["Order_ID"].isna().any():
        raise ValueError("Order_ID contains missing values.")

    result = (
        df.groupby("Category")
        .agg(
            total_revenue=("Revenue", "sum"),
            total_orders=("Order_ID", "nunique")
        )
        .reset_index()
    )

    result["average_order_value"] = (
        result["total_revenue"] / result["total_orders"]
    )

    return result.sort_values(
        "average_order_value", ascending=False
    )


def detect_sales_trends(df, threshold_pct=30):
    required_columns = ["Order_Date", "Revenue"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")

    if not pd.api.types.is_datetime64_any_dtype(df["Order_Date"]):
        raise ValueError("Order_Date must be datetime.")

    if not pd.api.types.is_numeric_dtype(df["Revenue"]):
        raise ValueError("Revenue must be numeric.")

    if df["Order_Date"].isna().any() or df["Revenue"].isna().any():
        raise ValueError("Date and Revenue cannot contain missing values.")

    if threshold_pct <= 0:
        raise ValueError("Threshold must be greater than zero.")

    monthly = (
        df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"]
        .sum()
        .reset_index()
    )

    monthly["Order_Date"] = monthly["Order_Date"].astype(str)

    monthly["change_pct"] = (
        monthly["Revenue"].pct_change() * 100
    ).round(2)

    monthly["unusual_change"] = (
        monthly["change_pct"].abs() >= threshold_pct
    )

    return monthly

ANALYSIS_TOOLS = {
    "top_products": get_top_products,
    "monthly_sales": get_monthly_sales,
    "category_aov": get_category_aov,
    "detect_trends": detect_sales_trends
}

def run_analysis_tool(df, tool_name, arguments=None):

    if arguments is None:
        arguments = {}

    if tool_name not in ANALYSIS_TOOLS:
        raise ValueError(f"Tool '{tool_name}' is not allowed.")

    if not isinstance(arguments, dict):
        raise ValueError("Arguments must be a dictionary.")

    if tool_name == "top_products":

        if set(arguments) - {"n"}:
            raise ValueError("Unsupported arguments.")

        n = arguments.get("n", 5)

        if type(n) is not int or n < 1 or n > 20:
            raise ValueError("n must be an integer between 1 and 20.")

        return get_top_products(df, n=n)

    elif tool_name == "monthly_sales":

        if arguments:
            raise ValueError("This tool accepts no arguments.")

        return get_monthly_sales(df)

    elif tool_name == "category_aov":

        if arguments:
            raise ValueError("This tool accepts no arguments.")

        return get_category_aov(df)

    elif tool_name == "detect_trends":

        if set(arguments) - {"threshold_pct"}:
            raise ValueError("Unsupported arguments.")

        threshold = arguments.get("threshold_pct", 30)

        if type(threshold) not in (int, float):
            raise ValueError("Threshold must be numeric.")

        if not 0 < threshold <= 1000:
            raise ValueError("Threshold must be between 0 and 1000.")

        return detect_sales_trends(df, threshold_pct=threshold)

top_products_tool = types.FunctionDeclaration(
    name="top_products",
    description="Find top products based on total revenue.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "n": types.Schema(
                type=types.Type.INTEGER,
                description="Number of top products. Default is 5."
            )
        }
    )
)

monthly_sales_tool = types.FunctionDeclaration(
    name="monthly_sales",
    description="Calculate total revenue for each month.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={}
    )
)

category_aov_tool = types.FunctionDeclaration(
    name="category_aov",
    description="Calculate average order value for each category.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={}
    )
)

detect_trends_tool = types.FunctionDeclaration(
    name="detect_trends",
    description="Detect significant month-over-month revenue changes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "threshold_pct": types.Schema(
                type=types.Type.NUMBER,
                description="Percentage change threshold. Default is 30."
            )
        }
    )
)

analysis_tool = types.Tool(
    function_declarations=[
        top_products_tool,
        monthly_sales_tool,
        category_aov_tool,
        detect_trends_tool
    ]
)

def get_gemini_client():

    api_key = st.secrets.get("GEMINI_API_KEY", None)

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in Streamlit secrets."
        )

    return genai.Client(api_key=api_key)

def select_analysis_tool(user_question, data, client):

    schema = []

    for column in data.columns:
        schema.append({
            "column_name": column,
            "data_type": str(data[column].dtype),
            "missing_values": int(data[column].isnull().sum())
        })

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
        You are a professional Data Analyst AI Agent.

        USER QUESTION:
        {user_question}

        AVAILABLE DATASET SCHEMA:
        {schema}

        Select the most appropriate analysis tool.

        Rules:
        - Only select from the registered tools.
        - Never invent column names.
        - Do not calculate results yourself.
        - Python will perform all calculations.
        """,
        config=types.GenerateContentConfig(
            tools=[analysis_tool],
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode="ANY"
                )
            )
        )
    )

    if not response.function_calls:
        raise ValueError("Gemini did not select an analysis tool.")

    return response.function_calls[0]

def execute_analysis(df, function_call):

    tool_name = function_call.name
    arguments = dict(function_call.args)

    result = run_analysis_tool(
        df,
        tool_name,
        arguments
    )

    return result

def generate_business_insight(
    user_question,
    analysis_result,
    client
):

    prompt = f"""
    You are a professional business data analyst.

    User question:
    {user_question}

    Verified Python analysis results:
    {analysis_result.to_string(index=False)}

    Instructions:
    1. Answer using only the verified results.
    2. Never invent numbers or facts.
    3. Do not assume reasons for revenue changes.
    4. Clearly distinguish observations from hypotheses.
    5. Label unsupported explanations as things to investigate.
    6. Use Indian Rupees (₹) for monetary values.
    7. Give one practical business recommendation.

    Use simple, professional language.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

def answer_question(df, user_question, client):

    function_call = select_analysis_tool(
        user_question,
        df,
        client
    )

    tool_name = function_call.name

    result = execute_analysis(
        df,
        function_call
    )

    insight = generate_business_insight(
        user_question,
        result,
        client
    )

    return tool_name, result, insight


def select_analysis_tool(user_question, data, client):

    if not is_supported_question(user_question):
        raise ValueError(
            "Sorry, I can only answer questions related to the available sales analysis."
        )

    schema = []

    for column in data.columns:
        schema.append({
            "column_name": column,
            "data_type": str(data[column].dtype),
            "missing_values": int(data[column].isnull().sum())
        })

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
        You are a professional Data Analyst AI Agent.

        USER QUESTION:
        {user_question}

        AVAILABLE DATASET SCHEMA:
        {schema}

        AVAILABLE TOOLS:
        - top_products: Find top products by revenue.
        - monthly_sales: Calculate monthly revenue.
        - category_aov: Calculate average order value.
        - detect_trends: Detect unusual monthly revenue changes.

        Select a tool only if it matches the user's question.
        Never invent column names or calculate results yourself.
        """,
        config=types.GenerateContentConfig(
            tools=[analysis_tool],
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode="AUTO"
                )
            )
        )
    )

    if not response.function_calls:
        raise ValueError("No suitable analysis tool was selected.")

    return response.function_calls[0]

def is_supported_question(user_question):
    question = user_question.lower()

    supported_topics = [
        "sales", "revenue", "product", "products",
        "category", "categories", "monthly", "month",
        "trend", "trends", "order", "orders",
        "average order value", "aov", "highest", "lowest",
        "top", "best", "performance"
    ]

    return any(word in question for word in supported_topics)
