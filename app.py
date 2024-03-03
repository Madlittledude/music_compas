import streamlit as st



### CIRCLE OF FIFTHS imports
from circle_of_fifths import draw_circle_of_fifths


### CHORD imports
from chords import earth_note_colors, _light_note_colors, chord_intervals, calculate_chord_notes, circle_of_fifths_notes, format_chord_name, show_related_chords_section

### FRETBOARD imports
from fretboard_visual import guitar_fretboard_visualization

# Streamlit app title
st.title('Circle of Fifths - Chord Visualizer')








def main_streamlit_layout():
    # Initial selections for root note and chord type
    root_note = st.selectbox('Select the root note:', circle_of_fifths_notes, key='root_note_select')
    chord_type = st.selectbox('Select the chord type:', list(chord_intervals.keys()), key='chord_type_select')
    
    # Calculate the chord notes based on the selections
    chord_notes,chord_degrees = calculate_chord_notes(root_note, chord_type)
    
    # Display the basic chord information
    st.write(f"{root_note} {format_chord_name(chord_type)}: {chord_notes} = {chord_degrees}")
    
    # Checkbox to show the circle of fifths
    if st.checkbox('Show Circle of Fifths', key='show_circle_of_fifths'):
        
        draw_circle_of_fifths(root_note, chord_notes,chord_degrees)
    
    # Selecting the color palette
    selected_palette = st.selectbox('Select the color palette:', ['Soft', 'Earth'], key='color_palette_select')
    note_colors = earth_note_colors if selected_palette == 'Earth' else _light_note_colors

    # Checkbox to show guitar fretboard visualization
    if st.checkbox('Show guitar fretboard visualization', key='guitar_fretboard_visualization'):
        guitar_fretboard_visualization(note_colors, chord_notes,chord_degrees, show_degrees=True)

    # Checkbox to show related chords
    if st.checkbox('Show related chords', key='related_chords_checkbox'):
        show_related_chords_section(root_note, chord_type)



main_streamlit_layout()


#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
