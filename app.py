import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Groww SIP Discovery Engine", layout="wide")

st.title("Groww SIP Discovery Engine 🔍")
st.markdown("### Internal PM Tool for Bulk Feedback Analysis")

api_key = st.text_input("Enter your Gemini API Key:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        sample_data = """Money deducted but not in app, pausing SIP.
Market crashed, I stopped my auto-pay.
Direct MFs go down too much, no one warned me."""

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
                response = model.generate_content(prompt)
                st.markdown("### AI Categorization Results")
                st.markdown(response.text)
                st.success("Analysis complete.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your Gemini API key above to use the app.")
