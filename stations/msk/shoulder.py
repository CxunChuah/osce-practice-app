import streamlit as st
from datetime import datetime
import time

def display_station():
    st.title("Shoulder Examination OSCE Station")
    
    # Station information
    st.markdown("""
    ## Instructions
    
    You are asked to perform a focused examination of the shoulder joint on a 45-year-old patient 
    who presents with right shoulder pain for the past 3 weeks. The pain is worse on overhead activities.
    
    **Time allowed:** 8 minutes
    
    **Tasks:**
    1. Take a focused history
    2. Perform a systematic shoulder examination
    3. Explain your findings and differential diagnosis to the examiner
    """)
    
    # Start station button
    if 'station_started' not in st.session_state:
        st.session_state.station_started = False
        st.session_state.start_time = None
        st.session_state.current_step = 0
        st.session_state.completed_steps = []
        st.session_state.notes = ""
    
    # Timer display
    if st.session_state.station_started:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, 8*60 - elapsed)
        
        mins, secs = divmod(int(remaining), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        # Display timer prominently
        st.markdown(f"""
        <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; text-align:center;">
            <h2>Time Remaining: {time_str}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # End station if time runs out
        if remaining <= 0:
            st.session_state.station_started = False
            st.warning("Time's up! Please complete your examination.")
            st.session_state.show_feedback = True
            st.experimental_rerun()
    
    # Station content
    if not st.session_state.station_started:
        if st.button("Start Station"):
            st.session_state.station_started = True
            st.session_state.start_time = time.time()
            st.experimental_rerun()
    else:
        # Define examination steps
        steps = [
            {
                "name": "Introduction & Consent",
                "content": """
                ### Introduction & Consent
                
                **Expected actions:**
                - Introduce yourself to the patient
                - Explain the examination procedure
                - Obtain consent
                - Ensure patient comfort and appropriate exposure
                
                **Sample dialogue:**
                "Hello, my name is [your name]. I'm a physiotherapy student. I'd like to examine your shoulder today. Is that okay with you?"
                """,
                "checklist": [
                    "Introduced self",
                    "Explained procedure",
                    "Obtained consent",
                    "Ensured appropriate exposure"
                ]
            },
            {
                "name": "Inspection",
                "content": """
                ### Inspection
                
                **Expected actions:**
                - Observe both shoulders from front, side and back
                - Look for muscle wasting, deformity, scars, swelling
                - Assess posture
                
                **Findings:**
                On inspection, the patient's right shoulder appears slightly lower than the left. There is mild wasting of the supraspinatus and infraspinatus muscles visible on the right side.
                """,
                "checklist": [
                    "Observed from multiple angles",
                    "Checked for deformity/asymmetry",
                    "Assessed for muscle wasting",
                    "Noted posture"
                ]
            },
            {
                "name": "Palpation",
                "content": """
                ### Palpation
                
                **Expected actions:**
                - Palpate bony landmarks (AC joint, sternoclavicular joint, coracoid process)
                - Palpate rotator cuff insertion
                - Note areas of tenderness
                
                **Findings:**
                There is tenderness on palpation of the greater tuberosity and the supraspinatus insertion. The AC joint is not tender.
                """,
                "checklist": [
                    "Palpated key bony landmarks",
                    "Assessed for tenderness",
                    "Palpated rotator cuff insertions",
                    "Compared both sides"
                ]
            },
            {
                "name": "Movement",
                "content": """
                ### Movement Assessment
                
                **Expected actions:**
                - Assess active and passive range of motion:
                  - Forward flexion (0-180°)
                  - Abduction (0-180°)
                  - External rotation
                  - Internal rotation
                
                **Findings:**
                Active abduction is limited to 100° on the right with pain. Passive abduction allows movement to 120° with pain at the end range. Forward flexion is limited to 120° actively. External rotation is reduced by approximately 15° compared to the left. Internal rotation allows the patient to reach to L3 on the right versus T10 on the left.
                """,
                "checklist": [
                    "Assessed active ROM in all planes",
                    "Assessed passive ROM in all planes",
                    "Noted painful arcs of movement",
                    "Compared both sides"
                ]
            },
            {
                "name": "Special Tests",
                "content": """
                ### Special Tests
                
                **Expected actions:**
                Perform appropriate special tests:
                - Painful arc test
                - Neer's impingement test
                - Hawkins-Kennedy test
                - Empty can test (Jobe's test)
                - Drop arm test
                - Apprehension and relocation tests
                
                **Findings:**
                Positive painful arc between 60-120° of abduction. Neer's and Hawkins-Kennedy tests are positive. Empty can test produces pain and mild weakness. Drop arm and apprehension tests are negative.
                """,
                "checklist": [
                    "Performed impingement tests",
                    "Performed rotator cuff tests",
                    "Performed instability tests",
                    "Interpreted test results correctly"
                ]
            },
            {
                "name": "Functional Assessment",
                "content": """
                ### Functional Assessment
                
                **Expected actions:**
                - Assess patient's ability to perform activities of daily living
                - Ask about impact on work and leisure activities
                
                **Sample questions:**
                "Can you reach behind your back to tuck in your shirt?"
                "Can you reach overhead to a high shelf?"
                "How has this affected your work/hobbies?"
                """,
                "checklist": [
                    "Assessed ADL function",
                    "Inquired about work impact",
                    "Assessed impact on quality of life"
                ]
            },
            {
                "name": "Completion",
                "content": """
                ### Completion & Presentation
                
                **Expected actions:**
                - Thank the patient
                - Cover the patient
                - Summarize findings
                - Present differential diagnosis
                
                **Differential Diagnosis:**
                1. Rotator cuff tendinopathy/impingement syndrome
                2. Supraspinatus tear
                3. Adhesive capsulitis (early)
                4. Referred pain from cervical spine
                
                **Next steps:**
                Recommend appropriate imaging (ultrasound/MRI) and initial management.
                """,
                "checklist": [
                    "Thanked patient",
                    "Ensured patient comfort",
                    "Summarized findings accurately",
                    "Provided reasonable differential",
                    "Suggested appropriate next steps"
                ]
            }
        ]
        
        # Display current step
        current_step = st.session_state.current_step
        
        if current_step < len(steps):
            step = steps[current_step]
            
            st.markdown(step["content"])
            
            # Checklist for current step
            st.subheader("Checklist")
            
            checklist_cols = st.columns(2)
            checked_items = []
            
            for i, item in enumerate(step["checklist"]):
                col_idx = i % 2
                with checklist_cols[col_idx]:
                    if st.checkbox(item, key=f"check_{current_step}_{i}"):
                        checked_items.append(item)
            
            # Notes section
            st.text_area("Your notes for this step:", 
                          key=f"notes_{current_step}", 
                          height=100)
            
            # Navigation buttons
            cols = st.columns(2)
            
            with cols[0]:
                if current_step > 0:
                    if st.button("Previous Step"):
                        st.session_state.current_step -= 1
                        st.experimental_rerun()
            
            with cols[1]:
                if st.button("Next Step"):
                    # Save completed checklist items
                    st.session_state.completed_steps.append({
                        "step_name": step["name"],
                        "completed_items": checked_items,
                        "total_items": len(step["checklist"]),
                        "notes": st.session_state.get(f"notes_{current_step}", "")
                    })
                    
                    st.session_state.current_step += 1
                    st.experimental_rerun()
        else:
            # Station completed
            st.success("You have completed all steps of the examination!")
            
            # Calculate score
            total_checklist_items = sum(len(s["checklist"]) for s in steps)
            completed_items = sum(len(s["completed_items"]) for s in st.session_state.completed_steps)
            score_percentage = (completed_items / total_checklist_items) * 100
            
            # Display score
            st.markdown(f"""
            ## Station Summary
            
            **Score:** {completed_items}/{total_checklist_items} ({score_percentage:.1f}%)
            
            **Performance by section:**
            """)
            
            # Display performance by section
            for i, step_result in enumerate(st.session_state.completed_steps):
                step_score = (len(step_result["completed_items"]) / step_result["total_items"]) * 100
                st.markdown(f"""
                **{step_result["step_name"]}:** {len(step_result["completed_items"])}/{step_result["total_items"]} ({step_score:.1f}%)
                """)
                
                if step_result["notes"]:
                    st.markdown(f"**Your notes:** {step_result['notes']}")
            
            # Save results button
            if st.button("Save Results"):
                # Here you would implement saving to database
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to session state for now - you can modify this to save to a database later
                if "practice_history" not in st.session_state:
                    st.session_state.practice_history = []
                
                st.session_state.practice_history.append({
                    "station": "Shoulder Examination",
                    "timestamp": timestamp,
                    "score": f"{score_percentage:.1f}%",
                    "details": st.session_state.completed_steps
                })
                
                st.success("Results saved successfully!")
            
            # Return to stations button
            if st.button("Return to Stations"):
                # Reset the current station state but keep practice history
                for key in list(st.session_state.keys()):
                    if key not in ['logged_in', 'username', 'practice_history']:
                        del st.session_state[key]
                        
                # Clear selected station
                if "selected_station" in st.session_state:
                    del st.session_state.selected_station
                    
                st.experimental_rerun()

# For testing directly
if __name__ == "__main__":
    display_station()
