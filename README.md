
# AI Data Analyst Agent 🤖📊

An AI-powered data analysis application that allows users to explore sales data using natural-language questions. It combines Google's Gemini API with Python data-analysis tools to generate results, visualizations, and business insights.

## 🚀 Project Overview

The AI Data Analyst Agent helps users analyze sales data without manually writing pandas queries for every question.

Users can upload a CSV file, ask questions about their sales data, and view the analysis results through an interactive Streamlit interface.

## ✨ Features

- **CSV Upload:** Upload sales data for analysis.
- **Natural-Language Questions:** Ask questions about sales performance in plain English.
- **AI-Powered Tool Selection:** Gemini selects an appropriate predefined analysis tool.
- **Data Analysis:** Use pandas to calculate sales metrics and summaries.
- **Interactive Visualizations:** Display charts using Plotly.
- **Business Insights:** Generate explanations of the analysis results using Gemini.
- **Input Validation:** Check the uploaded dataset and handle unsupported questions.

## 🛠️ Technologies Used

- Python
- Pandas
- Google Gemini API
- Streamlit
- Plotly

## ⚙️ How It Works

1. The user uploads a CSV file.
2. The application validates the dataset.
3. The user asks a question about the sales data.
4. Gemini selects an available analysis tool.
5. Python and pandas perform the requested calculation.
6. Plotly displays a visualization when appropriate.
7. Gemini generates a business-oriented explanation of the results.

## 📂 Project Structure

```text
AI-Data-Analyst-Agent/
├── app.py
├── agent.py
├── sales_data.csv
├── requirements.txt
└── README.md
```

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Data-Analyst-Agent
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your Gemini API key

Create a Google Gemini API key and configure it as an environment variable named `GEMINI_API_KEY`.

Never commit your API key to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

## 🔐 Security Considerations

- Keep API keys and authentication tokens private.
- Use environment variables or a secrets manager for credentials.
- Do not upload private datasets or sensitive information.
- Treat uploaded CSV files as untrusted input.

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Building an interactive Python application.
- Integrating an LLM with predefined analysis tools.
- Performing data analysis with pandas.
- Creating data visualizations.
- Generating business insights from analytical results.
- Managing API credentials securely.

## 🔮 Future Improvements

- Support more CSV schemas and datasets.
- Add more data-analysis tools.
- Improve validation of natural-language questions.
- Add downloadable reports.
- Deploy the application for public access.

## 👩‍💻 Author

Created as a hands-on AI project to explore the integration of large language models, data analysis, and interactive applications.
