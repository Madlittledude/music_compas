import streamlit as st
from chords import calculate_chord_notes

st.set_page_config(layout="wide")

def fretboard_select():
    # Define the chromatic scale and mode intervals
    chromatic_scale = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    mode_intervals = {
        'Ionian': [0, 2, 4, 5, 7, 9, 11],
        'Dorian': [0, 2, 3, 5, 7, 9, 10],
        'Phrygian': [0, 1, 3, 5, 7, 8, 10],
        'Lydian': [0, 2, 4, 6, 7, 9, 11],
        'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
        'Aeolian': [0, 2, 3, 5, 7, 8, 10],
        'Locrian': [0, 1, 3, 5, 6, 8, 10],
        'Harmonic Minor': [0, 2, 3, 5, 7, 8, 11],
        'Phrygian Dominant': [0, 1, 4, 5, 7, 8, 10]
    }

    # Guitar strings dictionary
    guitar_strings_standard = {
        'E_low': ['E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E'],
        'A': ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A'],
        'D': ['D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D'],
        'G': ['G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G'],
        'B': ['B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B'],
        'E_high': ['E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E']
    }

    # Function to generate all modes for every note in the chromatic scale
    def generate_all_modes_scales():
        all_modes_scales = {}
        for note in chromatic_scale:
            all_modes_scales[note] = {}
            for mode_name, intervals in mode_intervals.items():
                scale_notes = [chromatic_scale[(chromatic_scale.index(note) + interval) % 12] for interval in intervals]
                all_modes_scales[note][mode_name] = scale_notes
        return all_modes_scales

    all_modes_scales = generate_all_modes_scales()

    # Function to find scales that contain the selected notes
    def find_scales_for_notes(selected_notes):
        matching_scales = []
        for root_note, modes in all_modes_scales.items():
            for mode_name, scale_notes in modes.items():
                if all(note in scale_notes for note in selected_notes):
                    matching_scales.append(f"{root_note} {mode_name}")
        return matching_scales


    # Function to calculate notes and degrees for a mode
    def calculate_mode_notes(root_note, mode_name, descending=False):
        root_index = chromatic_scale.index(root_note)
        if descending and "Melodic Minor" in mode_name:
            mode_name = "Melodic Minor Descending"
        intervals = mode_intervals[mode_name]
        mode_notes = []
        degrees = []
        for interval in intervals:
            note_index = (root_index + interval) % 12
            note_name = chromatic_scale[note_index]
            mode_notes.append(note_name)
            degrees.append(interval)  # Assuming interval_to_degree function exists
        return mode_notes, degrees


    # Streamlit app layout
    st.title('Guitar Scale Finder')

    # Initialize the selected notes and notes history in the session state if they're not already there
    if 'selected_notes' not in st.session_state:
        st.session_state['selected_notes'] = []

    if 'notes_history' not in st.session_state:
        st.session_state['notes_history'] = []


    # Placeholder for displaying the history of selected notes
    history_placeholder = st.empty()

    # Create a placeholder for the selected notes text
    selected_notes_placeholder = st.empty()

    # Custom CSS to simulate guitar strings behind the buttons
    st.markdown(
        """
        <style>
        .stButton>button {
            width: 100%;
            margin: 0;
        }
        .string-line {
            height: 1px;
            background-color: black;
            position: relative;
            top: -20px;
            z-index: -1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Function to update the selected notes and history displays
    def update_selected_notes_display():
        # Update current selected notes display
        selected_notes_text = ', '.join(st.session_state['selected_notes'])
        selected_notes_placeholder.markdown(f"**Selected notes**: {selected_notes_text}")
        
        # Update history of selected notes display
        if st.session_state['notes_history']:
            history_text = ' | '.join([', '.join(set_notes) for set_notes in st.session_state['notes_history']])
            history_placeholder.markdown(f"**History of selected notes**: {history_text}")
        else:
            history_placeholder.markdown("**History of selected notes**: None")

    # Initially update the selected notes and history displays
    update_selected_notes_display()

    # Display the fretboard with simulated strings
    for string_name, notes in guitar_strings_standard.items():
        st.markdown('<div class="string-line"></div>', unsafe_allow_html=True)
        cols = st.columns(len(notes))
        for idx, note in enumerate(notes):
            button_key = f"button_{string_name}_{idx}"
            if cols[idx].button(note, key=button_key):
                if note in st.session_state['selected_notes']:
                    st.session_state['selected_notes'].remove(note)
                elif len(st.session_state['selected_notes']) < 5:
                    st.session_state['selected_notes'].append(note)
                update_selected_notes_display()


    # Custom CSS to increase font size
    st.markdown(
        """
        <style>
        .scale-card {
            margin: 10px 0;
            padding: 20px; /* Increased padding inside the card for more space */
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            background-color: #f9f9f9;
        }
        .scale-name {
            font-size: 24px; /* Slightly larger for better hierarchy */
            font-weight: bold;
            color: #017BFE;
            margin-bottom: 10px; /* Added space below the scale name */
        }
        .notes {
            font-size: 33px; /* Increased font size */
            color: #333;
            margin: 5px 8px; /* Added more space around each note */
            display: inline-flex; /* Changed to flex to center content */
            align-items: center; /* Center content vertically */
            justify-content: center; /* Center content horizontally */
            padding: 8px 12px; /* Increased padding for more space inside */
            background-color: #e7f5ff;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
        }
        .selected-note {
            background-color: #d63384;
            color: #fff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Define the color palette
    # kinda clowny colors
    # note_colors = ['#FFD700', '#FF8C00', '#1E90FF', '#32CD32', '#DA70D6']
    # Define colors
    non_selected_note_color = '#d3d3d3'  # Light grey for non-selected notes
    selected_note_colors = [
        '#FF6347',  # Tomato
        '#4682B4',  # Steel Blue
        '#FFD700',  # Gold
        '#32CD32',  # Lime Green
        '#DA70D6',  # Orchid
    ]

    # Function to get color for a note based on selection status
    def get_note_color(note, selected_notes):
        if note in selected_notes:
            # If the note is selected, cycle through the selected_note_colors based on the note's index
            return selected_note_colors[selected_notes.index(note) % len(selected_note_colors)]
        else:
            # Use the non_selected_note_color for non-selected notes
            return non_selected_note_color

    if st.button("Find Scales for Selected Notes", key="find_scales_for_selected_notes"):
        matching_scales = find_scales_for_notes(st.session_state['selected_notes'])
        if matching_scales:
            formatted_scales = "<div class='scale-card'><p class='scale-name'>Matching scales:</p>"
            for scale in matching_scales:
                root_note, mode_name = scale.split(' ', 1)
                scale_notes, _ = calculate_mode_notes(root_note, mode_name)
                formatted_notes = ", ".join([
                    f"<span class='notes' style='background-color: {get_note_color(note, st.session_state['selected_notes'])};'>{note}</span>"
                    for note in scale_notes
                ])
                formatted_scales += f"<div class='scale-name'>{scale}:</div><div>{formatted_notes}</div>"
            formatted_scales += "</div>"
            
            st.markdown(formatted_scales, unsafe_allow_html=True)
        else:
            st.markdown("<div class='scale-card'><p class='scale-name'>No scales match the selected notes.</p></div>", unsafe_allow_html=True)

    # Button to find scales for notes in history
    if st.button("Find Scales for History Notes", key="find_scales_for_history_notes"):
        all_notes_history = [note for notes_set in st.session_state['notes_history'] for note in notes_set]
        if all_notes_history:
            matching_scales_history = find_scales_for_notes(all_notes_history)
            if matching_scales_history:
                formatted_scales_history = "<div class='scale-card'><p class='scale-name'>Matching scales for history notes:</p>"
                for scale in matching_scales_history:
                    root_note, mode_name = scale.split(' ', 1)
                    scale_notes, _ = calculate_mode_notes(root_note, mode_name)
                    formatted_notes = ", ".join([
                        f"<span class='notes'>{note}</span>"
                        for note in scale_notes
                    ])
                    formatted_scales_history += f"<div class='scale-name'>{scale}:</div><div>{formatted_notes}</div>"
                formatted_scales_history += "</div>"
                
                st.markdown(formatted_scales_history, unsafe_allow_html=True)
            else:
                st.markdown("<div class='scale-card'><p class='scale-name'>No scales match the notes in history.</p></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='scale-card'><p class='scale-name'>No history notes available.</p></div>", unsafe_allow_html=True)

    # Place Clear and Reset buttons after the fretboard display logic
    if st.button("Clear Selected Notes", key="clear_selected_notes"):
        if st.session_state['selected_notes']:
            st.session_state['notes_history'].append(st.session_state['selected_notes'].copy())
            st.session_state['selected_notes'] = []
        update_selected_notes_display()

    if st.button("Reset All", key="reset_all"):
        st.session_state['selected_notes'] = []
        st.session_state['notes_history'] = []
        update_selected_notes_display()

if __name__ == "__main__":
    fretboard_select()