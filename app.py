import streamlit as st
import pandas as pd

st.set_page_config(page_title="Task Management Dashboard", layout="wide")

st.title("Mindful Task Management")

tab1, tab2 = st.tabs(["Profile & Task Creation", "Task Organization"])

with tab1:
    st.header("Your Growth Profile")
    
    skill_areas = [
        "Planning", "Organizing", "Prioritizing", "Focusing",
        "Starting Tasks", "Completing Tasks", "Managing Time", "Adapting to Changes"
    ]
    
    cols = st.columns(2)
    profile = {}
    for i, skill in enumerate(skill_areas):
        with cols[i % 2]:
            strength = st.checkbox(f"{skill} (Strength)", key=f"strength_{i}")
            growth = st.checkbox(f"{skill} (Growth)", key=f"growth_{i}")
            profile[skill] = "Strength" if strength else ("Growth" if growth else "Neither")
    
    st.subheader("Preferred Task Visualization")
    visualization = st.selectbox("Choose a visualization method", 
                                 ["List View", "Kanban Board", "Calendar View", "Get Ready, Do, Done", "Priority Matrix", "Mind Map"])
    
    st.subheader("Reminder Connections")
    reminder_options = ["Google", "Apple", "Microsoft"]
    reminders = st.multiselect("Select reminder connections", reminder_options)
    
    st.header("Create Your Task List")
    task_input = st.text_area("What would you like to accomplish? List your tasks here, one per line.")
    task_type = st.selectbox("Select what type of task list we are completing:",
                             ["Daily Tasks", "Weekly Goals", "Long-term Project", "Recurring Responsibilities", "Quick To-Dos", "Other"])
    
    if task_type == "Other":
        other_type = st.text_input("Specify list type")
    
    if st.button("Create Task List"):
        st.session_state.tasks = task_input.split('\n')
        st.session_state.task_type = task_type

with tab2:
    st.header("Organize Your Tasks")
    
    if 'tasks' not in st.session_state:
        st.warning("Please create a task list in the Profile & Task Creation tab first.")
    else:
        tasks_df = pd.DataFrame({
            "Task": st.session_state.tasks,
            "Motivation": [1] * len(st.session_state.tasks),
            "Importance": [1] * len(st.session_state.tasks),
            "Urgency": [1] * len(st.session_state.tasks),
            "Est. Time (min)": [30] * len(st.session_state.tasks),
            "Difficulty": [1] * len(st.session_state.tasks),
            "Dependencies": [""] * len(st.session_state.tasks),
            "Deadline": [""] * len(st.session_state.tasks)
        })
        
        edited_df = st.data_editor(tasks_df, num_rows="dynamic")
        
        st.subheader("Priority Matrix")
        cols = st.columns(2)
        with cols[0]:
            st.write("Urgent and Important")
            st.write(edited_df[(edited_df['Urgency'] > 2) & (edited_df['Importance'] > 2)]['Task'].tolist())
        with cols[1]:
            st.write("Important, Not Urgent")
            st.write(edited_df[(edited_df['Urgency'] <= 2) & (edited_df['Importance'] > 2)]['Task'].tolist())
        with cols[0]:
            st.write("Urgent, Not Important")
            st.write(edited_df[(edited_df['Urgency'] > 2) & (edited_df['Importance'] <= 2)]['Task'].tolist())
        with cols[1]:
            st.write("Neither Urgent Nor Important")
            st.write(edited_df[(edited_df['Urgency'] <= 2) & (edited_df['Importance'] <= 2)]['Task'].tolist())