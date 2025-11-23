import streamlit as st
from modules import (
    data_exploration,
    descriptive_stats,
    probability,
    inferential_stats,
    regression,
    algebra,
    ml_basics,
    progress,
    sandbox
)

# Page configuration
st.set_page_config(
    page_title="Interactive Statistics & ML Learning Tool",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "# Interactive Learning Tool\nLearn statistics and ML through hands-on experiments."
    }
)

# Initialize Session State for Progress
if 'xp' not in st.session_state:
    st.session_state.xp = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []

def main():
    st.title("Interactive Statistics & ML Learning Tool 📊")

    # Sidebar Navigation
    st.sidebar.title("Navigation")

    # Display Mini-Profile
    st.sidebar.markdown(f"**XP:** {st.session_state.xp} | **Badges:** {len(st.session_state.badges)}")
    st.sidebar.divider()

    options = {
        "1. Data Exploration": data_exploration,
        "2. Descriptive Statistics": descriptive_stats,
        "3. Probability": probability,
        "4. Inferential Statistics": inferential_stats,
        "5. Regression & Correlation": regression,
        "6. Algebra & Calculus": algebra,
        "7. ML Basics": ml_basics,
        "8. Progress Tracking": progress,
        "9. Sandbox": sandbox
    }

    selection = st.sidebar.radio("Go to Module:", list(options.keys()))

    # Run the selected module
    module = options[selection]

    st.markdown("---")
    module.show()
    st.markdown("---")
    st.sidebar.markdown("---")
    st.sidebar.info("Select a module to begin learning!")

if __name__ == "__main__":
    main()
