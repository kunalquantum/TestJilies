import streamlit as st
import pandas as pd
import plotly.express as px
from utils import generate_random_data, get_iris_data

def show():
    st.header("1. Data Exploration & Visualization")
    st.markdown("Upload a dataset or generate one to explore relationships using interactive charts.")

    # Data Source Selection
    data_source = st.radio("Select Data Source:", ["Upload CSV", "Use Iris Dataset", "Generate Random Data"], horizontal=True)

    df = None

    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error reading file: {e}")
    elif data_source == "Use Iris Dataset":
        df = get_iris_data()
    elif data_source == "Generate Random Data":
        rows = st.slider("Number of Rows", 10, 500, 100)
        df = generate_random_data(rows=rows)

    if df is not None:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        st.subheader("Visualization Settings")

        col1, col2 = st.columns(2)

        with col1:
            chart_type = st.selectbox("Chart Type", ["Scatter Plot", "Histogram", "Bar Chart", "Box Plot"])

        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        all_cols = df.columns.tolist()

        if chart_type == "Scatter Plot":
            with col2:
                x_axis = st.selectbox("X Axis", numeric_cols, index=0 if len(numeric_cols) > 0 else 0)
                y_axis = st.selectbox("Y Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                color_col = st.selectbox("Color By (Optional)", [None] + all_cols)

            if x_axis and y_axis:
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, title=f"{y_axis} vs {x_axis}")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Histogram":
            with col2:
                x_axis = st.selectbox("Variable", numeric_cols)
                bins = st.slider("Number of Bins", 5, 50, 20)

            if x_axis:
                fig = px.histogram(df, x=x_axis, nbins=bins, title=f"Distribution of {x_axis}")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Bar Chart":
            with col2:
                x_axis = st.selectbox("X Axis (Categorical/Numeric)", all_cols)
                y_axis = st.selectbox("Y Axis (Numeric)", numeric_cols)

            if x_axis and y_axis:
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Box Plot":
            with col2:
                y_axis = st.selectbox("Y Axis (Numeric)", numeric_cols)
                x_axis = st.selectbox("Group By (Optional)", [None] + all_cols)

            if y_axis:
                fig = px.box(df, y=y_axis, x=x_axis, title=f"Box Plot of {y_axis}")
                st.plotly_chart(fig, use_container_width=True)

        # Gamification: Award XP for exploring
        if st.button("I explored this data!"):
            st.session_state.xp += 10
            st.toast("You gained 10 XP for exploring data! 🎉")
