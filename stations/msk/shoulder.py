import streamlit as st
from datetime import datetime
import time

def display_station():
    # Check if we're in analysis mode
    if st.session_state.get("analysis_mode", False):
        display_scenario_analysis()
        return
    # Check if we're in OSCE practice mode
    elif st.session_state.get("osce_practice_mode", False):
        display_osce_practice()
        return
    
    st.title("Musculoskeletal Station: Post-Op Total Hip Replacement")
    
    # Station information
    st.markdown("""
    ## Scenario
    
    Mr. Specter is a 72-year-old retired food vendor, with a history of Diabetes Mellitus, Postural 
    Hypotension and Hyperlipidemia. He visited physio rehab after his total hip replacement. 
    Currently he is post-op 2 weeks. Dr allowed Partial weight bearing. Please teach him 2 appropriate exercises.
    
    **Time allowed:** 8 minutes
    
    **Tasks:**
    1. Introduce yourself
    2. Obtain consent for the intervention
    3. Select and teach 2 appropriate exercises
    4. Explain the benefits and precautions of these exercises
    """)
    
    # Display Start Analysis button in the bottom right
    st.markdown("""
    <style>
    .stButton button {
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container for button to place it at the bottom
    with st.container():
        st.write("")
        st.write("")
        if st.button("Start Analysis"):
            st.session_state.analysis_mode = True
            st.rerun()

def display_scenario_analysis():
    st.title("Scenario Analysis: Post-Op Total Hip Replacement")
    
    st.markdown("""
    ## Understanding the Scenario
    
    Let's break down the key elements of this case to identify important considerations for treatment:
    """)
    
    # Create tabs for different analysis sections
    tabs = st.tabs(["Patient Profile", "Medical History", "Current Status", "Exercise Selection"])
    
    with tabs[0]:
        st.markdown("""
        ### Patient Profile
        
        <div style="background-color: #e6f7ff; padding: 20px; border: 2px solid #91d5ff; border-radius: 10px; margin-bottom: 15px;">
        <span style="background-color: #ffff00; padding: 2px 5px; font-weight: bold;">Mr. Specter is a 72-year-old retired food vendor</span>
        </div>
        
        **Analysis:**
        
        ✅ **Age:** Advanced age (72) is significant as it:
        - Affects recovery timeframes
        - May indicate reduced physiological reserve
        - Influences exercise prescription intensity
        
        ✅ **Occupation (retired food vendor):**
        - May suggest previous prolonged standing postures
        - May have contributed to hip degeneration
        - Important to consider potential return to activities
        """, unsafe_allow_html=True)
        
    with tabs[1]:
        st.markdown("""
        ### Medical History
        
        <div style="background-color: #e6f7ff; padding: 20px; border: 2px solid #91d5ff; border-radius: 10px; margin-bottom: 15px;">
        <span style="background-color: #ffff00; padding: 2px 5px; font-weight: bold;">with a history of Diabetes Mellitus, Postural Hypotension and Hyperlipidemia</span>
        </div>
        
        **Analysis:**
        
        ✅ **Diabetes Mellitus:**
        - May impact wound healing
        - Associated with peripheral neuropathy (reduced sensation in extremities)
        - Affects exercise tolerance and recovery
        - May need to consider timing around medications and meals
        
        ✅ **Postural Hypotension:**
        - Risk of dizziness and falls with position changes
        - Exercises need gradual position transitions
        - Monitor for symptoms during and after exercises
        - Important to teach proper hand support during transitions
        
        ✅ **Hyperlipidemia:**
        - Associated with cardiovascular risk
        - Consider impact on overall endurance
        - Long-term goal should include appropriate cardiovascular exercise
        """, unsafe_allow_html=True)
        
    with tabs[2]:
        st.markdown("""
        ### Current Status
        
        <div style="background-color: #e6f7ff; padding: 20px; border: 2px solid #91d5ff; border-radius: 10px; margin-bottom: 15px;">
        <span style="background-color: #ffff00; padding: 2px 5px; font-weight: bold;">He visited physio rehab after his total hip replacement. Currently he is post-op 2 weeks. Dr allowed Partial weight bearing.</span>
        </div>
        
        **Analysis:**
        
        ✅ **Post-op 2 weeks:**
        - Early rehabilitation phase
        - Primary concerns: protect surgical site and prevent dislocation
        - Focus on range of motion within hip precautions
        - Pain management still important
        
        ✅ **Partial weight bearing:**
        - Need to teach correct use of walking aids
        - Monitor weight-bearing status during exercises
        - Focus on exercises that respect weight-bearing restrictions
        - Static and non-weight bearing exercises are appropriate
        
        ✅ **Total hip replacement:**
        - Must follow hip precautions (typically no hip flexion >90°, no adduction past midline, no internal rotation beyond neutral)
        - Consideration of surgical approach (anterior vs posterior)
        - Focus on glute strengthening and hip stability
        """, unsafe_allow_html=True)
        
    with tabs[3]:
        st.markdown("""
        ### Exercise Selection Considerations
        
        Based on our analysis, appropriate exercises should:
        
        1. **Respect hip precautions** to prevent dislocation
        2. **Adhere to partial weight bearing** restrictions
        3. **Consider postural hypotension** - avoid rapid position changes
        4. **Be appropriate for patient age** and early post-op phase
        5. **Include proper support** to prevent falls
        6. **Involve gradual progression** considering diabetes and age
        
        **Potential Appropriate Exercises:**
        
        1. **Ankle pumps and ankle circles** - improve circulation, prevent DVT
        2. **Isometric gluteal contractions** - engage key muscles without movement
        3. **Assisted heel slides** within precaution limits
        4. **Abdominal bracing** - core stability without hip strain
        5. **Supine hip abduction** - strengthens abductors while protecting joint
        
        **Teaching Approach:**
        
        1. Clear, simple instructions appropriate for age
        2. Demonstrate exercises first
        3. Have patient perform with feedback
        4. Provide written instructions with pictures
        5. Explain benefits and precautions
        6. Check understanding
        """)
    
    # Button to return to the scenario
    if st.button("Return to Scenario"):
        st.session_state.analysis_mode = False
        st.rerun()
    
    # Button to start the OSCE practice station
    if st.button("Start OSCE Practice"):
        st.session_state.analysis_mode = False
        st.session_state.osce_practice_mode = True
        st.rerun()

def display_osce_practice():
    st.title("OSCE Practice: Post-Op Total Hip Replacement")
    
    # Start station button
    if 'station_started' not in st.session_state:
        st.session_state.station_started = False
        st.session_state.start_time = None
        st.session_state.current_step = 0
        st.session_state.completed_steps = []
        st.session_state.notes = ""
    
    # Station information
    st.markdown("""
    ## Scenario Reminder
    
    Mr. Specter is a 72-year-old retired food vendor, with a history of Diabetes Mellitus, Postural 
    Hypotension and Hyperlipidemia. He visited physio rehab after his total hip replacement. 
    Currently he is post-op 2 weeks. Dr allowed Partial weight bearing. Please teach him 2 appropriate exercises.
    
    **Target time:** 8 minutes
    """)
    
    # Stopwatch display
    if st.session_state.station_started:
        elapsed = time.time() - st.session_state.start_time
        mins, secs = divmod(int(elapsed), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        # Display stopwatch prominently
        st.markdown(f"""
        <div style="background-color:#f5f5f5; padding:10px; border-radius:5px; border:2px solid #4CAF50; text-align:center;">
            <h2>Time Elapsed: {time_str}</h2>
            <p>Target: 8 minutes</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Warning if over time
        if elapsed > 8*60:
            st.warning("You've exceeded the 8-minute target time. In a real OSCE, you would need to conclude now.")
    
    # Station content
    if not st.session_state.station_started:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.info("""
            ### Instructions
            
            In this station, you will demonstrate how you would teach appropriate exercises to a post-op total hip replacement patient.
            
            You can:
            - Talk to your device as if it were the patient
            - Demonstrate exercises (imagining that you are showing them to the patient)
            - Explain precautions and benefits
            
            Check off items in the right column as you complete them.
            """)
            
        with col2:
            if st.button("Start Station"):
                st.session_state.station_started = True
                st.session_state.start_time = time.time()
                st.rerun()
    else:
        # Define practice steps
        steps = [
            {
                "name": "Introduction & Consent",
                "content": """
                ### Introduction & Consent
                
                **Expected actions:**
                - Introduce yourself (name and role)
                - Explain what you will be doing
                - Obtain consent for the intervention
                - Check if the patient has any questions
                
                **Considerations:**
                Remember that Mr. Specter is 72 years old and may need clear, simple explanations. Consider his history of postural hypotension which may affect position changes during exercises.
                """,
                "checklist": [
                    "Introduced self with name and role",
                    "Explained purpose of session",
                    "Obtained consent",
                    "Used appropriate language for age"
                ]
            },
            {
                "name": "Exercise 1 Selection & Teaching",
                "content": """
                ### Exercise 1 Selection & Teaching
                
                **Expected actions:**
                - Select an appropriate exercise considering patient's condition
                - Demonstrate the exercise clearly
                - Explain starting position and movement
                - Provide appropriate dosage (sets/reps)
                - Observe patient attempting the exercise
                - Provide feedback and correction
                
                **Potential appropriate exercises:**
                - Supine isometric gluteal contractions
                - Supine hip abduction (within precautions)
                - Ankle pumps and circles
                - Seated knee extension (if appropriate for weight bearing status)
                
                **Considerations:**
                Remember hip precautions following THR, partial weight-bearing status, and need for stability due to postural hypotension.
                """,
                "checklist": [
                    "Selected appropriate exercise",
                    "Demonstrated clearly",
                    "Provided correct starting position",
                    "Specified appropriate dosage",
                    "Observed and corrected performance",
                    "Adhered to hip precautions",
                    "Maintained partial weight-bearing"
                ]
            },
            {
                "name": "Exercise 2 Selection & Teaching",
                "content": """
                ### Exercise 2 Selection & Teaching
                
                **Expected actions:**
                - Select a second appropriate exercise
                - Demonstrate the exercise clearly
                - Explain starting position and movement
                - Provide appropriate dosage (sets/reps)
                - Observe patient attempting the exercise
                - Provide feedback and correction
                
                **Considerations:**
                Choose a complementary exercise that addresses a different aspect of rehabilitation while still respecting precautions and partial weight-bearing status.
                """,
                "checklist": [
                    "Selected appropriate exercise",
                    "Demonstrated clearly",
                    "Provided correct starting position",
                    "Specified appropriate dosage",
                    "Observed and corrected performance",
                    "Adhered to hip precautions",
                    "Maintained partial weight-bearing"
                ]
            },
            {
                "name": "Benefits & Precautions",
                "content": """
                ### Benefits & Precautions
                
                **Expected actions:**
                - Explain the benefits of each exercise
                - Discuss specific precautions for THR
                - Address safety concerns related to medical history
                - Provide progressions/regressions as appropriate
                
                **Key points to cover:**
                - Hip precautions (no flexion >90°, no adduction past midline, no internal rotation)
                - Signs of excessive exertion to watch for
                - How exercises contribute to recovery
                - When to stop an exercise (pain, dizziness, etc.)
                - Considerations for diabetes and postural hypotension
                """,
                "checklist": [
                    "Explained benefits of exercises",
                    "Covered relevant hip precautions",
                    "Addressed safety with position changes",
                    "Provided progression options",
                    "Discussed when to stop exercises",
                    "Considered medical history in explanations"
                ]
            },
            {
                "name": "Closure",
                "content": """
                ### Closure
                
                **Expected actions:**
                - Check understanding
                - Provide opportunity for questions
                - Give written instructions or reminders
                - Schedule follow-up or next steps
                - Thank the patient
                
                **Considerations:**
                Ensure Mr. Specter fully understands the exercises and precautions before ending the session.
                """,
                "checklist": [
                    "Checked understanding",
                    "Answered questions appropriately",
                    "Provided written/visual instructions",
                    "Discussed follow-up plan",
                    "Thanked patient"
                ]
            }
        ]
        
        # Display current step
        current_step = st.session_state.current_step
        
        if current_step < len(steps):
            step = steps[current_step]
            
            # Create two columns - one for content, one for checklist
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(step["content"])
            
            with col2:
                # Checklist for current step
                st.markdown("""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">
                <h3>Checklist</h3>
                </div>
                """, unsafe_allow_html=True)
                
                checked_items = []
                for i, item in enumerate(step["checklist"]):
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
                        st.rerun()
            
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
                    st.rerun()
        else:
            # Capture final time
            if st.session_state.start_time:
                total_time = time.time() - st.session_state.start_time
                mins, secs = divmod(int(total_time), 60)
                time_taken = f"{mins:02d}:{secs:02d}"
            else:
                time_taken = "Not recorded"
            
            # Station completed
            st.success("You have completed all steps of the exercise teaching demonstration!")
            
            # Calculate score
            total_checklist_items = sum(len(s["checklist"]) for s in steps)
            completed_items = sum(len(s["completed_items"]) for s in st.session_state.completed_steps)
            score_percentage = (completed_items / total_checklist_items) * 100
            
            # Display score with time taken
            st.markdown(f"""
            <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border: 2px solid #4285f4; margin-bottom: 20px;">
                <h2>Station Summary</h2>
                <p><strong>Time taken:</strong> {time_taken} (Target: 8 minutes)</p>
                <p><strong>Score:</strong> {completed_items}/{total_checklist_items} ({score_percentage:.1f}%)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Performance by section:")
            
            # Display performance by section
            for i, step_result in enumerate(st.session_state.completed_steps):
                step_score = (len(step_result["completed_items"]) / step_result["total_items"]) * 100
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #4CAF50;">
                <strong>{step_result["step_name"]}:</strong> {len(step_result["completed_items"])}/{step_result["total_items"]} ({step_score:.1f}%)
                </div>
                """, unsafe_allow_html=True)
                
                if step_result["notes"]:
                    st.markdown(f"**Your notes:** {step_result['notes']}")
            
            # Example feedback
            st.markdown("""
            ## Sample Model Answer
            
            ### Appropriate Exercises
            
            **Exercise 1: Supine Isometric Gluteal Contractions**
            - Starting position: Lying on back with legs straight
            - Action: Squeeze buttocks together, hold for 5 seconds, then relax
            - Dosage: 10 repetitions, 3 sets per day
            - Benefits: Strengthens gluteal muscles without hip movement, supports hip stability
            - Precautions: Ensure no hip rotation during the exercise
            
            **Exercise 2: Ankle Pumps and Circles**
            - Starting position: Lying on back or sitting with legs extended
            - Action: Point toes up and down, then rotate ankles in circles
            - Dosage: 10 repetitions each direction, every hour while awake
            - Benefits: Improves circulation, prevents blood clots, maintains ankle mobility
            - Precautions: Ensure no hip movement during the exercise
            
            ### Key Points in Teaching
            
            1. **Clear Instructions**: Use simple language appropriate for a 72-year-old
            2. **Demonstration**: Show the exercise before asking patient to perform it
            3. **Observation**: Watch patient perform and provide corrections
            4. **Precautions**: Emphasize THR precautions (no flexion >90°, no adduction past midline, no internal rotation)
            5. **Adaptation**: Consider postural hypotension with position changes
            6. **Documentation**: Provide written instructions with pictures
            
            ### Other Appropriate Exercises
            
            - Supine hip abduction within safe range
            - Seated knee extension (if appropriate for weight bearing status)
            - Abdominal bracing for core stability
            """)
            
            # Save results button
            if st.button("Save Results"):
                # Here you would implement saving to database
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to session state for now
                if "practice_history" not in st.session_state:
                    st.session_state.practice_history = []
                
                st.session_state.practice_history.append({
                    "station": "Post-Op THR Exercise Teaching",
                    "timestamp": timestamp,
                    "time_taken": time_taken,
                    "score": f"{score_percentage:.1f}%",
                    "details": st.session_state.completed_steps
                })
                
                st.success("Results saved successfully!")
            
            # Return buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Return to Scenario Analysis"):
                    # Reset the OSCE practice state
                    for key in ['station_started', 'start_time', 'current_step', 'completed_steps', 'notes']:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    # Go back to analysis mode
                    st.session_state.osce_practice_mode = False
                    st.session_state.analysis_mode = True
                    st.rerun()
                    
            with col2:
                if st.button("Return to Station Selection"):
                    # Reset all station-specific state
                    for key in list(st.session_state.keys()):
                        if key not in ['logged_in', 'username', 'practice_history']:
                            del st.session_state[key]
                            
                    # Clear selected station
                    if "selected_station" in st.session_state:
                        del st.session_state.selected_station
                        
                    st.rerun()
            {
                "name": "Benefits & Precautions",
                "content": """
                ### Benefits & Precautions
                
                **Expected actions:**
                - Explain the benefits of each exercise
                - Discuss specific precautions for THR
                - Address safety concerns related to medical history
                - Provide progressions/regressions as appropriate
                
                **Key points to cover:**
                - Hip precautions (no flexion >90°, no adduction past midline, no internal rotation)
                - Signs of excessive exertion to watch for
                - How exercises contribute to recovery
                - When to stop an exercise (pain, dizziness, etc.)
                - Considerations for diabetes and postural hypotension
                """,
                "checklist": [
                    "Explained benefits of exercises",
                    "Covered relevant hip precautions",
                    "Addressed safety with position changes",
                    "Provided progression options",
                    "Discussed when to stop exercises",
                    "Considered medical history in explanations"
                ]
            },
            {
                "name": "Closure",
                "content": """
                ### Closure
                
                **Expected actions:**
                - Check understanding
                - Provide opportunity for questions
                - Give written instructions or reminders
                - Schedule follow-up or next steps
                - Thank the patient
                
                **Considerations:**
                Ensure Mr. Specter fully understands the exercises and precautions before ending the session.
                """,
                "checklist": [
                    "Checked understanding",
                    "Answered questions appropriately",
                    "Provided written/visual instructions",
                    "Discussed follow-up plan",
                    "Thanked patient"
                ]
            }
        
        # Display current step
        current_step = st.session_state.current_step
        
        if current_step < len(steps):
            step = steps[current_step]
            
            # Create two columns - one for content, one for checklist
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(step["content"])
            
            with col2:
                # Checklist for current step
                st.markdown("""
                <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">
                <h3>Checklist</h3>
                </div>
                """, unsafe_allow_html=True)
                
                checked_items = []
                for i, item in enumerate(step["checklist"]):
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
                        st.rerun()
            
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
                    st.rerun()
        else:
            # Capture final time
            if st.session_state.start_time:
                total_time = time.time() - st.session_state.start_time
                mins, secs = divmod(int(total_time), 60)
                time_taken = f"{mins:02d}:{secs:02d}"
            else:
                time_taken = "Not recorded"
            
            # Station completed
            st.success("You have completed all steps of the exercise teaching demonstration!")
            
            # Calculate score
            total_checklist_items = sum(len(s["checklist"]) for s in steps)
            completed_items = sum(len(s["completed_items"]) for s in st.session_state.completed_steps)
            score_percentage = (completed_items / total_checklist_items) * 100
            
            # Display score with time taken
            st.markdown(f"""
            <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; border: 2px solid #4285f4; margin-bottom: 20px;">
                <h2>Station Summary</h2>
                <p><strong>Time taken:</strong> {time_taken} (Target: 8 minutes)</p>
                <p><strong>Score:</strong> {completed_items}/{total_checklist_items} ({score_percentage:.1f}%)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Performance by section:")
            
            # Display performance by section
            for i, step_result in enumerate(st.session_state.completed_steps):
                step_score = (len(step_result["completed_items"]) / step_result["total_items"]) * 100
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #4CAF50;">
                <strong>{step_result["step_name"]}:</strong> {len(step_result["completed_items"])}/{step_result["total_items"]} ({step_score:.1f}%)
                </div>
                """, unsafe_allow_html=True)
                
                if step_result["notes"]:
                    st.markdown(f"**Your notes:** {step_result['notes']}")
            
            # Example feedback
            st.markdown("""
            ## Sample Model Answer
            
            ### Appropriate Exercises
            
            **Exercise 1: Supine Isometric Gluteal Contractions**
            - Starting position: Lying on back with legs straight
            - Action: Squeeze buttocks together, hold for 5 seconds, then relax
            - Dosage: 10 repetitions, 3 sets per day
            - Benefits: Strengthens gluteal muscles without hip movement, supports hip stability
            - Precautions: Ensure no hip rotation during the exercise
            
            **Exercise 2: Ankle Pumps and Circles**
            - Starting position: Lying on back or sitting with legs extended
            - Action: Point toes up and down, then rotate ankles in circles
            - Dosage: 10 repetitions each direction, every hour while awake
            - Benefits: Improves circulation, prevents blood clots, maintains ankle mobility
            - Precautions: Ensure no hip movement during the exercise
            
            ### Key Points in Teaching
            
            1. **Clear Instructions**: Use simple language appropriate for a 72-year-old
            2. **Demonstration**: Show the exercise before asking patient to perform it
            3. **Observation**: Watch patient perform and provide corrections
            4. **Precautions**: Emphasize THR precautions (no flexion >90°, no adduction past midline, no internal rotation)
            5. **Adaptation**: Consider postural hypotension with position changes
            6. **Documentation**: Provide written instructions with pictures
            
            ### Other Appropriate Exercises
            
            - Supine hip abduction within safe range
            - Seated knee extension (if appropriate for weight bearing status)
            - Abdominal bracing for core stability
            """)
            
            # Save results button
            if st.button("Save Results"):
                # Here you would implement saving to database
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to session state for now
                if "practice_history" not in st.session_state:
                    st.session_state.practice_history = []
                
                st.session_state.practice_history.append({
                    "station": "Post-Op THR Exercise Teaching",
                    "timestamp": timestamp,
                    "time_taken": time_taken,
                    "score": f"{score_percentage:.1f}%",
                    "details": st.session_state.completed_steps
                })
                
                st.success("Results saved successfully!")
            
            # Return buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Return to Scenario Analysis"):
                    # Reset the OSCE practice state
                    for key in ['station_started', 'start_time', 'current_step', 'completed_steps', 'notes']:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    # Go back to analysis mode
                    st.session_state.osce_practice_mode = False
                    st.session_state.analysis_mode = True
                    st.rerun()
                    
            with col2:
                if st.button("Return to Station Selection"):
                    # Reset all station-specific state
                    for key in list(st.session_state.keys()):
                        if key not in ['logged_in', 'username', 'practice_history']:
                            del st.session_state[key]
                            
                    # Clear selected station
                    if "selected_station" in st.session_state:
                        del st.session_state.selected_station
                        
                    st.rerun()"Benefits & Precautions",
                "content": """
                ### Benefits & Precautions
                
                **Expected actions:**
                - Explain the benefits of each exercise
                - Discuss specific precautions for THR
                - Address safety concerns related to medical history
                - Provide progressions/regressions as appropriate
                
                **Key points to cover:**
                - Hip precautions (no flexion >90°, no adduction past midline, no internal rotation)
                - Signs of excessive exertion to watch for
                - How exercises contribute to recovery
                - When to stop an exercise (pain, dizziness, etc.)
                - Considerations for diabetes and postural hypotension
                """,
                "checklist": [
                    "Explained benefits of exercises",
                    "Covered relevant hip precautions",
                    "Addressed safety with position changes",
                    "Provided progression options",
                    "Discussed when to stop exercises",
                    "Considered medical history in explanations"
                ]
            },
            {
                "name": "Closure",
                "content": """
                ### Closure
                
                **Expected actions:**
                - Check understanding
                - Provide opportunity for questions
                - Give written instructions or reminders
                - Schedule follow-up or next steps
                - Thank the patient
                
                **Considerations:**
                Ensure Mr. Specter fully understands the exercises and precautions before ending the session.
                """,
                "checklist": [
                    "Checked understanding",
                    "Answered questions appropriately",
                    "Provided written/visual instructions",
                    "Discussed follow-up plan",
                    "Thanked patient"
                ]
            }
        ]
        
        # Display current step
        current_step = st.session_state.current_step
        
        if current_step < len(steps):
            step = steps[current_step]
            
            # Create two columns - one for content, one for checklist
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(step["content"])
            
            with col2:
                # Checklist for current step
                st.subheader("Checklist")
                
                checked_items = []
                for i, item in enumerate(step["checklist"]):
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
                        st.rerun()
            
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
                    st.rerun()
        else:
            # Station completed
            st.success("You have completed all steps of the exercise teaching demonstration!")
            
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
            
            # Example feedback
            st.markdown("""
            ## Sample Model Answer
            
            ### Appropriate Exercises
            
            **Exercise 1: Supine Isometric Gluteal Contractions**
            - Starting position: Lying on back with legs straight
            - Action: Squeeze buttocks together, hold for 5 seconds, then relax
            - Dosage: 10 repetitions, 3 sets per day
            - Benefits: Strengthens gluteal muscles without hip movement, supports hip stability
            - Precautions: Ensure no hip rotation during the exercise
            
            **Exercise 2: Ankle Pumps and Circles**
            - Starting position: Lying on back or sitting with legs extended
            - Action: Point toes up and down, then rotate ankles in circles
            - Dosage: 10 repetitions each direction, every hour while awake
            - Benefits: Improves circulation, prevents blood clots, maintains ankle mobility
            - Precautions: Ensure no hip movement during the exercise
            
            ### Key Points in Teaching
            
            1. **Clear Instructions**: Use simple language appropriate for a 72-year-old
            2. **Demonstration**: Show the exercise before asking patient to perform it
            3. **Observation**: Watch patient perform and provide corrections
            4. **Precautions**: Emphasize THR precautions (no flexion >90°, no adduction past midline, no internal rotation)
            5. **Adaptation**: Consider postural hypotension with position changes
            6. **Documentation**: Provide written instructions with pictures
            
            ### Other Appropriate Exercises
            
            - Supine hip abduction within safe range
            - Seated knee extension (if appropriate for weight bearing status)
            - Abdominal bracing for core stability
            """)
            
            # Save results button
            if st.button("Save Results"):
                # Here you would implement saving to database
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Save to session state for now
                if "practice_history" not in st.session_state:
                    st.session_state.practice_history = []
                
                st.session_state.practice_history.append({
                    "station": "Post-Op THR Exercise Teaching",
                    "timestamp": timestamp,
                    "score": f"{score_percentage:.1f}%",
                    "details": st.session_state.completed_steps
                })
                
                st.success("Results saved successfully!")
            
            # Return buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Return to Scenario Analysis"):
                    # Reset the OSCE practice state
                    for key in ['station_started', 'start_time', 'current_step', 'completed_steps', 'notes']:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    # Go back to analysis mode
                    st.session_state.osce_practice_mode = False
                    st.session_state.analysis_mode = True
                    st.rerun()
                    
            with col2:
                if st.button("Return to Station Selection"):
                    # Reset all station-specific state
                    for key in list(st.session_state.keys()):
                        if key not in ['logged_in', 'username', 'practice_history']:
                            del st.session_state[key]
                            
                    # Clear selected station
                    if "selected_station" in st.session_state:
                        del st.session_state.selected_station
                        
                    st.rerun()

# For testing directly
if __name__ == "__main__":
    display_station()
