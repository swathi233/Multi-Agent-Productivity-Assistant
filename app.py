import streamlit as st
import datetime
from agents import Agent
from auth import login, register
from db import engine
from models import Base
from tools.voice_tool import listen

# ---------------- INITIAL SETUP ----------------
Base.metadata.create_all(bind=engine)
agent = Agent()

st.set_page_config(page_title="🤖 AI Assistant", layout="wide")

# -------- STYLE --------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
button[kind="secondary"] {
    border-radius: 12px;
    height: 60px;
    font-size: 16px;
    font-weight: 500;
}
.login-card {
    max-width: 400px;
    margin: auto;
    padding: 30px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "voice_task" not in st.session_state:
    st.session_state.voice_task = ""

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

# ---------------- LOGIN / REGISTER PAGE ----------------
if not st.session_state.user:
    st.markdown("<h1 style='text-align: center;'>🤖 AI Assistant</h1>", unsafe_allow_html=True)
    st.caption("Login or create an account")

    auth_mode = st.radio("Select Option", ["Login", "Register"], horizontal=True)
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_mode == "Register":
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Create Account", use_container_width=True):
            user = register(username, password)

            if user:
                st.success("Account created!")
            else:
                st.error("Username already exists")
            if not username or not password:
                st.error("Please fill all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                register(username, password)
                st.success("Account created! Please login")

    else:  # LOGIN
        if st.button("Login", use_container_width=True):
            user = login(username, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome {user.username}")
                st.rerun()
            else:
                st.error("Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
else:
    user = st.session_state.user
    if not user:
        st.error("You must log in first!")
        st.stop()

    uid = user.id

    # Greeting
    hour = datetime.datetime.now().hour
    greeting = "☀️ Good Morning" if hour < 12 else "🌤 Good Afternoon" if hour < 18 else "🌙 Good Evening"
    st.title(f"{greeting}, {user.username}")

    # Sidebar Navigation
    options = ["🏠 Dashboard", "📌 Task", "📝 Notes", "🎂 Birthday", "📅 Meeting"]
    page = st.sidebar.radio("Navigation", options, index=options.index(st.session_state.page))
    st.session_state.page = page

    # ---------------- DASHBOARD ----------------
    if page == "🏠 Dashboard":
        st.subheader("Overview")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tasks", len(agent.get_tasks(uid)))
        col2.metric("Notes", len(agent.get_notes(uid)))
        col3.metric("Birthdays", len(agent.get_birthdays(uid)))
        col4.metric("Meetings", len(agent.get_meetings(uid)))

        st.markdown("### ⚡ Quick Actions")
        st.caption("Jump quickly to features")

        c1, c2, c3, c4 = st.columns(4)
        if c1.button("📌 Add Task", use_container_width=True):
            st.session_state.page = "📌 Task"
            st.rerun()
        if c2.button("📝 Write Note", use_container_width=True):
            st.session_state.page = "📝 Notes"
            st.rerun()
        if c3.button("📅 Meeting", use_container_width=True):
            st.session_state.page = "📅 Meeting"
            st.rerun()
        if c4.button("🎂 Birthday", use_container_width=True):
            st.session_state.page = "🎂 Birthday"
            st.rerun()

    # ---------------- TASK ----------------
    elif page == "📌 Task":
        st.subheader("📌 Task Manager")

        col1, col2 = st.columns([3, 1])
        with col1:
            task_input = st.text_input("Enter Task", value=st.session_state.voice_task)
        with col2:
            if st.button("🎤 Speak"):
                st.session_state.voice_task = listen()

        # Voice task
        if st.session_state.voice_task:
            st.info(f"🗣 You said: {st.session_state.voice_task}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Save Voice Task"):
                    st.success(agent.add_task(st.session_state.voice_task, None, uid))
                    st.session_state.voice_task = ""
                    st.rerun()
            with c2:
                if st.button("❌ Cancel"):
                    st.session_state.voice_task = ""

        # Manual task
        if st.button("➕ Add Task"):
            if task_input:
                st.success(agent.add_task(task_input, None, uid))
                st.session_state.voice_task = ""
                st.rerun()
            else:
                st.error("Enter a task")

        # Task list
        st.markdown("### 📂 Your Tasks")
        tasks = agent.get_tasks(uid)
        if not tasks:
            st.info("✨ No tasks yet. Add one above!")
        else:
            for t in tasks:
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.write(f"✔️ {t.title}")
                with col2:
                    if st.button("❌", key=f"del_{t.id}"):
                        agent.delete_task(t.id)
                        st.rerun()

    # ---------------- NOTES ----------------
    elif page == "📝 Notes":
        st.subheader("📝 Notes")
        note = st.text_area("Write your note")
        if st.button("💾 Save Note"):
            if note:
                st.success(agent.add_note(note, uid))
                st.rerun()
            else:
                st.error("Enter note")

        st.markdown("### 📂 Saved Notes")
        notes = agent.get_notes(uid)
        if not notes:
            st.info("No notes yet")
        else:
            for n in notes:
                st.write(f"🗒 {n.content}")

    # ---------------- BIRTHDAY ----------------
    elif page == "🎂 Birthday":
        st.subheader("🎂 Birthday Manager")
        name = st.text_input("Name")
        email = st.text_input("Email")
        date = st.date_input("Birthday").strftime("%Y-%m-%d")
        if st.button("🎉 Add Birthday"):
            if name and email:
                st.success(agent.add_birthday(name, email, date, uid))
                st.rerun()
            else:
                st.error("Fill all fields")

        st.markdown("### 🎁 Saved Birthdays")
        birthdays = agent.get_birthdays(uid)
        if not birthdays:
            st.info("No birthdays added")
        else:
            for b in birthdays:
                st.write(f"🎂 {b.name} — {b.date}")

    # ---------------- MEETING ----------------
    elif page == "📅 Meeting":
        st.subheader("📅 Schedule Meeting")
        email = st.text_input("Participant Email")
        subject = st.text_input("Subject")
        desc = st.text_area("Description")
        date = st.date_input("Date").strftime("%Y-%m-%d")
        time = st.text_input("Time")

        if st.button("📩 Create Meeting"):
            if email and subject:
                st.success(agent.add_meeting(email, subject, desc, date, time, uid))
                st.rerun()
            else:
                st.error("Fill required fields")

        st.markdown("### 📂 Meetings")
        meetings = agent.get_meetings(uid)
        if not meetings:
            st.info("No meetings scheduled")
        else:
            for m in meetings:
                st.write(f"📅 {m.subject} with {m.email}")