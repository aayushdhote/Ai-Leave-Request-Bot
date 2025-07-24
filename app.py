import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="AI Leave Bot", layout="centered")
st.title("🧠 Leave Request Automation Bot")

# Load employee data
try:
    df = pd.read_csv("employee_data.csv")
except FileNotFoundError:
    st.error("⚠️ 'employee_data.csv' not found. Please upload the file to proceed.")
    st.stop()

# Optional: View employee list
with st.expander("📋 View Employee Data"):
    st.dataframe(df)

# Simulated leave history
leave_history = []

with st.form("leave_form"):
    name = st.text_input("👤 Employee Name")
    leave_days = st.number_input("📅 Leave Days", min_value=1, max_value=30)
    reason = st.text_area("✍️ Reason for Leave")
    submit = st.form_submit_button("✅ Submit Request")

if submit:
    emp = df[df["Name"].str.lower() == name.lower()]
    if emp.empty:
        st.error("❌ Employee not found.")
    else:
        used = emp["Used Leaves"].values[0]
        total = emp["Total Leaves"].values[0]
        balance = total - used

        st.info(f"🧾 Total Leaves: {total} | Used: {used} | Balance: {balance}")

        if leave_days <= balance:
            st.success(f"✅ Leave Approved. Remaining balance: {balance - leave_days}")
            # Add to leave history (in-memory for now)
            leave_history.append({
                "Name": name.title(),
                "Days": leave_days,
                "Reason": reason,
                "Status": "Approved"
            })
        else:
            st.error(f"❌ Rejected. Only {balance} leave(s) remaining.")
            leave_history.append({
                "Name": name.title(),
                "Days": leave_days,
                "Reason": reason,
                "Status": "Rejected"
            })

# Optional: View leave history
if leave_history:
    st.subheader("📜 Leave Request History")
    st.table(pd.DataFrame(leave_history))

    # Allow download as text
    if st.button("⬇️ Download Summary"):
        history_df = pd.DataFrame(leave_history)
        output = StringIO()
        history_df.to_csv(output, index=False)
        st.download_button("Download CSV", data=output.getvalue(), file_name="leave_summary.csv", mime="text/csv")
