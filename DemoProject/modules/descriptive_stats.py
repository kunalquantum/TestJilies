import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

def show():
    st.header("2. Descriptive Statistics")
    st.markdown("Understand datasets through summary statistics: Mean, Median, Mode, Variance, and Standard Deviation.")

    # Educational Flashcards
    st.subheader("📚 Interactive Flashcards")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.expander("Mean (Average)"):
            st.write("**Definition:** The sum of all values divided by the number of values.")
            st.latex(r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i")
            st.info("Example: (1+2+3)/3 = 2")
    with c2:
        with st.expander("Median"):
            st.write("**Definition:** The middle value when data is ordered.")
            st.info("Example: 1, 3, 100 -> Median is 3 (robust to outliers!)")
    with c3:
        with st.expander("Standard Deviation"):
            st.write("**Definition:** A measure of the amount of variation or dispersion of a set of values.")
            st.latex(r"\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2}")

    st.divider()

    # Interactive Calculator
    st.subheader("🧮 Live Statistics Calculator")
    st.write("Edit the numbers below to see how statistics change in real-time.")

    input_str = st.text_area("Enter numbers separated by commas:", "10, 20, 20, 40, 50, 100")

    try:
        data_list = [float(x.strip()) for x in input_str.split(',') if x.strip()]
        if len(data_list) > 0:
            data = np.array(data_list)

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Mean", f"{np.mean(data):.2f}")
            col2.metric("Median", f"{np.median(data):.2f}")

            # Mode can be multiple, just show first or formatted
            mode_res = stats.mode(data, keepdims=True)
            mode_val = mode_res.mode[0] if len(mode_res.mode) > 0 else "N/A"
            col3.metric("Mode", f"{mode_val}")

            col4.metric("Variance", f"{np.var(data):.2f}")
            col5.metric("Std Dev", f"{np.std(data):.2f}")

            st.write("---")
            st.write("**Data Distribution:**")
            chart_data = pd.DataFrame(data, columns=["Value"])
            st.bar_chart(chart_data["Value"].value_counts().sort_index())

        else:
            st.warning("Please enter at least one number.")

    except ValueError:
        st.error("Invalid input. Please enter numbers separated by commas (e.g., 1, 2.5, 3).")

    if st.button("Complete Descriptive Stats Module"):
        st.session_state.xp += 20
        if "Stats Novice" not in st.session_state.badges:
            st.session_state.badges.append("Stats Novice")
            st.balloons()
            st.toast("Badge Unlocked: Stats Novice! 🏆")
        else:
            st.toast("You gained 20 XP!")
