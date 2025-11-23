import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor
from utils import get_housing_data

def show():
    st.header("9. Sandbox & Challenge Mode")

    mode = st.radio("Mode Selection", ["Manual Sandbox", "AutoML Challenge (New!)"], horizontal=True)

    if 'housing_df' not in st.session_state:
        st.session_state.housing_df = get_housing_data()
    df = st.session_state.housing_df

    if mode == "Manual Sandbox":
        st.markdown("### 🏠 Challenge: Predict Housing Prices")
        st.write("Real-world Scenario: You are a data scientist at a real estate agency. Can you build a model to predict house prices in California?")

        # 1. Dataset Preview
        st.dataframe(df.head())

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
        model_name = st.selectbox("Algorithm", ["Linear Regression", "Decision Tree", "Random Forest", "XGBoost"])

        # Hyperparameters
        params = {}
        if model_name == "Decision Tree":
            params['max_depth'] = st.slider("Max Depth", 1, 20, 5)
        elif model_name == "Random Forest":
            params['n_estimators'] = st.slider("Number of Trees", 10, 100, 50)
        elif model_name == "XGBoost":
            params['learning_rate'] = st.slider("Learning Rate", 0.01, 0.5, 0.1)

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
            elif model_name == "XGBoost":
                model = XGBRegressor(learning_rate=params.get('learning_rate'), random_state=42)

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

    elif mode == "AutoML Challenge (New!)":
        st.subheader("🤖 AutoML Leaderboard")
        st.markdown("Let the computer do the work! Automatically train multiple models and find the best one.")

        target = 'Target_Price'
        features = df.columns.drop(target).tolist()

        st.write("Target Variable: **House Price**")
        st.write(f"Training on {len(features)} features: {', '.join(features)}")

        if st.button("Run AutoML Pipeline 🏎️"):
            X = df[features]
            y = df[target]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            models = {
                "Linear Regression": LinearRegression(),
                "Decision Tree (Depth=5)": DecisionTreeRegressor(max_depth=5),
                "Random Forest (n=50)": RandomForestRegressor(n_estimators=50, random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "XGBoost": XGBRegressor(n_jobs=1, random_state=42)
            }

            results = []

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, (name, model) in enumerate(models.items()):
                status_text.text(f"Training {name}...")
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                r2 = r2_score(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)

                results.append({
                    "Model": name,
                    "R2 Score": r2,
                    "MSE": mse,
                    "MAE": mae,
                    "Object": model
                })
                progress_bar.progress((i + 1) / len(models))

            status_text.text("Training Complete!")
            progress_bar.empty()

            # Display Leaderboard
            results_df = pd.DataFrame(results).sort_values(by="R2 Score", ascending=False)
            st.write("### 🏆 Model Leaderboard")
            st.dataframe(results_df.drop(columns=["Object"]).style.highlight_max(axis=0, subset=["R2 Score"]))

            # Visualize Best Model
            best_model_name = results_df.iloc[0]['Model']
            best_r2 = results_df.iloc[0]['R2 Score']
            st.success(f"The best model is **{best_model_name}** with R2 = {best_r2:.3f}")

            best_model = results_df.iloc[0]['Object']
            y_pred_best = best_model.predict(X_test)

            # Residual Plot
            residuals = y_test - y_pred_best
            fig_res = px.scatter(x=y_pred_best, y=residuals, labels={'x': 'Predicted', 'y': 'Residuals'},
                                 title=f"Residual Plot ({best_model_name})")
            fig_res.add_hline(y=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig_res)

            # Feature Importance (if applicable)
            if hasattr(best_model, 'feature_importances_'):
                st.subheader("Feature Importance")
                fi = pd.DataFrame({
                    'Feature': features,
                    'Importance': best_model.feature_importances_
                }).sort_values(by='Importance', ascending=False)

                fig_fi = px.bar(fi, x='Importance', y='Feature', orientation='h', title="Feature Importance")
                st.plotly_chart(fig_fi)

            st.session_state.xp += 100
            st.toast("100 XP Gained for running AutoML!")

    st.divider()
    st.write("### 🧪 Freeform Experiment")
    st.write("This sandbox is open for you to add your own experiments later!")
