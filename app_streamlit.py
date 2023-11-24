import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import base64

# Web App Title
st.markdown('''
# **The EDA App**

This is the **EDA App** created in Streamlit using the **ydata-profiling** library.

**** App built in `Python` + `Streamlit` 

---
''')

# Function to generate download link for the CSV file
def get_table_download_link_csv(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="dataframe.csv">Download CSV File</a>'
    return href

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

# Pandas Profiling Report
if uploaded_file is not None:
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_file)
        return csv
    df = load_csv()

    # Display download link for the uploaded CSV
    st.markdown(get_table_download_link_csv(df), unsafe_allow_html=True)

    pr = ProfileReport(df, explorative=True)
    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)

    # Save report to HTML file
    report_html = pr.to_html()
    with open("report.html", "w") as f:
        f.write(report_html)

    # Download button for the report
    with open("report.html", "rb") as file:
        st.download_button(
            label="Download Report",
            data=file,
            file_name="pandas_profiling_report.html",
            mime="text/html"
        )
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        # Example data
        @st.cache
        def load_data():
            a = pd.DataFrame(
                np.random.rand(100, 5),
                columns=['a', 'b', 'c', 'd', 'e']
            )
            return a
        df = load_data()
        pr = ProfileReport(df, explorative=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)

        # Save report to HTML file
        report_html = pr.to_html()
        with open("report.html", "w") as f:
            f.write(report_html)

        # Download button for the report
        with open("report.html", "rb") as file:
            st.download_button(
                label="Download Report",
                data=file,
                file_name="pandas_profiling_report.html",
                mime="text/html"
            )
