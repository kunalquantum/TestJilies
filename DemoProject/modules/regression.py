import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression, LogisticRegression
from utils import generate_linear_data

def show():
    st.header("5. Regression & Correlation")
    st.markdown("Explore relationships between variables.")

    tab1, tab2 = st.tabs(["Linear Regression", "Logistic Regression"])

    with tab1:
        st.subheader("Interactive Linear Regression")
        st.write("Adjust the parameters of the data generation and see how the line fits.")

        col1, col2 = st.columns(2)
        with col1:
            noise = st.slider("Noise Level", 0.0, 50.0, 10.0)
            slope = st.slider("True Slope", -10.0, 10.0, 2.0)

        # Generate Data
        df = generate_linear_data(n_samples=200, noise=noise, slope=slope)

        # Fit Model
        model = LinearRegression()
        model.fit(df[['X']], df['y'])
        df['Prediction'] = model.predict(df[['X']])

        # Plot
        fig = px.scatter(df, x='X', y='y', opacity=0.6, title=f"y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}")
        fig.add_traces(go.Scatter(x=df['X'], y=df['Prediction'], mode='lines', name='Fit Line', line=dict(color='red')))
        st.plotly_chart(fig, use_container_width=True)

        st.write(f"**R-squared Score:** {model.score(df[['X']], df['y']):.4f}")

    with tab2:
        st.subheader("Logistic Regression (Classification)")
        st.write("See how a sigmoid curve fits binary data (0 or 1).")

        # Simple synthetic binary data
        x_log = np.linspace(-10, 10, 100)
        # Shift sigmoid
        bias = st.slider("Bias (Shift Curve)", -5.0, 5.0, 0.0)

        def sigmoid(x):
            return 1 / (1 + np.exp(-(x + bias)))

        # Generate noisy binary outcomes
        y_prob = sigmoid(x_log)
        y_class = [1 if p > np.random.rand() else 0 for p in y_prob]

        # Fit Logic Reg
        log_reg = LogisticRegression()
        log_reg.fit(x_log.reshape(-1, 1), y_class)

        # Plot
        fig_log = go.Figure()
        fig_log.add_trace(go.Scatter(x=x_log, y=y_class, mode='markers', name='Data', marker=dict(color='blue', opacity=0.5)))

        # Prediction curve
        x_range = np.linspace(-10, 10, 300).reshape(-1, 1)
        y_prob_pred = log_reg.predict_proba(x_range)[:, 1]
        fig_log.add_trace(go.Scatter(x=x_range.flatten(), y=y_prob_pred, mode='lines', name='Probability Curve', line=dict(color='red')))

        st.plotly_chart(fig_log, use_container_width=True)

    if st.button("I understand regression!"):
        st.session_state.xp += 20
        st.toast("20 XP Added! 📉")
