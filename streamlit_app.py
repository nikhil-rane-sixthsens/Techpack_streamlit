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
        api_url = "http://34.203.252.31/process-pdf"  # Update with your API endpoint if different
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

                # Extract style name and description from the result
                style_name = result.get("style_name", "Default Style Name")  # Replace with actual key if different
                article_description = result.get("description", "Default Description")  # Replace with actual key if different

                # Define the headers for the second API call
                headers = {
                    "Guid": "30a00b95-75f6-4fea-82a6-21512196363e",
                    "Productcatcode": "01"
                }

                # API URL for updating
                update_api_url = "https://coreapi.wfxondemand.com/Item/api/v1/Item/1000180673?callFrom=Item"

                # Update style name
                style_name_payload = {
                    "article_name": style_name,
                    "parentcolid": "article_name"
                }
                style_name_response = requests.put(update_api_url, headers=headers, json=style_name_payload)

                if style_name_response.status_code == 200:
                    st.success("Style name updated successfully!")
                else:
                    st.error(f"Failed to update style name: {style_name_response.status_code}")
                    st.write("Response content:", style_name_response.text)

                # Update article description
                article_description_payload = {
                    "article_description": article_description,
                    "parentcolid": "article_description"
                }
                article_description_response = requests.put(update_api_url, headers=headers, json=article_description_payload)

                if article_description_response.status_code == 200:
                    st.success("Article description updated successfully!")
                else:
                    st.error(f"Failed to update article description: {article_description_response.status_code}")
                    st.write("Response content:", article_description_response.text)
            
            except json.JSONDecodeError:
                st.error("Failed to decode JSON response.")
                st.write("Response content:", response.text)  # Debugging fallback
        else:
            st.error(f"API Error: {response.status_code}")
            st.write("Response content:", response.text)
    else:
        st.error("Please upload a PDF file first.")
