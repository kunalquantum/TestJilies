import streamlit as st

def show():
    st.header("8. Progress Tracking & Badges")
    st.markdown("Track your learning journey!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total XP", st.session_state.xp)

    with col2:
        st.write("### 🏆 Your Badges")
        if st.session_state.badges:
            for badge in st.session_state.badges:
                st.success(f"🏅 {badge}")
        else:
            st.info("No badges yet. Complete modules to earn them!")

    st.divider()

    # Levels
    level = st.session_state.xp // 100 + 1
    st.subheader(f"Current Level: {level}")

    progress_to_next = st.session_state.xp % 100
    st.progress(progress_to_next / 100)
    st.caption(f"{progress_to_next}/100 XP to Level {level + 1}")

    st.write("### 🎯 Achievements Guide")
    st.write("- **Explorer:** 10 XP (Data Exploration)")
    st.write("- **Stats Novice:** 20 XP + Badge (Descriptive Stats)")
    st.write("- **Chance Master:** 15 XP (Probability)")
    st.write("- **Inference Pro:** 25 XP (Inferential Stats)")
    st.write("- **Predictor:** 20 XP (Regression)")
    st.write("- **Math Whiz:** 15 XP (Algebra)")
    st.write("- **ML Engineer:** 30 XP (ML Basics)")
