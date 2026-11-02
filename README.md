# AI Data Analyst Agent 🤖📊

An AI-powered sales data analysis application that allows users to explore sales data using natural-language questions. It combines Google's Gemini API with Python data-analysis tools to generate analytical results, visualizations, and business insights.

## 🚀 Project Overview

The AI Data Analyst Agent helps users analyze sales data without manually writing pandas queries for every question.

Users can upload a sales CSV file, ask questions about their data in plain English, and view the analysis results through an interactive Streamlit interface.

## ✨ Features

- **CSV Upload:** Upload sales datasets for analysis.
- **Natural-Language Questions:** Ask questions about sales performance in plain English.
- **AI-Powered Tool Selection:** Gemini selects an appropriate predefined analysis tool.
- **Data Analysis:** Use Python and pandas to calculate sales metrics and summaries.
- **Interactive Visualizations:** Display analytical charts using Plotly.
- **Business Insights:** Generate explanations of analysis results using Gemini.
- **Input Validation:** Validate required dataset columns and handle unsupported questions.

## 🛠️ Technologies Used

- Python
- Pandas
- Google Gemini API
- Streamlit
- Plotly

## ⚙️ How It Works

1. The user uploads a sales CSV file.
2. The application validates the dataset.
3. The user asks a question about the sales data.
4. Gemini selects an available analysis tool.
5. Python and pandas perform the requested calculation.
6. Plotly displays a visualization when appropriate.
7. Gemini generates a business-oriented explanation of the results.

## 📂 Project Structure

```text
AI-Data-Analyst-Agent/
│
├── app.py
├── agent.py
├── sales_data.csv
├── requirements.txt
└── README.md
```

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/lakshmi26-u/AI-Data-Analyst-Agent.git
```

### 2. Navigate to the project folder

```bash
cd AI-Data-Analyst-Agent
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your Gemini API key

Create a Google Gemini API key and configure it as an environment variable named `GEMINI_API_KEY`.

Never upload your API key or other credentials to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## 📋 Dataset Requirements

The current application is designed for sales datasets containing these required columns:

- `Order_ID`
- `Order_Date`
- `Product`
- `Category`
- `Revenue`

If `Revenue` is not provided, the application can calculate it using `Quantity` and `Unit_Price`, when both columns are available.

## 🔐 Security Considerations

- Keep API keys and authentication tokens private.
- Use environment variables or a secrets manager for credentials.
- Do not upload private datasets or sensitive information.
- Treat uploaded CSV files as untrusted input.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Building an interactive Python application.
- Integrating a Large Language Model (LLM) with predefined analysis tools.
- Performing data analysis using pandas.
- Creating interactive data visualizations.
- Generating business insights from analytical results.
- Managing API credentials securely.

## 🔮 Future Improvements

- Support additional CSV schemas and datasets.
- Add more data-analysis tools.
- Improve natural-language question validation.
- Add downloadable analytical reports.
- Deploy the application for public access.

## 👩‍💻 Author

**Uthralakshmi M**

Built as a hands-on project to explore the integration of Generative AI, Python data analysis, and interactive applications.
