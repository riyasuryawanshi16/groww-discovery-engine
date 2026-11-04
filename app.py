import streamlit as st
import google.generativeai as genai

# Setup API Key (Make sure to add your GEMINI_API_KEY to Streamlit Secrets later)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please configure your GEMINI_API_KEY in Streamlit secrets.")

model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Groww SIP Discovery Engine", layout="wide")

st.title("Groww SIP Discovery Engine 🔍")
st.markdown("### Internal PM Tool for Bulk Feedback Analysis")
st.markdown("Paste raw user reviews below. The AI will categorize them into our core churn pillars: **Operational Void**, **Frictionless Panic**, or **Linear Growth Fallacy**.")

# Default sample data
sample_data = """Money deducted but not in app, pausing SIP.
Market crashed, I stopped my auto-pay.
Direct MFs go down too much, no one warned me.
Can't find the edit button, just canceled it."""

review_input = st.text_area("Paste Raw User Feedback (one per line):", value=sample_data, height=150)

if st.button("Analyze & Categorize Feedback"):
    with st.spinner("AI is processing user intent..."):
        prompt = f"""
        You are a Product Management AI Assistant. Categorize the following user reviews into one of these specific churn themes:
        1. Operational Void (Anxiety over settlement delays / T+1)
        2. Frictionless Panic (Pausing due to market dips / emotional control)
        3. Linear Growth Fallacy (Lack of human advisor / expectation mismatch)
        4. UI/UX Friction (Bugs, hard to find buttons)
        5. Financial Hardship (Job loss, medical bills)
        
        Reviews to analyze:
        {review_input}
        
        Output a clean Markdown table with the columns: [Raw Review] | [Identified Theme] | [Brief Rationale].
        """
        
        try:
            response = model.generate_content(prompt)
            st.markdown("### AI Categorization Results")
            st.markdown(response.text)
            st.success("Analysis complete. Ready for Evidence Log export.")
        except Exception as e:
            st.error(f"Error connecting to AI: {e}")
