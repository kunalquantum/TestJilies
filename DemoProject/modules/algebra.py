import streamlit as st
import numpy as np
import plotly.graph_objects as go

def show():
    st.header("6. Algebra & Calculus Primer")
    st.markdown("Visualize vectors, matrices, and derivatives.")

    tab1, tab2 = st.tabs(["Linear Algebra (Vectors)", "Calculus (Derivatives)"])

    with tab1:
        st.subheader("Vector Addition Visualization")

        c1, c2 = st.columns(2)
        with c1:
            st.write("Vector A")
            ax = st.number_input("Ax", value=3.0)
            ay = st.number_input("Ay", value=2.0)
        with c2:
            st.write("Vector B")
            bx = st.number_input("Bx", value=-1.0)
            by = st.number_input("By", value=4.0)

        rx, ry = ax + bx, ay + by

        fig = go.Figure()
        # Draw A
        fig.add_trace(go.Scatter(x=[0, ax], y=[0, ay], mode='lines+markers', name='Vector A', line=dict(color='blue', width=4)))
        # Draw B starting from A tip
        fig.add_trace(go.Scatter(x=[ax, rx], y=[ay, ry], mode='lines+markers', name='Vector B', line=dict(color='green', width=4)))
        # Draw Resultant
        fig.add_trace(go.Scatter(x=[0, rx], y=[0, ry], mode='lines+markers', name='Resultant (A+B)', line=dict(color='red', width=4, dash='dash')))

        max_val = max(abs(ax), abs(ay), abs(bx), abs(by), abs(rx), abs(ry)) + 2
        fig.update_layout(xaxis_range=[-max_val, max_val], yaxis_range=[-max_val, max_val],
                          width=600, height=600, showlegend=True, title="Visualizing A + B")
        st.plotly_chart(fig)

    with tab2:
        st.subheader("Interactive Derivative Explorer")
        st.write("See the tangent line (slope) at any point on the curve $f(x) = x^2$")

        x_val = st.slider("Select X value", -5.0, 5.0, 1.0, 0.1)

        # Function: x^2
        x = np.linspace(-6, 6, 100)
        y = x**2

        # Tangent at x_val: y = f'(a)(x-a) + f(a)
        # f'(x) = 2x
        slope = 2 * x_val
        y_val = x_val**2

        # Tangent line equation
        tangent_y = slope * (x - x_val) + y_val

        fig_calc = go.Figure()
        fig_calc.add_trace(go.Scatter(x=x, y=y, name="f(x)=x^2"))
        fig_calc.add_trace(go.Scatter(x=x, y=tangent_y, name=f"Tangent at x={x_val}", line=dict(dash='dot')))
        fig_calc.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='markers', marker=dict(size=10, color='red'), name='Point'))

        fig_calc.update_layout(yaxis_range=[-5, 30], title=f"Slope (Derivative) = {slope:.2f}")
        st.plotly_chart(fig_calc)

    if st.button("I played with Math!"):
        st.session_state.xp += 15
        st.toast("15 XP Added! 📐")
