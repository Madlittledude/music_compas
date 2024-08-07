import streamlit as st
import math


### CIRCLE OF FIFTHS imports
from circle_of_fifths import draw_circle_of_fifths

### For our mode notes and degrees 
from note_sets import get_scale_notes_and_degrees, mode_descriptions

### CHORD imports
from chords import   degree_names, mode_intervals, parallel_modes, get_borrowed_chords, earth_note_colors, _light_note_colors, chord_intervals, calculate_chord_notes, circle_of_fifths_notes, format_chord_name,progression_to_root_notes, chord_symbols, get_chord_type_from_part

### FRETBOARD imports
from fretboard_visual import guitar_fretboard_visualization


# # Check if navigation query param is set and redirect
# query_params = st.experimental_get_query_params()
# if 'nav' in query_params and query_params['nav'][0] == 'fretboard_select_FREQ':
#     # Redirect to fretboard_select_FREQ.py
#     st.experimental_set_query_params(app='fretboard_select_FREQ')  # This is a placeholder. Adjust according to your actual redirection method.
#     st.stop()

# # Navigation sidebar
# with st.sidebar:
#     if st.button('Go to Fretboard Select FREQ'):
#         # Set query param to navigate
#         st.experimental_set_query_params(nav='fretboard_select_FREQ')


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

def calculate_color(degree_index, total_degrees):
    """Generates a cyclical color moving through RGB back to Red."""
    # Convert degree index to an angle in radians
    angle = (degree_index / total_degrees) * 2 * math.pi
    
    # Calculate RGB using sine functions for smooth cycling through red, green, and blue
    red = math.sin(angle) ** 2 * 255
    green = math.sin(angle + 2 * math.pi / 3) ** 2 * 255  # Offset by 120 degrees
    blue = math.sin(angle + 4 * math.pi / 3) ** 2 * 255  # Offset by 240 degrees

    return f'#{int(red):02x}{int(green):02x}{int(blue):02x}'


# Generate colors for each degree based on their index
degree_list = list(degree_names.values())
degree_colors = {degree: calculate_color(index, len(degree_list)) for index, degree in enumerate(degree_list)}

def get_absolute_and_relative_degrees(notes, scale_notes):
    """Calculates the absolute degrees of the root note and the relative degrees of all notes in a chord."""
    absolute_degrees = [degree_names.get(scale_notes.index(note) % len(scale_notes), '?') if note in scale_notes else '?' for note in notes]
    return absolute_degrees

def get_note_degree(root_note, scale_notes):
    """Gets the degree of a note within a given scale."""
    if root_note in scale_notes:
        index = scale_notes.index(root_note)
        return degree_names.get(index, '?')
    return '?'

def display_borrowed_chords(chords, scale_notes):
    """Displays borrowed chords with detailed degree information in a visually appealing card format, structured in a centered grid inside the card."""
    for root, chord_type, notes, degrees in chords:
        root_degree_index = scale_notes.index(root) if root in scale_notes else None
        root_degree = degree_names.get(root_degree_index, '?')
        root_color = degree_colors.get(root_degree, '#FFFFFF')  # Get color based on the root degree
        absolute_degrees = get_absolute_and_relative_degrees(notes, scale_notes)

        st.markdown(f"""
        <div style='border-radius: 8px; background-color: {root_color}; padding: 20px; margin-bottom: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
            <h3 style='color: black; text-align: center;'>{root} {format_chord_name(chord_type)} - Degree: {root_degree}</h3>
            <div style='display: grid; grid-template-columns: repeat({len(notes)}, 1fr); align-items: center; justify-items: center; font-size: 16px;'>""", unsafe_allow_html=True)
        for note, relative_degree, absolute_degree in zip(notes, degrees, absolute_degrees):
            note_color = degree_colors.get(relative_degree, '#FFFFFF')  # Use relative degree to color-code individual notes
            st.markdown(f"""
            <div style='margin: 5px;'>
                <div style='color: black; font-weight: bold;'>{note}</div>
                <div style='color: {note_color};'>Rel: {relative_degree}</div>
                <div style='color: {note_color};'>Abs: {absolute_degree}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)






# def display_borrowed_chords(chords):
#     """Displays borrowed chords in a visually appealing format, each note with its degree directly underneath."""
#     for root, chord_type, notes, degrees in chords:
#         # Create a card for each chord
#         st.markdown(f"<div style='background-color: #f8f9fa; border-radius: 10px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
#         st.markdown(f"<h3 style='color: #333;'>{root} {format_chord_name(chord_type)}</h3>", unsafe_allow_html=True)
#         num_notes = len(notes)
#         cols = st.columns(num_notes)  # Create a column for each note in the chord
        
#         # Display each note with its corresponding degree directly below it, with color coding
#         for col, note, degree in zip(cols, notes, degrees):
#             col.markdown(f"""
#             <div style='text-align: center; margin-top: 10px;'>
#                 <p style='font-size: 18px; font-weight: bold; color: #4A90E2;'>{note}</p>
#                 <p style='color: #6C757D;'><sup>{degree}</sup></p>
#             </div>
#             """, unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)  # Close the card div

def format_chord_name(chord_type):
    """Formats the chord type to use abbreviations like 'M' for Maj7, 'm' for minor, etc."""
    abbreviations = {
        'major': '',
        'minor': 'm',
        'major_seventh': 'M',
        'minor_seventh': 'm7',
        'diminished': '*',
        'augmented': '+',
        'dominant_seventh': '7'
    }
    return abbreviations.get(chord_type, chord_type)  # Default to raw chord type if no abbreviation is found




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
        mode_choice = st.selectbox('Select the mode to borrow from:', list(parallel_modes.keys()), key='mode_selectt_borrowed_chords')
        borrowed_chords = get_borrowed_chords(mode_choice,root_note)
        scale_notes, _ = get_scale_notes_and_degrees(mode_choice, root_note)  # Get scale notes for color mapping

        if borrowed_chords:
            st.write(f"Borrowed chords from {mode_choice}:")
            for (b_root, b_type, b_notes, b_degrees) in borrowed_chords:
                st.write(f"{b_root} {format_chord_name(b_type)}: {b_notes} = {b_degrees}")
                if st.checkbox(f"Show fretboard for {b_root} {format_chord_name(b_type)}", key=f'fretboard_borrowed_{b_root}'):
                    guitar_fretboard_visualization(note_colors, b_notes, b_degrees, show_degrees=True)
                    
        display_borrowed_chords(borrowed_chords,scale_notes)

    if st.checkbox('Show Mode Details', key='show_mode_details'):
        mode_choice = st.selectbox('Select a mode to explore:', list(mode_intervals.keys()), key='mode_select_details')
        mode_info = mode_descriptions.get(mode_choice, {'simple': 'No description available.', 'deep': ''})
        if st.checkbox(f"Show simple description of {mode_choice} mode", key='simple_desc'):
            st.write(f"**Simple Description:** {mode_info['simple']}")
        if st.checkbox(f"Show detailed description of {mode_choice} mode", key='detailed_desc'):
            st.write(f"**Detailed Description:** {mode_info['deep']}")

        scale_notes, scale_degrees = get_scale_notes_and_degrees(mode_choice, root_note)
        st.write("### Scale Notes and Degrees")
        num_notes = len(scale_notes)
        cols_notes = st.columns(num_notes)
        cols_degrees = st.columns(num_notes)
        for col_note, note in zip(cols_notes, scale_notes):
            col_note.markdown(f"<div style='text-align: center; border: 2px solid gray; padding: 8px; font-weight: bold; font-size: 16px;'>{note}</div>", unsafe_allow_html=True)
        for col_degree, degree in zip(cols_degrees, scale_degrees):
            col_degree.markdown(f"<div style='text-align: center; border: 2px solid gray; padding: 8px; font-size: 14px;'>{degree}</div>", unsafe_allow_html=True)
            

    


main_streamlit_layout()



#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
    # Checkbox to show related chords
    # if st.checkbox('Show related chords', key='related_chords_checkbox'):
    #     show_related_chords_section(root_note, chord_type)


#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
