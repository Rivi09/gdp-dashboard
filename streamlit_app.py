import streamlit as st
import pandas as pd
from pathlib import Path

# Set up page config
st.set_page_config(page_title='Excel Data Dashboard', page_icon=':bar_chart:')

# Load Excel file
DATA_FILENAME = Path(__file__).parent / 'data/Discovery Awards.xlsx'
xls = pd.ExcelFile(DATA_FILENAME)

# Get sheet names
sheet_names = xls.sheet_names

# Sidebar - Select sheet
selected_sheet = st.sidebar.selectbox('Select a sheet:', sheet_names)

def load_data(sheet_name):
    """Load and clean data from the selected sheet."""
    df = xls.parse(sheet_name)
    df.columns = df.columns.astype(str)  # Ensure column names are strings
    return df

# Load selected sheet data
df = load_data(selected_sheet)

# Display dataset preview
st.header(f'Data Preview - {selected_sheet}')
st.dataframe(df.head(10))

# Show column filters if the dataset has valid columns
if not df.empty:
    st.sidebar.subheader('Filter Data')
    filter_columns = st.sidebar.multiselect('Select columns to filter:', df.columns)
    
    if filter_columns:
        filters = {}
        for col in filter_columns:
            unique_values = df[col].dropna().unique()
            selected_values = st.sidebar.multiselect(f'Filter {col}:', unique_values)
            if selected_values:
                filters[col] = selected_values
        
        for col, values in filters.items():
            df = df[df[col].isin(values)]

    # Display filtered data
    st.subheader('Filtered Data')
    st.dataframe(df)
    
    # Display summary statistics
    st.subheader('Summary Statistics')
    st.write(df.describe())
    
    # Visualization - Show bar charts and line charts for numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_columns:
        st.subheader('Data Visualization')
        selected_metric = st.selectbox('Select a column for visualization:', numeric_columns)
        
        st.subheader('Bar Chart')
        st.bar_chart(df[selected_metric])
        
        st.subheader('Line Chart')
        st.line_chart(df[selected_metric])
        
        st.subheader('Multiple Bar Charts')
        st.bar_chart(df[numeric_columns])
        
        st.subheader('Multiple Line Charts')
        st.line_chart(df[numeric_columns])
else:
    st.warning('No valid data available in this sheet.')
