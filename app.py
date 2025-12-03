import streamlit as st

st.set_page_config(page_title="Futsal Rotation", layout="centered")
st.title("⚽ Futsal Team Rotation (Vest Colors)")


# Initialize session state
if "teams" not in st.session_state:
    st.session_state.teams = []
if "queue" not in st.session_state:
    st.session_state.queue = []
if "history" not in st.session_state:
    st.session_state.history = []


st.subheader("Enter Vest Colors")
colors_input = st.text_area(
    "Type each team color on a new line:",
    placeholder="Example:\nRed\nBlue\nGreen\nYellow"
)

# Create teams (one color = one team)
if st.button("Start Rotation"):
    colors = [c.strip() for c in colors_input.splitlines() if c.strip()]

    if len(colors) < 2:
        st.error("You need at least 2 teams.")
    else:
        st.session_state.teams = colors
        st.session_state.queue = list(range(len(colors)))
        st.session_state.history = []
        st.success("Rotation started!")


# If teams exist, show current match
if st.session_state.queue:

    queue = st.session_state.queue
    teams = st.session_state.teams

    # Current match: two teams in front of the queue
    if len(queue) >= 2:
        a_idx, b_idx = queue[0], queue[1]

        st.subheader("Current Match")
        colA, colB = st.columns(2)
        with colA:
            st.markdown(f"### Team A\n**{teams[a_idx]}**")
        with colB:
            st.markdown(f"### Team B\n**{teams[b_idx]}**")

        st.divider()

        st.subheader("Match Result")

        col1, col2, col3 = st.columns(3)

        # Team A wins
        if col1.button("🏆 Team A Won"):
            st.session_state.history.append(
                (teams[a_idx], teams[b_idx], "Team A Won")
            )
            # Winner stays, loser moves to end
            new_queue = queue[1:] + [queue[0]]
            st.session_state.queue = new_queue

        # Team B wins
        if col2.button("🏆 Team B Won"):
            st.session_state.history.append(
                (teams[a_idx], teams[b_idx], "Team B Won")
            )
            # Bring B to front, A moves to end
            new_queue = queue[2:] + [queue[0]] + [queue[1]]
            st.session_state.queue = new_queue

        # Both lost
        if col3.button("❌ Both Lost"):
            st.session_state.history.append(
                (teams[a_idx], teams[b_idx], "Both Lost")
            )
            # Remove A and B, add both to end
            new_queue = queue[2:] + [a_idx, b_idx]
            st.session_state.queue = new_queue

        st.divider()

        # Show upcoming match
        if len(st.session_state.queue) >= 2:
            next_A = teams[st.session_state.queue[0]]
            next_B = teams[st.session_state.queue[1]]

            st.subheader("Next Match")
            st.write(f"**{next_A}** vs **{next_B}**")

        # Show team after that
        if len(st.session_state.queue) >= 3:
            st.subheader("Team Waiting")
            st.write(teams[st.session_state.queue[2]])


# Match History
if st.session_state.history:
    st.subheader("Match History")
    for i, match in enumerate(st.session_state.history, 1):
        teamA, teamB, result = match
        st.write(f"**Match {i}:** {teamA} vs {teamB} → **{result}**")
