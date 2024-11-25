import streamlit as st
import base64
import requests
import json

# Streamlit UI
st.title("PDF Style Extractor")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file:
    st.write("File uploaded successfully. Click 'Extract' to process.")

if st.button("Extract"):
    if uploaded_file:
        # Read and encode the uploaded file in base64
        pdf_bytes = uploaded_file.read()
        pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

        # Send the request to the Flask API
        api_url = "http://127.0.0.1:5000/process-pdf"  # Update with your API endpoint if different
        payload = {"file_base64": pdf_base64}

        # Spinner while processing
        with st.spinner("Processing..."):
            response = requests.post(api_url, json=payload)

        # Display the response
        if response.status_code == 200:
            try:
                # Ensure the response is parsed as JSON
                result = response.json()

                # Safely display JSON in the Streamlit app
                st.success("Extraction successful!")
                st.json(result)
            except json.JSONDecodeError:
                st.error("Failed to decode JSON response.")
                st.write("Response content:", response.text)  # Debugging fallback
        else:
            st.error(f"API Error: {response.status_code}")
            st.write("Response content:", response.text)
    else:
        st.error("Please upload a PDF file first.")
