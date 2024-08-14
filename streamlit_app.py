import streamlit as st
import base64
import pandas as pd

st.set_page_config(layout='wide')

def get_base64_of_pdf(file):
    return base64.b64encode(file.read()).decode()

# Single file uploader for multiple files
uploaded_files = st.file_uploader('Upload Files', accept_multiple_files=True)

if uploaded_files:
    # Ensure there are at least two files uploaded
    if len(uploaded_files) >= 2:
        file_types = [uploaded_file.name.split('.')[-1].lower() for uploaded_file in uploaded_files]

        if all(file_type == 'pdf' for file_type in file_types):
            col1, col2 = st.columns(2)

            # Display the first PDF file in the first column
            with col1:
                st.write(f'{uploaded_files[0].name}')
                pdf_base64 = get_base64_of_pdf(uploaded_files[0])
                pdf_url = f"data:application/pdf;base64,{pdf_base64}"
                st.markdown(f'<iframe src="{pdf_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True)

            # Display the second PDF file in the second column
            with col2:
                st.write(f'{uploaded_files[1].name}')
                pdf_base64 = get_base64_of_pdf(uploaded_files[1])
                pdf_url = f"data:application/pdf;base64,{pdf_base64}"
                st.markdown(f'<iframe src="{pdf_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True)

        elif all(file_type == 'csv' for file_type in file_types):
            col1, col2 = st.columns(2)

            with col1:
                # Display the first uploaded file in the first column
                df1 = pd.read_csv(uploaded_files[0])
                st.write(f'This is {uploaded_files[0].name} in Column 1')
                SelectedColumn1 = st.selectbox('Dataframe 1 Columns', df1.columns.tolist())
                st.dataframe(df1)

            with col2:
                # Display the second uploaded file in the second column
                df2 = pd.read_csv(uploaded_files[1])
                st.write(f'This is {uploaded_files[1].name} in Column 2')
                SelectedColumn2 = st.selectbox('Dataframe 2 Columns', df2.columns.tolist())
                st.dataframe(df2)

            try:
                # Attempt to merge the dataframes on the selected columns
                df3 = pd.merge(df1, df2, how='outer', left_on=SelectedColumn1, right_on=SelectedColumn2)
                st.dataframe(df3)
            except Exception as e:
                # Handle the error and display a message to the user
                st.error(f"An error occurred during the merge: {str(e)}")
        elif all(file_type in ['xlsx','xls'] for file_type in file_types):
            # Handle Excel files
            col1, col2 = st.columns(2)
            with col1:
                excel_file1 = pd.ExcelFile(uploaded_files[0])
                sheet_names1 = excel_file1.sheet_names
                st.write(f'Sheets in {uploaded_files[0].name}:')
                st.write(sheet_names1)
                selected_sheet1 = st.selectbox('Select a sheet from File 1', sheet_names1)
                if selected_sheet1:
                    df1 = pd.read_excel(uploaded_files[0], sheet_name=selected_sheet1)
                    SelectedColumn1 = st.selectbox('Dataframe 1 Columns', df1.columns.tolist())
                    st.write(f'Contents of sheet: {selected_sheet1}')
                    st.dataframe(df1)

            with col2:
                excel_file2 = pd.ExcelFile(uploaded_files[1])
                sheet_names2 = excel_file2.sheet_names
                st.write(f'Sheets in {uploaded_files[1].name}:')
                st.write(sheet_names2)
                selected_sheet2 = st.selectbox('Select a sheet from File 2', sheet_names2)
                if selected_sheet2:
                    df2 = pd.read_excel(uploaded_files[1], sheet_name=selected_sheet2)
                    SelectedColumn2 = st.selectbox('Dataframe 2 Columns', df2.columns.tolist())
                    st.write(f'Contents of sheet: {selected_sheet2}')
                    st.dataframe(df2)

            try:
                df3 = pd.merge(df1, df2, how='outer', left_on=SelectedColumn1, right_on=SelectedColumn2)

                # Select columns to display in df3
                selected_columns = st.multiselect('Select columns to display in the merged dataframe',
                                                  df3.columns.tolist())
                if selected_columns:
                    st.dataframe(df3[selected_columns])
                else:
                    st.dataframe(df3)

            except Exception as e:
                st.error(f"An error occurred during the merge: {str(e)}")

        else:
            st.warning("Please upload files of the same type (either both PDFs or both CSVs/Excel files).")
    else:
        st.warning("Please upload at least two files.")