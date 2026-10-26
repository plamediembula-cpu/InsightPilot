
import streamlit as st

# Application settings
st.set_page_config(
    page_title="InsightPilot",
    page_icon="📊",
    layout="wide"
)

# Application title
st.title("📊 InsightPilot")
st.subheader("Your AI-Powered Business Analytics Assistant")

st.write(
    "Welcome to InsightPilot! Upload your business data, "
    "explore insights, and make smarter decisions."
)

st.divider()

# Main features
st.header("What can InsightPilot do?")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📁 Data Analysis")
    st.write("Upload business data and analyze sales and profits.")

with col2:
    st.subheader("📈 Dashboards")
    st.write("Explore business performance through interactive charts.")

with col3:
    st.subheader("🤖 AI Insights")
    st.write("Get AI-powered business insights and recommendations.")

st.divider()

st.success("Welcome! Your InsightPilot application is running.")


# Business data upload
st.divider()
st.header("📂 Upload Your Business Data")

uploaded_file = st.file_uploader(
    "Choose a CSV file containing your business data",
    type=["csv"]
)

if uploaded_file is not None:
    import pandas as pd

    try:
        df = pd.read_csv(uploaded_file)

        st.success("Your data was uploaded successfully!")

        st.subheader("📋 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Records", len(df))

        with col2:
            st.metric("Total Columns", len(df.columns))

        with col3:
            st.metric("Missing Values", int(df.isnull().sum().sum()))

        st.subheader("Available Columns")
        st.write(", ".join(df.columns.astype(str)))

    except Exception as e:
        st.error(f"Unable to read this CSV file: {e}")


# Business analytics dashboard
if uploaded_file is not None and "df" in locals():

    required_columns = {
        "Date", "Product", "Category",
        "Quantity", "Unit_Price", "Unit_Cost"
    }

    if required_columns.issubset(df.columns):

        import plotly.express as px

        data = df.copy()

        data["Quantity"] = pd.to_numeric(
            data["Quantity"], errors="coerce"
        )
        data["Unit_Price"] = pd.to_numeric(
            data["Unit_Price"], errors="coerce"
        )
        data["Unit_Cost"] = pd.to_numeric(
            data["Unit_Cost"], errors="coerce"
        )
        data["Date"] = pd.to_datetime(
            data["Date"], errors="coerce"
        )

        data = data.dropna(
            subset=["Date", "Quantity", "Unit_Price", "Unit_Cost"]
        )


        # Interactive business filters
        st.subheader("🔎 Filter Business Data")

        category_options = sorted(
            data["Category"].dropna().unique().tolist()
        )

        selected_categories = st.multiselect(
            "Select categories",
            options=category_options,
            default=category_options
        )

        product_options = sorted(
            data.loc[
                data["Category"].isin(selected_categories),
                "Product"
            ].dropna().unique().tolist()
        )

        selected_products = st.multiselect(
            "Select products",
            options=product_options,
            default=product_options
        )

        if not data.empty:
            min_date = data["Date"].min().date()
            max_date = data["Date"].max().date()

            selected_dates = st.date_input(
                "Select date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if len(selected_dates) == 2:
                start_date, end_date = selected_dates

                data = data[
                    data["Category"].isin(selected_categories)
                    & data["Product"].isin(selected_products)
                    & (
                        data["Date"].dt.date >= start_date
                    )
                    & (
                        data["Date"].dt.date <= end_date
                    )
                ].copy()
            else:
                st.info("Please select a start and end date.")
                st.stop()




        if not data.empty:

            data["Revenue"] = (
                data["Quantity"] * data["Unit_Price"]
            )
            data["Cost"] = (
                data["Quantity"] * data["Unit_Cost"]
            )
            data["Profit"] = (
                data["Revenue"] - data["Cost"]
            )

            total_revenue = data["Revenue"].sum()
            total_cost = data["Cost"].sum()
            total_profit = data["Profit"].sum()

            profit_margin = (
                total_profit / total_revenue * 100
                if total_revenue != 0 else 0
            )

            st.divider()
            st.header("📈 Business Analytics Dashboard")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Revenue", f"${total_revenue:,.2f}")
            col2.metric("Total Cost", f"${total_cost:,.2f}")
            col3.metric("Gross Profit", f"${total_profit:,.2f}")
            col4.metric("Gross Margin", f"{profit_margin:.1f}%")

            st.subheader("Revenue Trend")

            daily_sales = (
                data.groupby("Date", as_index=False)["Revenue"]
                .sum()
                .sort_values("Date")
            )

            fig1 = px.line(
                daily_sales,
                x="Date",
                y="Revenue",
                markers=True,
                title="Revenue Over Time"
            )

            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("Sales by Product")

            product_sales = (
                data.groupby("Product", as_index=False)["Revenue"]
                .sum()
                .sort_values("Revenue", ascending=False)
            )

            fig2 = px.bar(
                product_sales,
                x="Product",
                y="Revenue",
                color="Product",
                title="Revenue by Product"
            )

            st.plotly_chart(fig2, use_container_width=True)

            st.subheader("Revenue by Category")

            category_sales = (
                data.groupby("Category", as_index=False)["Revenue"]
                .sum()
            )

            fig3 = px.pie(
                category_sales,
                names="Category",
                values="Revenue",
                title="Revenue Distribution by Category"
            )

            st.plotly_chart(fig3, use_container_width=True)

        else:
            st.warning("No valid sales records found.")
    else:
        st.info(
            "For the business dashboard, upload a CSV containing "
            "Date, Product, Category, Quantity, Unit_Price, and Unit_Cost."
        )


# InsightPilot Generative AI Assistant
st.divider()
st.header("🤖 Ask InsightPilot AI")

st.write(
    "Ask a question about your sales, revenue, products, "
    "or business performance."
)

if "data" in locals() and not data.empty:

    question = st.text_input(
        "What would you like to know?",
        placeholder="How can I improve my business profits?"
    )

    if st.button("✨ Generate AI Insights"):

        if not question.strip():
            st.warning("Please enter a business question.")

        elif not st.secrets.get("OPENAI_API_KEY", ""):
            st.info(
                "The AI assistant is ready. "
                "An OpenAI API key is needed to generate responses."
            )

        else:
            from openai import OpenAI

            client = OpenAI(
                api_key=st.secrets["OPENAI_API_KEY"]
            )

            
            product_summary = (
                data.groupby("Product")[
                    ["Revenue", "Cost", "Profit"]
                ]
                .sum()
            )

            product_summary["Gross Margin (%)"] = (
                product_summary["Profit"]
                .div(
                    product_summary["Revenue"].replace(
                        0, float("nan")
                    )
                )
                .mul(100)
            )

            product_summary = (
                product_summary.round(2).to_string()
            )


            business_context = f"""
            Total revenue: ${total_revenue:,.2f}
            Total cost: ${total_cost:,.2f}
            Gross profit: ${total_profit:,.2f}
            Gross margin: {profit_margin:.1f}%

            Product performance:
            {product_summary}
            """

            try:
                with st.spinner("Analyzing your business data..."):

                    response = client.responses.create(
                        model="gpt-4.1-mini",
                        instructions=(
                            "You are InsightPilot, a professional "
                            "business analytics assistant. "
                            "Use the supplied business statistics "
                            "to answer questions and recommend actions. "
                            "Do not invent numbers or claim that "
                            "a correlation proves causation. "
                            "Be clear, practical, and concise."
                        ),
                        input=(
                            f"Business statistics:\n{business_context}"
                            f"\n\nBusiness question:\n{question}"
                        )
                    )

                    st.subheader("AI Business Insights")
                    st.write(response.output_text)
                    st.session_state["latest_ai_report"] = response.output_text

            except Exception:
                st.error(
                    "The AI request could not be completed. "
                    "Check your API configuration and account."
                )

else:
    st.info(
        "Upload a valid sales CSV file to activate "
        "the AI business assistant."
    )


# Product Profitability Analysis
if "data" in locals() and not data.empty:

    st.divider()
    st.header("💰 Product Profitability Analysis")

    st.write(
        "Compare products by revenue, gross profit, "
        "and gross profit margin."
    )

    profitability = (
        data.groupby("Product", as_index=False)[
            ["Revenue", "Cost", "Profit"]
        ]
        .sum()
    )

    profitability["Gross Margin (%)"] = (
        profitability["Profit"]
        .div(profitability["Revenue"].replace(0, float("nan")))
        .mul(100)
        .fillna(0)
    )

    profitability = profitability.sort_values(
        "Profit", ascending=False
    )

    st.dataframe(
        profitability,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn(
                "Revenue", format="$%.2f"
            ),
            "Cost": st.column_config.NumberColumn(
                "Cost", format="$%.2f"
            ),
            "Profit": st.column_config.NumberColumn(
                "Gross Profit", format="$%.2f"
            ),
            "Gross Margin (%)": st.column_config.NumberColumn(
                "Gross Margin (%)", format="%.1f%%"
            ),
        }
    )

    best_margin_product = profitability.loc[
        profitability["Gross Margin (%)"].idxmax()
    ]

    st.success(
        f"Highest gross margin: {best_margin_product['Product']} "
        f"({best_margin_product['Gross Margin (%)']:.1f}%)"
    )


# Downloadable Business Report
if "data" in locals() and not data.empty and "Profit" in data.columns:

    import io
    from datetime import datetime
    from xml.sax.saxutils import escape
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    )

    st.divider()
    st.header("📄 Download Business Report")

    st.write(
        "Generate a professional PDF report based on "
        "your selected business data."
    )

    def create_business_report():

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        elements = []

        elements.append(
            Paragraph("InsightPilot", styles["Title"])
        )

        elements.append(
            Paragraph("Business Performance Report", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"Generated: {datetime.now():%B %d, %Y}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        # Financial summary for selected data
        revenue = data["Revenue"].sum()
        cost = data["Cost"].sum()
        profit = data["Profit"].sum()
        margin = profit / revenue * 100 if revenue else 0

        elements.append(
            Paragraph("Financial Overview", styles["Heading2"])
        )

        summary = [
            ["Metric", "Value"],
            ["Total Revenue", f"${revenue:,.2f}"],
            ["Total Cost", f"${cost:,.2f}"],
            ["Gross Profit", f"${profit:,.2f}"],
            ["Gross Margin", f"{margin:.1f}%"]
        ]

        summary_table = Table(summary, colWidths=[250, 200])

        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17406D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.whitesmoke]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 9)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # Product profitability
        elements.append(
            Paragraph("Product Profitability", styles["Heading2"])
        )

        product_data = (
            data.groupby("Product")[["Revenue", "Profit"]]
            .sum()
            .sort_values("Profit", ascending=False)
        )

        product_rows = [
            ["Product", "Revenue", "Gross Profit", "Margin"]
        ]

        for product, row in product_data.iterrows():

            product_revenue = row["Revenue"]
            product_profit = row["Profit"]

            product_margin = (
                product_profit / product_revenue * 100
                if product_revenue else 0
            )

            product_rows.append([
                Paragraph(escape(str(product)), styles["Normal"]),
                f"${product_revenue:,.2f}",
                f"${product_profit:,.2f}",
                f"{product_margin:.1f}%"
            ])

        product_table = Table(
            product_rows,
            colWidths=[155, 115, 115, 85],
            repeatRows=1
        )

        product_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17406D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.whitesmoke]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ]))

        elements.append(product_table)
        elements.append(Spacer(1, 20))

        elements.append(
            Paragraph(
                "Gross profit equals revenue minus recorded product costs. "
                "Operating expenses and taxes are not included.",
                styles["Normal"]
            )
        )

        # Include the most recent AI-generated insights
        ai_report = st.session_state.get("pdf_ai_report")

        if ai_report:
            elements.append(Spacer(1, 20))
            elements.append(
                Paragraph("AI Business Recommendations", styles["Heading2"])
            )

            for paragraph in ai_report.split("\n"):
                if paragraph.strip():
                    elements.append(
                        Paragraph(
                            escape(paragraph),
                            styles["Normal"]
                        )
                    )
                    elements.append(Spacer(1, 6))


        doc.build(elements)

        buffer.seek(0)
        return buffer.getvalue()

    import hashlib

    # Identify the currently selected business data
    report_fingerprint = hashlib.sha256(
        data[[
            "Date", "Product", "Category",
            "Quantity", "Unit_Price", "Unit_Cost"
        ]].to_csv(index=False).encode("utf-8")
    ).hexdigest()

    # Generate new recommendations without asking a question
    if st.button("✨ Generate AI Business Report"):

        api_key = st.secrets.get("OPENAI_API_KEY", "")

        if not api_key:
            st.error("Please configure your OpenAI API key.")

        else:
            from openai import OpenAI

            product_report = data.groupby("Product")[
                ["Revenue", "Cost", "Profit"]
            ].sum()

            product_report["Gross Margin (%)"] = (
                product_report["Profit"]
                .div(product_report["Revenue"].replace(0, float("nan")))
                .mul(100)
            )

            context = (
                f"Revenue: ${data['Revenue'].sum():,.2f}\n"
                f"Cost: ${data['Cost'].sum():,.2f}\n"
                f"Gross profit: ${data['Profit'].sum():,.2f}\n"
                f"Product performance:\n"
                f"{product_report.round(2).to_string()}"
            )

            try:
                with st.spinner("Generating your AI business report..."):
                    client = OpenAI(api_key=api_key)

                    result = client.responses.create(
                        model="gpt-4.1-mini",
                        instructions=(
                            "You are a professional business analyst. "
                            "Provide three actionable business recommendations "
                            "based strictly on the supplied statistics. "
                            "Distinguish gross profit dollars from gross margin. "
                            "Do not invent data or claim causation without evidence. "
                            "Use concise plain text."
                        ),
                        input=context
                    )

                    st.session_state["pdf_ai_report"] = result.output_text
                    st.session_state["pdf_data_fingerprint"] = report_fingerprint

                    st.success("Your AI business report is ready!")

            except Exception:
                st.error(
                    "Could not generate the AI report. "
                    "Please check your API connection."
                )


    
    # Only allow download for the current filtered data
    report_is_current = (
        st.session_state.get("pdf_data_fingerprint")
        == report_fingerprint
        and bool(st.session_state.get("pdf_ai_report"))
    )

    if report_is_current:
        pdf_report = create_business_report()

        st.download_button(
            label="📥 Download AI Business Report (PDF)",
            data=pdf_report,
            file_name="InsightPilot_AI_Business_Report.pdf",
            mime="application/pdf"
        )
    else:
        st.info(
            "Click Generate AI Business Report to create "
            "fresh recommendations for the selected data."
        )








