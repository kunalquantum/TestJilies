import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as stats
import pandas as pd

def show():
    st.header("4. Inferential Statistics")
    st.markdown("Bridge the gap between sample data and population parameters.")

    mode = st.selectbox("Choose Concept", ["Sampling Methods (Random vs Stratified)", "Central Limit Theorem", "Confidence Intervals", "A/B Testing"])

    if mode == "Sampling Methods (Random vs Stratified)":
        st.subheader("Random vs Stratified Sampling")
        st.write("Compare how sampling methods affect bias when the population has distinct groups (strata).")

        # Create a synthetic population with two groups
        st.write("### Population: 10,000 People (Students vs Professionals)")
        st.write("Group A (Students): Mean Income = $20k")
        st.write("Group B (Professionals): Mean Income = $80k")
        st.write("Population Mix: 10% Professionals, 90% Students")

        # Parameters
        n_students = 9000
        n_pros = 1000
        total_pop = n_students + n_pros

        pop_students = np.random.normal(20000, 5000, n_students)
        pop_pros = np.random.normal(80000, 15000, n_pros)
        population = np.concatenate([pop_students, pop_pros])

        true_mean = np.mean(population)
        st.metric("True Population Mean Income", f"${true_mean:,.2f}")

        st.divider()

        sample_size = st.slider("Sample Size", 50, 500, 100)

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Simple Random Sampling")
            if st.button("Take Random Sample"):
                sample = np.random.choice(population, sample_size, replace=False)
                sample_mean = np.mean(sample)
                error = abs(sample_mean - true_mean)
                st.metric("Random Sample Mean", f"${sample_mean:,.2f}", delta=f"{sample_mean-true_mean:.2f}")
                st.write(f"Error: ${error:,.2f}")

        with c2:
            st.subheader("Stratified Sampling")
            st.write("Samples proportionally from each group (90% Students, 10% Pros).")
            if st.button("Take Stratified Sample"):
                # Calculate strata sizes based on population proportion
                n_sample_students = int(sample_size * (n_students / total_pop))
                n_sample_pros = sample_size - n_sample_students

                s_students = np.random.choice(pop_students, n_sample_students, replace=False)
                s_pros = np.random.choice(pop_pros, n_sample_pros, replace=False)

                strat_sample = np.concatenate([s_students, s_pros])
                strat_mean = np.mean(strat_sample)
                error = abs(strat_mean - true_mean)

                st.metric("Stratified Sample Mean", f"${strat_mean:,.2f}", delta=f"{strat_mean-true_mean:.2f}")
                st.write(f"Error: ${error:,.2f}")

    elif mode == "Central Limit Theorem":
        st.subheader("Central Limit Theorem (CLT) Visualization")
        st.write("See how the distribution of sample means becomes normal, regardless of the population distribution.")

        pop_type = st.selectbox("Population Distribution", ["Uniform", "Exponential", "Bimodal"])
        sample_size = st.slider("Sample Size (n)", 2, 100, 30)
        num_simulations = st.slider("Number of Simulations", 100, 2000, 500)

        if st.button("Run Simulation"):
            # Generate Population
            if pop_type == "Uniform":
                pop_data = np.random.uniform(0, 10, 10000)
            elif pop_type == "Exponential":
                pop_data = np.random.exponential(scale=2, size=10000)
            else:
                pop_data = np.concatenate([np.random.normal(2, 1, 5000), np.random.normal(8, 1, 5000)])

            # Sample Means
            means = []
            for _ in range(num_simulations):
                sample = np.random.choice(pop_data, sample_size)
                means.append(np.mean(sample))

            # Plot
            fig = ff.create_distplot([means], group_labels=['Sample Means'], bin_size=(max(means)-min(means))/20, show_hist=True, show_rug=False)
            fig.update_layout(title=f"Distribution of {num_simulations} Sample Means (n={sample_size})")
            st.plotly_chart(fig, use_container_width=True)

    elif mode == "Confidence Intervals":
        st.subheader("Confidence Interval Simulator")
        st.write("Visualize how often a confidence interval captures the true population mean.")

        ci_level = st.slider("Confidence Level (%)", 80, 99, 95)
        n_experiments = 20
        true_mean = 50
        true_std = 10
        n_samples = 30

        # Simulate experiments
        intervals = []
        captured = []

        z_score = stats.norm.ppf(1 - (1 - ci_level/100)/2)

        for i in range(n_experiments):
            sample = np.random.normal(true_mean, true_std, n_samples)
            x_bar = np.mean(sample)
            margin_of_error = z_score * (true_std / np.sqrt(n_samples))
            low = x_bar - margin_of_error
            high = x_bar + margin_of_error
            intervals.append((low, high, x_bar))
            captured.append(low <= true_mean <= high)

        # Plot
        fig = go.Figure()

        # Add true mean line
        fig.add_shape(type="line", x0=true_mean, y0=-1, x1=true_mean, y1=n_experiments,
                      line=dict(color="green", width=2, dash="dash"))

        for i, (low, high, x_bar) in enumerate(intervals):
            color = "blue" if captured[i] else "red"
            fig.add_trace(go.Scatter(x=[low, high], y=[i, i], mode='lines', line=dict(color=color)))
            fig.add_trace(go.Scatter(x=[x_bar], y=[i], mode='markers', marker=dict(color=color, size=5)))

        fig.update_layout(title=f"{ci_level}% Confidence Intervals for {n_experiments} Samples",
                          xaxis_title="Value", yaxis_title="Experiment ID", showlegend=False)
        st.plotly_chart(fig)
        st.write(f"In this run, **{sum(captured)}** out of **{n_experiments}** intervals captured the true mean.")

    elif mode == "A/B Testing":
        st.subheader("A/B Testing Simulator")
        st.write("Test if Variant B converts better than Variant A.")

        col1, col2 = st.columns(2)
        with col1:
            conv_a = st.slider("True Conversion Rate A", 0.01, 0.50, 0.10)
        with col2:
            conv_b = st.slider("True Conversion Rate B", 0.01, 0.50, 0.12)

        sample_size = st.number_input("Sample Size per Group", 100, 10000, 1000)

        if st.button("Run A/B Test"):
            # Simulate data
            conversions_a = np.random.binomial(n=1, p=conv_a, size=sample_size)
            conversions_b = np.random.binomial(n=1, p=conv_b, size=sample_size)

            obs_a = np.mean(conversions_a)
            obs_b = np.mean(conversions_b)

            # T-test
            t_stat, p_val = stats.ttest_ind(conversions_a, conversions_b)

            st.metric("Observed Rate A", f"{obs_a:.2%}")
            st.metric("Observed Rate B", f"{obs_b:.2%}", delta=f"{(obs_b-obs_a):.2%}")

            st.write(f"**P-Value:** {p_val:.4f}")
            if p_val < 0.05:
                st.success("Result is Statistically Significant! (p < 0.05)")
            else:
                st.warning("Result is NOT Statistically Significant.")

    if st.button("I learned inference!"):
        st.session_state.xp += 25
        st.toast("25 XP Added! 📈")
