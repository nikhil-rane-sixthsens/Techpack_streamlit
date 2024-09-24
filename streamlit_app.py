import streamlit as st
import requests

def main():
    st.title("Techpack API")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    print(uploaded_file)
    # Define a list of module names for the dropdown
    module_names = ["H&M", "Nordstrom", "Chico", "Walmart", "Carhartt"]
    # Use selectbox for module_name selection
    module_name = st.selectbox("Select the module name", module_names)

    if st.button("Upload and Process"):
        if uploaded_file is not None:
            files = {'file': uploaded_file}
            data = {'module_name': module_name}
            # Update the URL to your Flask endpoint
            response = requests.post('http://34.229.10.166:8000/upload', files=files, data=data)
            if response.status_code == 200:
                json_response = response.json()
                st.success("File processed successfully!")
                st.json(json_response)
            else:
                st.error("Failed to process file.")
                st.write(response.json())

if __name__ == "__main__":
    main()
