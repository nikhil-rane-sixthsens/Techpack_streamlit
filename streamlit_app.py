import streamlit as st
import requests


def main():
    st.title("Techpack API")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    print(uploaded_file)
    module_name = st.text_input("Enter the module name", value="H&M, Nordstrom, Chico, Walmart, Carhartt")

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
