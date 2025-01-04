import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_by_category_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 9, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 9, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)
        response=response.json()

        if isinstance(response, list) and response:
            # Calculate total expense
            total_expense = sum(item["total"] for item in response)

            # Prepare data for the DataFrame, including percentage calculation
            data = {
                "Category": [item["category"] for item in response],
                "Total": [item["total"] for item in response],
                "Percentage": [(item["total"] / total_expense) * 100 if total_expense != 0 else 0 for item in response]
            }


            # Create and sort DataFrame
            df = pd.DataFrame(data)
            df_sorted = df.sort_values(by="Percentage", ascending=False)

            # Display the results
            st.title("Expense Breakdown By Category")
            st.bar_chart(data=df_sorted.set_index("Category")['Percentage'], width=0, height=0, use_container_width=True)

            # Format Total and Percentage for display
            df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
            df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)

            st.table(df_sorted)


        else:
            st.write("No data available or API response is not in the expected format.")

