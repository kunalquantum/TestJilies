import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from utils import get_housing_data

def show():
    st.header("9. Sandbox & Challenge Mode")
    st.markdown("### 🏠 Challenge: Predict Housing Prices")
    st.write("Real-world Scenario: You are a data scientist at a real estate agency. Can you build a model to predict house prices in California?")

    # 1. Load Data
    st.subheader("1. The Dataset")
    if 'housing_df' not in st.session_state:
        st.session_state.housing_df = get_housing_data()

    df = st.session_state.housing_df
    st.dataframe(df.head())
    st.write(f"Shape: {df.shape}")

    # 2. Select Features
    st.subheader("2. Feature Selection")
    target = 'Target_Price'
    features = df.columns.drop(target).tolist()

    selected_features = st.multiselect("Select features to train on:", features, default=['MedInc', 'HouseAge', 'AveRooms'])

    if not selected_features:
        st.warning("Please select at least one feature.")
        return

    # 3. Choose Model
    st.subheader("3. Choose Model")
    model_name = st.selectbox("Algorithm", ["Linear Regression", "Decision Tree", "Random Forest"])

    # Hyperparameters
    params = {}
    if model_name == "Decision Tree":
        params['max_depth'] = st.slider("Max Depth", 1, 20, 5)
    elif model_name == "Random Forest":
        params['n_estimators'] = st.slider("Number of Trees", 10, 100, 50)

    # 4. Train
    if st.button("Train Model 🚀"):
        X = df[selected_features]
        y = df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if model_name == "Linear Regression":
            model = LinearRegression()
        elif model_name == "Decision Tree":
            model = DecisionTreeRegressor(max_depth=params.get('max_depth'))
        elif model_name == "Random Forest":
            model = RandomForestRegressor(n_estimators=params.get('n_estimators'), random_state=42)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        st.success("Training Complete!")

        c1, c2 = st.columns(2)
        c1.metric("R2 Score (Accuracy)", f"{r2:.3f}")
        c2.metric("Mean Squared Error", f"{mse:.3f}")

        # Plot Prediction vs Actual
        fig = px.scatter(x=y_test, y=y_pred, labels={'x': 'Actual Price', 'y': 'Predicted Price'},
                         title="Actual vs Predicted Prices")
        fig.add_shape(type="line", x0=y.min(), y0=y.min(), x1=y.max(), y1=y.max(), line=dict(color="red", dash="dash"))
        st.plotly_chart(fig)

        if r2 > 0.6:
            st.balloons()
            st.success("Great model! You achieved an R2 score > 0.6!")
            if "Data Scientist" not in st.session_state.badges:
                st.session_state.badges.append("Data Scientist")
                st.session_state.xp += 50
                st.toast("Badge Unlocked: Data Scientist! 🎓")

    st.divider()
    st.write("### 🧪 Freeform Experiment")
    st.write("This sandbox is open for you to add your own experiments later!")
