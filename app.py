import streamlit as st



### CIRCLE OF FIFTHS imports
from circle_of_fifths import draw_circle_of_fifths


### CHORD imports
from chords import earth_note_colors, _light_note_colors, chord_intervals, calculate_chord_notes, circle_of_fifths_notes, format_chord_name,progression_to_root_notes, chord_symbols, get_chord_type_from_part

### FRETBOARD imports
from fretboard_visual import guitar_fretboard_visualization

# Streamlit app title
st.title('Circle of Fifths - Chord Visualizer')



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
    'Minor 6th Progression --------(vi-m6-I-IV)': 'vi-Vm6-I-IV'
}



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

    if st.checkbox('Show Chord Progression', key='chord_progression_GO'):
        selected_description = st.selectbox(
            'Select the chord progression:',
            list(progression_choices.keys()),  # Display descriptions
            key='progression_select'
        )
        selected_progression = progression_choices[selected_description]

        progression_parts = selected_progression.split('-')
        for index, part in enumerate(progression_parts):
            chord_type = get_chord_type_from_part(part)
            progression_root_notes = progression_to_root_notes(root_note, part)
            for prog_root in progression_root_notes:
                chord_notes, chord_degrees = calculate_chord_notes(prog_root, chord_type)
                display_symbol = chord_symbols[chord_type]
                st.write(f"{prog_root} {display_symbol}: {chord_notes} = {chord_degrees}")
                # Checkbox for each chord's guitar fretboard visualization
                if st.checkbox(f"Show fretboard for {prog_root} {display_symbol}", key=f'fretboard_{index}'):
                    guitar_fretboard_visualization(note_colors, chord_notes, chord_degrees, show_degrees=True)


main_streamlit_layout()


#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
    # Checkbox to show related chords
    # if st.checkbox('Show related chords', key='related_chords_checkbox'):
    #     show_related_chords_section(root_note, chord_type)


#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
