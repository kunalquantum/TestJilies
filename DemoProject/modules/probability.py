import streamlit as st
import random
import plotly.express as px
import pandas as pd
import numpy as np

def show():
    st.header("3. Probability")
    st.markdown("Simulate probability experiments to understand randomness and distributions.")

    tab1, tab2 = st.tabs(["🪙 Coin Flips", "🎲 Dice Rolls"])

    with tab1:
        st.subheader("Coin Flip Simulator")
        st.write("Understand the Law of Large Numbers by flipping coins.")

        col1, col2 = st.columns([1, 2])

        with col1:
            flips = st.slider("Number of Flips", 10, 10000, 100, step=10, key="coin_flips")
            if st.button("Flip Coins!"):
                results = ['Heads' if random.random() < 0.5 else 'Tails' for _ in range(flips)]
                df = pd.DataFrame(results, columns=['Result'])
                counts = df['Result'].value_counts(normalize=True).reset_index()
                counts.columns = ['Result', 'Proportion']

                st.session_state['coin_df'] = counts
                st.session_state['coin_total'] = flips

        with col2:
            if 'coin_df' in st.session_state:
                fig = px.bar(st.session_state['coin_df'], x='Result', y='Proportion',
                             title=f"Results of {st.session_state['coin_total']} Flips",
                             range_y=[0, 1])
                # Add a line for theoretical probability
                fig.add_hline(y=0.5, line_dash="dash", annotation_text="Theoretical (0.5)")
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Dice Roll Simulator")
        st.write("Visualize the uniform distribution of a fair die.")

        n_dice = st.slider("Number of Rolls", 10, 5000, 100, key="dice_rolls")

        if st.button("Roll Dice"):
            rolls = np.random.randint(1, 7, n_dice)
            df_dice = pd.DataFrame(rolls, columns=['Value'])
            counts = df_dice['Value'].value_counts(normalize=True).sort_index()

            fig = px.bar(x=counts.index, y=counts.values,
                         labels={'x': 'Die Face', 'y': 'Frequency'},
                         title=f"Distribution of {n_dice} Dice Rolls")
            fig.add_hline(y=1/6, line_dash="dash", annotation_text="Theoretical (0.166)")
            st.plotly_chart(fig)

    st.info("Notice how increasing the sample size makes the results closer to the theoretical probability!")

    if st.button("I understand randomness!"):
        st.session_state.xp += 15
        st.toast("15 XP Added! 🎲")
