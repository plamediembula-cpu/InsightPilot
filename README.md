\# InsightPilot — AI-Powered Business Analytics Assistant



\## Project Overview



InsightPilot is an interactive business analytics application built using Python, Streamlit, and Generative AI.



The application helps small businesses analyze sales data, monitor financial performance, identify profitable products, and generate AI-powered business recommendations.



\## Key Features



1\. \*\*CSV Data Upload:\*\* Upload business sales data for analysis.

2\. \*\*Interactive Dashboard:\*\* View revenue, product costs, gross profit, and gross profit margin.

3\. \*\*Data Visualization:\*\* Explore sales trends and product performance using interactive charts.

4\. \*\*Business Filters:\*\* Filter sales by category, product, and date.

5\. \*\*Product Profitability Analysis:\*\* Identify products with the highest gross profit and profit margins.

6\. \*\*Generative AI Assistant:\*\* Ask questions about business performance and receive AI-generated insights.

7\. \*\*Automated AI Reports:\*\* Generate business recommendations without manually entering a question.

8\. \*\*PDF Report Download:\*\* Download a business performance report containing financial results and AI recommendations.



\## Technologies Used



\- Python

\- Streamlit

\- Pandas

\- Plotly

\- OpenAI API

\- ReportLab



\## How to Run InsightPilot



1\. Install Python.

2\. Open Command Prompt in the InsightPilot project folder.

3\. Install the required libraries:



&#x20;  `python -m pip install -r requirements.txt`



4\. Create a `.streamlit` folder containing a `secrets.toml` file with your own OpenAI API key:



&#x20;  `OPENAI\_API\_KEY = "YOUR\_API\_KEY"`



5\. Start the application:



&#x20;  `python -m streamlit run app.py`



6\. Open `http://localhost:8501` in your browser.

7\. Upload a CSV file containing the following columns:



&#x20;  `Date, Product, Category, Quantity, Unit\_Price, Unit\_Cost`



8\. Explore the dashboard, ask the AI questions, or generate an AI business report.



An OpenAI API account with available credits is required for AI-generated features. Other analysis features do not require an API key.



\## Business Value



InsightPilot helps business owners turn raw sales data into understandable information and actionable recommendations without requiring advanced data analytics knowledge.



\## Data and Security



The included sample data is fictional. Users should only upload business information they are authorized to process.



API keys must be stored privately and must never be included in publicly shared project files.



\## Limitations



Gross profit is calculated using recorded product costs. Operating expenses and taxes are not included. AI recommendations should be reviewed before making business decisions.



\## Project Purpose



Created as an extra-credit innovation project to demonstrate how generative AI can be combined with business intelligence and data analytics to solve real-world problems.

