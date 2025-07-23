import streamlit as st 
import pandas as pd

st.title("🧠 Leave Request Automation Bot")

df = pd.read_csv("employee_data.csv")

with st.form("leave_form"):
    name = st.text_input("Employee Name")
    leave_days = st.number_input("Leave Days", min_value=1, max_value=30)
    reason = st.text_area("Reason for Leave")
    submit = st.form_submit_button("Submit Request")

if submit:
    emp = df[df["Name"].str.lower() == name.lower()]
    if emp.empty:
        st.error("❌ Employee not found.")
    else:
        used = emp["Used Leaves"].values[0]
        total = emp["Total Leaves"].values[0]
        balance = total - used
        if leave_days <= balance:
            st.success(f"✅ Leave Approved. Remaining balance: {balance - leave_days}")
        else:
            st.error(f"❌ Rejected. Only {balance} leave(s) remaining.")
