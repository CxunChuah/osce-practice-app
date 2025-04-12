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
                "patient_details": {
                    "name": "John Smith",
                    "age": 45,
                    "gender": "Male",
                    "race": "Caucasian",
                    "occupation": "Office worker",
                    "diagnosis": "Suspected meniscal tear",
                    "management": "Referred for physiotherapy assessment",
                    "investigation": "X-ray negative for fracture",
                    "chief_complaint": "Right knee pain when walking and climbing stairs",
                    "patient_goal": "Return to recreational jogging"
                },
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
                "patient_details": {
                    "name": "Sarah Johnson",
                    "age": 35,
                    "gender": "Female",
                    "race": "Asian",
                    "occupation": "Software Developer",
                    "diagnosis": "Non-specific low back pain",
                    "management": "Referred for physiotherapy assessment",
                    "investigation": "MRI shows mild disc bulge at L4/L5",
                    "chief_complaint": "Lower back pain that worsens after long periods of sitting",
                    "patient_goal": "Work without pain and return to yoga classes"
                },
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

def format_time(seconds):
    """Format seconds into MM:SS display"""
    mins, secs = divmod(seconds, 60)
    return f"{mins:02d}:{secs:02d}"

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
    if 'subjective_data' not in st.session_state:
        st.session_state.subjective_data = {}
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
                # Initialize subjective data with empty values
                if scenario.get("patient_details"):
                    st.session_state.subjective_data = {k: "" for k in scenario["patient_details"].keys()}
                break
        
        st.markdown("### Instructions:")
        st.markdown("1. The history taking phase will be timed with a stopwatch")
        st.markdown("2. The VIVA questions phase will also be timed")
        st.markdown("3. Your responses will be saved for review")
        st.markdown("4. You'll start with a Subjective assessment (SOAPIER format)")
        
        if st.button("Start Station 1"):
            st.session_state.station1_phase = 'history'
            st.session_state.start_time = time.time()
            st.rerun()
    
    # History taking phase
    elif st.session_state.station1_phase == 'history':
        scenario = st.session_state.selected_scenario
        elapsed_time = int(time.time() - st.session_state.start_time)
        
        # Display stopwatch instead of countdown
        time_text = format_time(elapsed_time)
        st.markdown(f"<h2 style='text-align: center;'>History Taking: {time_text}</h2>", unsafe_allow_html=True)
        
        # Display scenario
        st.markdown("### Patient Scenario")
        st.markdown(scenario["description"])
        
        # Subjective assessment table (SOAPIER)
        st.markdown("### Subjective Assessment")
        
        # Create a two-column layout for the table
        col1, col2 = st.columns(2)
        
        # Define subjective components
        subjective_components = {
            "Name": "",
            "Age": "",
            "Gender": "",
            "Race": "",
            "Occupation": "",
            "Date of Assessment": datetime.now().strftime("%Y-%m-%d"),
            "Doctor's Diagnosis": "",
            "Doctor's Management": "",
            "Investigation": "",
            "Chief Complaint": "",
            "Patient's Goal": ""
        }
        
        # Display form fields for subjective data
        for i, (label, default_value) in enumerate(subjective_components.items()):
            with col1:
                st.markdown(f"**{label}:**")
            with col2:
                key = f"subj_{label.lower().replace(' ', '_').replace(''', '')}"
                
                # Use the patient details as placeholder hints if available
                placeholder = ""
                if scenario.get("patient_details"):
                    field_key = label.lower().replace(' ', '_').replace('\'s', '').replace('doctor\'s', 'doctor')
                    for scenario_key in scenario["patient_details"].keys():
                        if scenario_key.lower() == field_key:
                            placeholder = scenario["patient_details"][scenario_key]
                
                # Store input in session state
                st.session_state.subjective_data[key] = st.text_input(
                    "", 
                    key=key,
                    value=st.session_state.subjective_data.get(key, ""),
                    placeholder=placeholder
                )
        
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
        
        # Manual transition button
        if st.button("Proceed to VIVA"):
            st.session_state.history_end_time = time.time()  # Record when history phase ended
            st.session_state.station1_phase = 'viva'
            st.rerun()
    
    # VIVA phase
    elif st.session_state.station1_phase == 'viva':
        scenario = st.session_state.selected_scenario
        
        # If history_end_time is not set, set it now
        if 'history_end_time' not in st.session_state:
            st.session_state.history_end_time = time.time()
        
        # Calculate elapsed time for history phase
        history_elapsed = int(st.session_state.history_end_time - st.session_state.start_time)
        
        # Calculate elapsed time for VIVA phase
        viva_elapsed = int(time.time() - st.session_state.history_end_time)
        
        # Display stopwatch
        time_text = format_time(viva_elapsed)
        st.markdown(f"<h2 style='text-align: center;'>VIVA Session: {time_text}</h2>", unsafe_allow_html=True)
        
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
        
        # Manual finish button
        if st.button("Finish Station"):
            st.session_state.viva_end_time = time.time()  # Record when VIVA phase ended
            st.session_state.station1_phase = 'summary'
            st.rerun()
    
    # Summary phase
    elif st.session_state.station1_phase == 'summary':
        st.markdown("## Station 1 Complete")
        st.markdown("### Summary")
        
        scenario = st.session_state.selected_scenario
        
        # Calculate times
        history_time = "N/A"
        viva_time = "N/A"
        
        if hasattr(st.session_state, 'history_end_time') and hasattr(st.session_state, 'start_time'):
            history_seconds = int(st.session_state.history_end_time - st.session_state.start_time)
            history_time = format_time(history_seconds)
            
        if hasattr(st.session_state, 'viva_end_time') and hasattr(st.session_state, 'history_end_time'):
            viva_seconds = int(st.session_state.viva_end_time - st.session_state.history_end_time)
            viva_time = format_time(viva_seconds)
        
        # Display time metrics
        st.markdown(f"**History Taking Time:** {history_time}")
        st.markdown(f"**VIVA Session Time:** {viva_time}")
        
        # Calculate performance metrics
        checked_points = len(st.session_state.checked_items)
        total_points = len(scenario["key_history_points"])
        history_percentage = (checked_points / total_points) * 100 if total_points > 0 else 0
        
        # Display coverage metrics
        st.markdown(f"**History Taking Coverage:** {history_percentage:.1f}%")
        st.markdown(f"**Points Covered:** {checked_points}/{total_points}")
        
        # Display subjective data
        st.markdown("### Subjective Assessment")
        subjective_data_markdown = ""
        for key, value in st.session_state.subjective_data.items():
            # Convert key from subj_name to Name
            display_key = key.replace('subj_', '').replace('_', ' ').title()
            subjective_data_markdown += f"**{display_key}:** {value}\n\n"
        
        st.markdown(subjective_data_markdown)
        
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
                "history_time": history_time,
                "viva_time": viva_time,
                "history_coverage": history_percentage,
                "points_covered": checked_points,
                "total_points": total_points,
                "subjective_data": st.session_state.subjective_data,
                "history_notes": st.session_state.history_notes,
                "viva_answers": st.session_state.viva_answers
            }
            save_session_data(username, session_data)
            st.success("Session results saved successfully!")
        
        # Return to dashboard
        if st.button("Return to Dashboard"):
            # Reset all session state variables
            st.session_state.station1_phase = 'intro'
            st.session_state.history_notes = ""
            st.session_state.checked_items = []
            st.session_state.viva_answers = {}
            st.session_state.subjective_data = {}
            st.session_state.start_time = None
            if 'history_end_time' in st.session_state:
                del st.session_state.history_end_time
            if 'viva_end_time' in st.session_state:
                del st.session_state.viva_end_time
            # Navigate back to dashboard
            st.switch_page("pages/1_Dashboard.py")
