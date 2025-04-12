import streamlit as st
import time
import json
import os
from datetime import datetime

def load_scenarios():
    """Load patient scenarios from a JSON file."""
    # Check if the file exists, if not create it with sample data
    if not os.path.exists("data/scenarios.json"):
        sample_scenarios = [
            {
                "id": 1,
                "title": "Knee Pain Assessment",
                "description": "A 45-year-old patient presents with right knee pain that started 2 weeks ago.",
                "key_history_points": [
                    "Pain characteristics (location, type, severity)",
                    "Onset and duration",
                    "Aggravating and relieving factors",
                    "Previous injuries or conditions",
                    "Impact on daily activities",
                    "Previous treatments tried"
                ],
                "viva_questions": [
                    "What special tests would you perform for this patient?",
                    "What are the potential differential diagnoses?",
                    "Describe your treatment approach for this patient."
                ]
            },
            {
                "id": 2,
                "title": "Lower Back Pain Assessment",
                "description": "A 35-year-old office worker presents with lower back pain that has been persistent for 3 months.",
                "key_history_points": [
                    "Pain characteristics (location, type, severity)",
                    "Onset and duration",
                    "Work environment and ergonomics",
                    "Daily activities and exercise routine",
                    "Sleep patterns and positions",
                    "Previous treatments or investigations"
                ],
                "viva_questions": [
                    "What red flags would you look for in this case?",
                    "How would you differentiate between mechanical and non-mechanical back pain?",
                    "Explain your management plan for this patient."
                ]
            }
        ]
        os.makedirs("data", exist_ok=True)
        with open("data/scenarios.json", "w") as f:
            json.dump(sample_scenarios, f)
    
    # Load scenarios from file
    with open("data/scenarios.json", "r") as f:
        scenarios = json.load(f)
    return scenarios

def save_session_data(username, session_data):
    """Save the session data to the user's history."""
    history_file = f"data/user_history/{username}.json"
    os.makedirs("data/user_history", exist_ok=True)
    
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    else:
        history = []
    
    history.append(session_data)
    
    with open(history_file, "w") as f:
        json.dump(history, f)

def display_station1():
    st.title("Station 1: History Taking + VIVA")
    
    # Initialize session state variables if they don't exist
    if 'station1_phase' not in st.session_state:
        st.session_state.station1_phase = 'intro'
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'history_notes' not in st.session_state:
        st.session_state.history_notes = ""
    if 'checked_items' not in st.session_state:
        st.session_state.checked_items = []
    if 'viva_answers' not in st.session_state:
        st.session_state.viva_answers = {}
    if 'selected_scenario' not in st.session_state:
        scenarios = load_scenarios()
        if scenarios:
            st.session_state.selected_scenario = scenarios[0]  # Default to first scenario
        else:
            st.error("No scenarios available. Please add scenarios to the database.")
            return
    
    # Intro phase - select scenario and start
    if st.session_state.station1_phase == 'intro':
        scenarios = load_scenarios()
        scenario_titles = [s["title"] for s in scenarios]
        selected_title = st.selectbox("Select a scenario:", scenario_titles)
        
        for scenario in scenarios:
            if scenario["title"] == selected_title:
                st.session_state.selected_scenario = scenario
                break
        
        st.markdown("### Instructions:")
        st.markdown("1. You will have 7 minutes for history taking")
        st.markdown("2. Followed by 3 minutes for VIVA questions")
        st.markdown("3. Your responses will be saved for review")
        
        if st.button("Start Station 1"):
            st.session_state.station1_phase = 'history'
            st.session_state.start_time = time.time()
            st.rerun()
    
    # History taking phase
    elif st.session_state.station1_phase == 'history':
        scenario = st.session_state.selected_scenario
        elapsed_time = int(time.time() - st.session_state.start_time)
        remaining_time = max(0, 7 * 60 - elapsed_time)
        
        # Display timer
        mins, secs = divmod(remaining_time, 60)
        timer_text = f"{mins:02d}:{secs:02d}"
        st.markdown(f"<h2 style='text-align: center;'>History Taking: {timer_text}</h2>", unsafe_allow_html=True)
        
        # Display scenario
        st.markdown("### Patient Scenario")
        st.markdown(scenario["description"])
        
        # History taking checklist
        st.markdown("### Key History Points")
        for i, point in enumerate(scenario["key_history_points"]):
            key = f"history_point_{i}"
            checked = st.checkbox(point, key=key)
            if checked and key not in st.session_state.checked_items:
                st.session_state.checked_items.append(key)
        
        # Notes section
        st.markdown("### Your Notes")
        st.session_state.history_notes = st.text_area("Enter your notes here:", 
                                                     value=st.session_state.history_notes,
                                                     height=200)
        
        # Auto-transition after 7 minutes
        if remaining_time <= 0:
            st.session_state.station1_phase = 'viva'
            st.rerun()
            
        # Manual transition button
        if st.button("Proceed to VIVA"):
            st.session_state.station1_phase = 'viva'
            st.rerun()
    
    # VIVA phase
    elif st.session_state.station1_phase == 'viva':
        scenario = st.session_state.selected_scenario
        elapsed_time = int(time.time() - st.session_state.start_time)
        history_time = min(7 * 60, elapsed_time)  # Cap at 7 minutes
        viva_elapsed = elapsed_time - history_time
        remaining_time = max(0, 3 * 60 - viva_elapsed)
        
        # Display timer
        mins, secs = divmod(remaining_time, 60)
        timer_text = f"{mins:02d}:{secs:02d}"
        st.markdown(f"<h2 style='text-align: center;'>VIVA Session: {timer_text}</h2>", unsafe_allow_html=True)
        
        # Display VIVA questions
        st.markdown("### VIVA Questions")
        for i, question in enumerate(scenario["viva_questions"]):
            st.markdown(f"**Q{i+1}: {question}**")
            answer_key = f"viva_answer_{i}"
            st.session_state.viva_answers[answer_key] = st.text_area(
                f"Your answer to Q{i+1}:", 
                value=st.session_state.viva_answers.get(answer_key, ""),
                key=answer_key
            )
        
        # Auto-transition after 3 minutes of VIVA
        if remaining_time <= 0:
            st.session_state.station1_phase = 'summary'
            st.rerun()
            
        # Manual finish button
        if st.button("Finish Station"):
            st.session_state.station1_phase = 'summary'
            st.rerun()
    
    # Summary phase
    elif st.session_state.station1_phase == 'summary':
        st.markdown("## Station 1 Complete")
        st.markdown("### Summary")
        
        scenario = st.session_state.selected_scenario
        
        # Calculate performance metrics
        checked_points = len(st.session_state.checked_items)
        total_points = len(scenario["key_history_points"])
        history_percentage = (checked_points / total_points) * 100 if total_points > 0 else 0
        
        # Display metrics
        st.markdown(f"**History Taking Coverage:** {history_percentage:.1f}%")
        st.markdown(f"**Points Covered:** {checked_points}/{total_points}")
        
        # Display history notes
        st.markdown("### Your History Notes")
        st.text_area("", value=st.session_state.history_notes, height=150, disabled=True)
        
        # Display VIVA answers
        st.markdown("### Your VIVA Responses")
        for i, question in enumerate(scenario["viva_questions"]):
            answer_key = f"viva_answer_{i}"
            answer = st.session_state.viva_answers.get(answer_key, "")
            st.markdown(f"**Q{i+1}: {question}**")
            st.text_area("", value=answer, height=100, disabled=True, key=f"display_{answer_key}")
        
        # Save session data
        if st.button("Save Results"):
            username = st.session_state.get("username", "anonymous")
            session_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "scenario": scenario["title"],
                "history_coverage": history_percentage,
                "points_covered": checked_points,
                "total_points": total_points,
                "history_notes": st.session_state.history_notes,
                "viva_answers": st.session_state.viva_answers
            }
            save_session_data(username, session_data)
            st.success("Session results saved successfully!")
        
        # Return to dashboard
        if st.button("Return to Dashboard"):
            st.session_state.station1_phase = 'intro'
            st.session_state.history_notes = ""
            st.session_state.checked_items = []
            st.session_state.viva_answers = {}
            st.session_state.start_time = None
            # Navigate back to dashboard
            st.switch_page("pages/1_Dashboard.py")
