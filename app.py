import streamlit as st
import pandas as pd
import dateparser
import re

st.set_page_config(page_title="Chat Leave Bot", layout="centered")
st.title("🤖 Watsonx-style Chat Leave Assistant")

# Load employee data
try:
    df = pd.read_csv("employee_data.csv")
except FileNotFoundError:
    st.error("⚠️ 'employee_data.csv' not found.")
    st.stop()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "employee_name" not in st.session_state:
    st.session_state.employee_name = None

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Type something like: I want leave from August 5 to 7")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    response = ""

    # Extract name if not set
    if not st.session_state.employee_name:
        name_match = re.search(r"my name is (\w+)", user_input, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            emp = df[df["Name"].str.lower() == name.lower()]
            if emp.empty:
                response = f"❌ Sorry, I couldn’t find employee named '{name}'. Try again."
            else:
                st.session_state.employee_name = name
                response = f"✅ Welcome, {name.title()}! Now tell me your leave details."
        else:
            response = "👋 Hi! Before we proceed, please tell me your name like: 'My name is Aayush'."

    else:
        # If name is set, extract leave dates and reason
        emp = df[df["Name"].str.lower() == st.session_state.employee_name.lower()].iloc[0]
        used = emp["Used Leaves"]
        total = emp["Total Leaves"]
        balance = total - used

        # Parse dates
        dates = re.findall(r"(?:from|between)?\s*(\w+\s+\d{1,2})\s*(?:to|-)?\s*(\w+\s+\d{1,2})?", user_input, re.IGNORECASE)
        reason_match = re.search(r"for (.+)", user_input, re.IGNORECASE)

        if dates:
            start_date = dateparser.parse(dates[0][0])
            end_date = dateparser.parse(dates[0][1]) if dates[0][1] else start_date
            days_requested = (end_date - start_date).days + 1

            reason = reason_match.group(1) if reason_match else "No reason provided"

            if days_requested <= balance:
                response = (
                    f"✅ Leave Approved for {st.session_state.employee_name.title()} from "
                    f"{start_date.strftime('%b %d')} to {end_date.strftime('%b %d')} "
                    f"({days_requested} days). Reason: {reason}.\n"
                    f"🧾 Remaining leave balance: {balance - days_requested}"
                )
            else:
                response = (
                    f"❌ Not enough leave balance. You have only {balance} leave(s), "
                    f"but requested {days_requested} day(s)."
                )
        else:
            response = "📅 I couldn't understand the leave dates. Try saying: 'Leave from August 5 to August 7 for family function.'"

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
