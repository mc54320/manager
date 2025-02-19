import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# 设置页面标题和图标
st.set_page_config(page_title='BI Dashboard', page_icon='📊', layout='wide')

# 侧边栏：文件上传
st.sidebar.header("Upload your CSV or Excel file")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['csv', 'xlsx'])

# 侧边栏：颜色选择
color = st.sidebar.color_picker("Choose a primary color", "#1f77b4")

# 读取数据
def load_data(file):
    if file is not None:
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
    return None

data = load_data(uploaded_file)

# 显示数据表
if data is not None:
    st.write("### Preview of Uploaded Data")
    st.dataframe(data)
    
    # 选择列
    numeric_columns = data.select_dtypes(['number']).columns.tolist()
    
    if numeric_columns:
        x_axis = st.sidebar.selectbox("Select X-axis", numeric_columns)
        y_axis = st.sidebar.selectbox("Select Y-axis", numeric_columns)
        chart_type = st.sidebar.radio("Choose Chart Type", ['Bar Chart', 'Line Chart', 'Scatter Plot'])
        
        st.write("### Data Visualization")
        
        if chart_type == 'Bar Chart':
            fig = px.bar(data, x=x_axis, y=y_axis, color_discrete_sequence=[color])
        elif chart_type == 'Line Chart':
            fig = px.line(data, x=x_axis, y=y_axis, line_shape='linear', color_discrete_sequence=[color])
        else:
            fig = px.scatter(data, x=x_axis, y=y_axis, color_discrete_sequence=[color])
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No numeric columns found in the dataset.")
else:
    st.info("Please upload a file to get started.")
