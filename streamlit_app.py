import streamlit as st
import requests
import pandas as pd
import io

# Function to convert to a DataFrame
def convert_to_dataframe(data):
    # Prepare dataframes for each key
    dataframes = {}

    for key in data:
        rows = []
        for entry in data[key]:
            row = {"Client Pdf Fields": entry["Client Pdf Fields"], "WFX Fields": entry["WFX Fields"]}
            # Handling for cases where 'Values' is a list of dictionaries
            if isinstance(entry["Values"], list):
                for sub_entry in entry["Values"]:
                    row.update(sub_entry)  # Add all subfields as columns
            else:
                row["Values"] = entry["Values"]  # Add single value
            rows.append(row)

        # Create dataframe
        dataframes[key] = pd.DataFrame(rows)

    return dataframes

def json_to_excel(json_data):
    dataframes = convert_to_dataframe(json_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    output.seek(0)
    return output.read()

def main():
    st.title("Techpack API")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    # Define a list of module names for the dropdown
    module_names = ["Nordstrom", "Walmart", "Carhartt", "GAP", "Chico", "HNM"]
    # Use selectbox for module_name selection
    module_name = st.selectbox("Select the module name", module_names)

    if st.button("Upload and Process"):
        if uploaded_file is not None:
            with st.spinner("Processing..."):
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                data = {'module_name': module_name}
                # response = requests.post('http://localhost:5000/upload', files=files, data=data)
                response = requests.post('http://44.201.117.143/upload', files=files, data=data)
            if response.status_code == 200:
                json_response = response.json()
                st.success("File processed successfully!")
                json_data = json_response['json']
                print(json_data)
                # Convert JSON data to Excel
                excel_bytes = json_to_excel(json_data)
                st.download_button(label="Download Excel", data=excel_bytes, file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            else:
                st.error("Failed to process file.")
                st.write(response.json())

if __name__ == "__main__":
    main()
