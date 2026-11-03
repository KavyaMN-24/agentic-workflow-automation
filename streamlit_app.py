
import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000/workflow"

st.set_page_config(
    page_title="Business Workflow Agent",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Agentic Business Workflow Automation")
st.caption("AI-powered business analysis using Groq and Python tools")

st.markdown("---")

st.subheader("Ask your business analyst")

request = st.text_area(
    "Enter your business request:",
    value=(
        "Analyze the sales data in data/sample/sales.csv. "
        "Identify the best-performing product and region "
        "and summarize overall performance."
    ),
    height=120,
)

if st.button("Run Business Analysis", type="primary"):
    if len(request.strip()) < 5:
        st.warning("Please enter a longer request.")
    else:
        with st.spinner("Agent is analyzing your request..."):
            try:
                response = httpx.post(
                    API_URL,
                    json={"request": request},
                    timeout=120.0,
                )
                response.raise_for_status()

                result = response.json()

                st.success("Analysis completed successfully!")

                st.subheader("Business Analysis Report")
                st.markdown(result["report"])

            except httpx.HTTPStatusError as error:
                st.error(
                    f"API error: {error.response.status_code}"
                )
            except httpx.RequestError:
                st.error(
                    "Cannot connect to the API. "
                    "Make sure the FastAPI server is running."
                )

st.markdown("---")
st.caption("Powered by Python, FastAPI, Streamlit and Groq")

