import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.datasets import make_blobs, make_moons, make_classification, make_regression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def show():
    st.header("7. Machine Learning Basics")
    st.markdown("Visualize fundamental ML algorithms and understand hyperparameters.")

    algo = st.selectbox("Select Mode", ["Classification (KNN)", "Clustering (K-Means)", "Hyperparameter Tuning (Surface Plot)"])

    if algo == "Classification (KNN)":
        st.subheader("KNN Visualization")

        n_neighbors = st.slider("Number of Neighbors (K)", 1, 15, 3)
        dataset_type = st.radio("Dataset Shape", ["Blobs", "Moons"])

        if dataset_type == "Blobs":
            X, y = make_blobs(n_samples=200, centers=2, random_state=42, cluster_std=2.0)
        else:
            X, y = make_moons(n_samples=200, noise=0.2, random_state=42)

        clf = KNeighborsClassifier(n_neighbors=n_neighbors)
        clf.fit(X, y)

        # Create meshgrid for decision boundary
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                             np.arange(y_min, y_max, 0.1))

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        fig = go.Figure()
        fig.add_trace(go.Contour(x=np.arange(x_min, x_max, 0.1), y=np.arange(y_min, y_max, 0.1), z=Z,
                                 opacity=0.3, showscale=False, colorscale='Viridis'))
        fig.add_trace(go.Scatter(x=X[:, 0], y=X[:, 1], mode='markers', marker=dict(color=y, colorscale='Viridis', line_width=1)))

        st.plotly_chart(fig)

    elif algo == "Clustering (K-Means)":
        st.subheader("K-Means Clustering")
        st.write("Unsupervised learning: finding groups in data.")

        k = st.slider("Number of Clusters (K)", 2, 8, 3)
        X, _ = make_blobs(n_samples=300, centers=4, cluster_std=1.0, random_state=42) # Data actually has 4 centers

        kmeans = KMeans(n_clusters=k, random_state=42)
        y_pred = kmeans.fit_predict(X)
        centroids = kmeans.cluster_centers_

        fig = px.scatter(x=X[:, 0], y=X[:, 1], color=y_pred.astype(str), title="Cluster Assignments")
        fig.add_scatter(x=centroids[:, 0], y=centroids[:, 1], mode='markers', marker=dict(size=15, color='black', symbol='x'), name='Centroids')

        st.plotly_chart(fig)

    elif algo == "Hyperparameter Tuning (Surface Plot)":
        st.subheader("3D Hyperparameter Optimization")
        st.markdown("See how changing **Max Depth** and **N Estimators** affects a Random Forest's accuracy.")

        if st.button("Generate Surface Plot"):
            # Generate a harder dataset
            X, y = make_classification(n_samples=500, n_features=10, n_informative=5, random_state=42)

            depths = range(1, 11, 2)
            estimators = range(10, 110, 20)

            results = []

            for d in depths:
                row = []
                for n in estimators:
                    rf = RandomForestClassifier(max_depth=d, n_estimators=n, random_state=42)
                    rf.fit(X, y)
                    acc = rf.score(X, y) # Training accuracy (overfitting potential)
                    row.append(acc)
                results.append(row)

            z_data = np.array(results)

            fig = go.Figure(data=[go.Surface(z=z_data, x=list(estimators), y=list(depths))])
            fig.update_layout(title="Accuracy Surface", scene=dict(
                    xaxis_title='N Estimators',
                    yaxis_title='Max Depth',
                    zaxis_title='Accuracy'),
                    width=700, height=700)
            st.plotly_chart(fig)
            st.info("Notice how increasing complexity (Depth & Estimators) increases training accuracy, potentially leading to overfitting.")

    if st.button("I understand ML Basics!"):
        st.session_state.xp += 30
        st.toast("30 XP Added! 🤖")
