import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict
import locale

st.set_page_config(layout="wide")

# Session State initialisieren
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "today" not in st.session_state:
    st.session_state.today = datetime.today()

if "start_of_week" not in st.session_state:
    st.session_state.start_of_week = datetime.today()

if "TASKS" not in st.session_state:
    st.session_state.TASKS = defaultdict(list)

# Dummy-Tags für die Wochentage
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class Category:
    def __init__(self, description, image_path):
        self.description = description
        self.image_path = image_path

    def __str__(self):
        return self.description  # Wichtig für die Anzeige im Selectbox-Menü

class Priority:
    def __init__(self, description, image_path):
        self.description = description
        self.image_path = image_path

    def __str__(self):
        return self.description  # Wichtig für die Anzeige im Selectbox-Menü

CATEGORY = {
    Category(description="Arbeit", image_path="data/category/buroklammer.png"),
    Category(description="Freizeit", image_path="data/category/gruppe.png"),
    Category(description="Uni/Schule", image_path="data/category/study.png"),
    Category(description="Sonstiges", image_path="data/category/zufallig.png")
}

PRIORITY = {
    Priority(description="P0", image_path="data/priority/green.png"),
    Priority(description="P1", image_path="data/priority/orange.png"),
    Priority(description="P2", image_path="data/priority/red.png")
}

class Task:
    def __init__(self, description, category, priority, date_beginn, date_end, done=False):
        self.description = description
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
    
    st.session_state.start_of_week = st.session_state.today - timedelta(days=st.session_state.today.weekday())  # Montag
    end_of_week = st.session_state.start_of_week + timedelta(days=6)          # Sonntag

    # Formatierung: "26. Mai - 1. Juni 2025"
    return f"{st.session_state.start_of_week.strftime('%d. %B')} - {end_of_week.strftime('%d. %B %Y')}"

@st.dialog("Task erstellen")
def createDialog():
    description = st.text_input(label="Beschreibung")
    category = st.selectbox(label="Kategorie", options=CATEGORY)
    priority = st.selectbox(label="Priorität", options=PRIORITY)
    date = st.date_input("Datum wählen", st.session_state.today)
    columns = st.columns([1,1])
    with columns[0]:
        startTime = st.time_input(label="Startzeit")
    with columns[1]:
        endTime = st.time_input("Endzeit", st.session_state.today + timedelta(minutes=30))
    done = st.checkbox("Task erledigt")
    if st.button("Erstellen", disabled=description.strip() == ""):
        dateAsText = (f"{date.day}/{date.month}/{date.year}")
        st.session_state.TASKS[dateAsText].append(Task(description, category, priority, startTime, endTime, done))
        st.rerun()
        st.text(dateAsText)

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
dateWeekday = st.session_state.start_of_week
for i, weekday in enumerate(WEEKDAYS):
    dateWeekday = dateWeekday + timedelta(days=i)
    with cols[i]:
        with st.container():
            st.markdown(f"### {weekday}")
            date = (f"{dateWeekday.day}/{dateWeekday.month}/{dateWeekday.year}")
            if date in st.session_state.TASKS.keys():
                for task in st.session_state.TASKS[date]:
                    st.write(task.description)
    dateWeekday = dateWeekday - timedelta(days=i)

if st.button("Task hinzufügen"):
    createDialog()