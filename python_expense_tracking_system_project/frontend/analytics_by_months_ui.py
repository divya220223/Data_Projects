import streamlit as st

import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_by_months_tab():
    response = requests.get(f"{API_URL}/monthly_expense/")

    monthly_expense = response.json()

    # Create and sort DataFrame
    if isinstance(monthly_expense, list) and all(isinstance(i, dict) for i in monthly_expense):
        df = pd.DataFrame(monthly_expense)
        df.rename(columns={
            "Month": "Month Number",
            "Month_name": "Month Name",
            "total": "Total"
        }, inplace=True)

        df_sorted = df.sort_values(by="Month Number", ascending=False)
        df_sorted.set_index("Month Number", inplace=True)

    # Display the results
        st.title("Expense Breakdown By Month")
        st.bar_chart(data=df_sorted.set_index("Month Name")['Total'], width=0, height=0, use_container_width=True)

    # Format Total and Percentage for display
        df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)

        st.table(df_sorted.sort_index())

    else:
        st.write("No data available or API response is not in the expected format.")
