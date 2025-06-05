import streamlit as st
from datetime import datetime, timedelta
import locale

# Session State initialisieren
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "today" not in st.session_state:
    st.session_state.today = datetime.today()

# Dummy-Tags für die Wochentage
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Task:
    def __init__(self, description, image_path, category, priority, date_beginn, date_end, done=False):
        self.description = description
        self.image_path = image_path
        self.category = category
        self.priority = priority
        self.date_beginn = date_beginn
        self.date_end = date_end
        self.done = done

    def mark_done(self):
        self.done = True

    def __repr__(self):
        return f"<Task {self.description} ({self.category}) due {self.due_date}>"


def setDate():
    # Optional: Sprache auf Deutsch setzen (klappt meist lokal, nicht immer in Web-Deployments)
    try:
        locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    except:
        pass  # fallback, falls nicht verfügbar
    
    start_of_week = st.session_state.today - timedelta(days=st.session_state.today.weekday())  # Montag
    end_of_week = start_of_week + timedelta(days=6)          # Sonntag

    # Formatierung: "26. Mai - 1. Juni 2025"
    return f"{start_of_week.strftime('%d. %B')} - {end_of_week.strftime('%d. %B %Y')}"

st.title("Task Manager")

columns = st.columns([1,1,15])
with columns[0]:
    if st.button("<"):
        st.session_state.today = st.session_state.today - timedelta(days=7)
with columns[1]:
    if st.button("\>"):
        st.session_state.today = st.session_state.today + timedelta(days=7)
with columns[2]:
    st.markdown(setDate())

cols = st.columns(7)
for i, weekday in enumerate(WEEKDAYS):
    cols[i].metric(label=WEEKDAYS[i], value="")

st.button("Task hinzufügen")