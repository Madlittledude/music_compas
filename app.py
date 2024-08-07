import streamlit as st



### CIRCLE OF FIFTHS imports
from circle_of_fifths import draw_circle_of_fifths

### For our mode notes and degrees 
from note_sets import get_scale_notes_and_degrees, mode_descriptions

### CHORD imports
from chords import  mode_intervals, parallel_modes, get_borrowed_chords, earth_note_colors, _light_note_colors, chord_intervals, calculate_chord_notes, circle_of_fifths_notes, format_chord_name,progression_to_root_notes, chord_symbols, get_chord_type_from_part

### FRETBOARD imports
from fretboard_visual import guitar_fretboard_visualization


# Check if navigation query param is set and redirect
query_params = st.experimental_get_query_params()
if 'nav' in query_params and query_params['nav'][0] == 'fretboard_select_FREQ':
    # Redirect to fretboard_select_FREQ.py
    st.experimental_set_query_params(app='fretboard_select_FREQ')  # This is a placeholder. Adjust according to your actual redirection method.
    st.stop()

# Navigation sidebar
with st.sidebar:
    if st.button('Go to Fretboard Select FREQ'):
        # Set query param to navigate
        st.experimental_set_query_params(nav='fretboard_select_FREQ')


def display_scale_notes_and_degrees(notes, degrees):
    """Displays scale notes and their corresponding degrees in a visually appealing format."""
    num_notes = len(notes)
    cols_notes = st.columns(num_notes)
    cols_degrees = st.columns(num_notes)
    
    used_notes = set()  # To track already used notes for enharmonic checks

    for col_note, col_degree, note, degree in zip(cols_notes, cols_degrees, notes, degrees):
        # Check if the note is an enharmonic equivalent already present
        if note in used_notes:
            # Optional logic to handle specific enharmonic issues could be added here
            note = note + " (enharmonic check needed)"
        used_notes.add(note)

        col_note.markdown(f"<div style='text-align: center; border: 2px solid gray; padding: 8px;'><b>{note}</b></div>", unsafe_allow_html=True)
        col_degree.markdown(f"<div style='text-align: center; border: 2px solid gray; padding: 8px;'><b>{degree}</b></div>", unsafe_allow_html=True)


# Streamlit app title
st.title('Circle of Fifths - Chord Visualizer')


allowable_symbols = ', '.join([symbol for symbol in chord_symbols.values() if symbol])
symbol_instructions = f"Allowed symbols: {allowable_symbols}. Use uppercase for major chords and lowercase for minor chords."

progression_choices = {
    'Basic Major Progression ----- (I-IV-V)': 'I-IV-V',
    'Jazz Minor Progression -------(ii-V-I)': 'ii-V-I',
    '50s Progression --------------(I-vi-IV-V)': 'I-vi-IV-V',
    'random_test_of_symbols -------(i-V7-Vsus2)': 'i-V7-Vsus2',
    'Blues Progression ------------(I7-IV7-V7)': 'I7-IV7-V7',
    'Pop Progression --------------(I-V-vi-IV)': 'I-V-vi-IV',
    'Rock Progression -------------(I-V-IV-IV)': 'I-V-IV-IV',
    'Jazz Fusion Progression ------(ii7-V7-Imaj7)': 'ii7-V7-Imaj7',
    'Funky Progression ------------(Iadd9-IV7-IV7-Vadd9)': 'Iadd9-IV7-IV7-Vadd9',
    'Ballad Progression -----------(vi-IV-I-V7)': 'vi-IV-I-V7',
    'Minor 6th Progression --------(vi-vm6-I-IV)': 'vi-vm6-I-IV'
}




def main_streamlit_layout():
    root_note = st.selectbox('Select the root note:', circle_of_fifths_notes, key='root_note_select')
    chord_type = st.selectbox('Select the chord type:', list(chord_intervals.keys()), key='chord_type_select')
    chord_notes, chord_degrees = calculate_chord_notes(root_note, chord_type)
    st.write(f"{root_note} {format_chord_name(chord_type)}: {chord_notes} = {chord_degrees}")
    
    if st.checkbox('Show Circle of Fifths', key='show_circle_of_fifths'):
        draw_circle_of_fifths(root_note, chord_notes, chord_degrees)
    
    selected_palette = st.selectbox('Select the color palette:', ['Soft', 'Earth'], key='color_palette_select')
    note_colors = earth_note_colors if selected_palette == 'Earth' else _light_note_colors

    if st.checkbox('Show guitar fretboard visualization', key='guitar_fretboard_visualization'):
        guitar_fretboard_visualization(note_colors, chord_notes, chord_degrees, show_degrees=True)

    if st.checkbox('Show Borrowed Chords', key='show_borrowed_chords'):
        mode_choice = st.selectbox('Select the mode to borrow from:', list(parallel_modes.keys()), key='mode_select')
        borrowed_chords = get_borrowed_chords(mode_choice, root_note)
        if borrowed_chords:
            st.write(f"Borrowed chords from {mode_choice}:")
            for (b_root, b_type, b_notes, b_degrees) in borrowed_chords:
                st.write(f"{b_root} {format_chord_name(b_type)}: {b_notes} = {b_degrees}")
                if st.checkbox(f"Show fretboard for {b_root} {format_chord_name(b_type)}", key=f'fretboard_borrowed_{b_root}'):
                    guitar_fretboard_visualization(note_colors, b_notes, b_degrees, show_degrees=True)
    
    if st.checkbox('Show Mode Details', key='show_mode_details'):
        # Ensure the key for mode selection here is unique by appending an identifier
        mode_choice = st.selectbox('Select a mode to explore:', list(mode_intervals.keys()), key='mode_select_details')
        scale_notes, scale_degrees = get_scale_notes_and_degrees(mode_choice, root_note)
        
        # Creating a better visual presentation for notes and degrees
        st.write("### Scale Notes and Degrees")
        num_notes = len(scale_notes)
        # Use columns to create a grid-like appearance
        cols_notes = st.columns(num_notes)
        cols_degrees = st.columns(num_notes)
        
        # Using markdown with enhanced CSS for better control over typography and layout
        for col_note, note in zip(cols_notes, scale_notes):
            col_note.markdown(f"""
            <div style='text-align: center; 
                        border: 2px solid gray; 
                        padding: 8px;
                        font-weight: bold; 
                        font-size: 16px;'>
                {note}
            </div>""", unsafe_allow_html=True)
        
        for col_degree, degree in zip(cols_degrees, scale_degrees):
            col_degree.markdown(f"""
            <div style='text-align: center; 
                        border: 2px solid gray; 
                        padding: 8px; 
                        font-size: 14px;'>
                {degree}
            </div>""", unsafe_allow_html=True)
    


main_streamlit_layout()



#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
    # Checkbox to show related chords
    # if st.checkbox('Show related chords', key='related_chords_checkbox'):
    #     show_related_chords_section(root_note, chord_type)


#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
