import streamlit as st



### CIRCLE OF FIFTHS imports
from circle_of_fifths import draw_circle_of_fifths


### CHORD imports
from chords import get_borrowed_chords, earth_note_colors, _light_note_colors, chord_intervals, calculate_chord_notes, circle_of_fifths_notes, format_chord_name,progression_to_root_notes, chord_symbols, get_chord_type_from_part

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
        progression_choices_with_custom = {
            **progression_choices,
            'Custom -----------------------(Enter Your Own)': 'Custom'
        }
        selected_description = st.selectbox(
            'Select the chord progression:',
            list(progression_choices_with_custom.keys()),  # Display descriptions including Custom option
            key='progression_select'
        )

        if selected_description == 'Custom -----------------------(Enter Your Own)':
            allowable_symbols = ', '.join([symbol for symbol in chord_symbols.values() if symbol])
            symbol_instructions = f"Allowed symbols: {allowable_symbols}. Use uppercase for major chords and lowercase for minor chords."
            st.text("Enter your custom chord progression using the format 'I-IV-V'. Include any of the following symbols after the Roman numeral as needed:")
            st.text(symbol_instructions)
            custom_progression = st.text_input("Custom Chord Progression", "")
            if custom_progression:
                selected_progression = custom_progression
            else:
                selected_progression = ""
        else:
            selected_progression = progression_choices[selected_description]

        if selected_progression:
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
    
    st.write("\nChecking parallel modes:", parallel_modes)

        # Checkbox to show borrowed chords
    if st.checkbox('Show Borrowed Chords', key='show_borrowed_chords'):
        mode_choice = st.selectbox('Select the mode to borrow from:', list(parallel_modes.keys()), key='mode_select')
        borrowed_chords = get_borrowed_chords(mode_choice, root_note)
        
        if borrowed_chords:
            st.write(f"Borrowed chords from {mode_choice}:")
            for (b_root, b_type, b_notes, b_degrees) in borrowed_chords:
                st.write(f"{b_root} {format_chord_name(b_type)}: {b_notes} = {b_degrees}")
                if st.checkbox(f"Show fretboard for {b_root} {format_chord_name(b_type)}", key=f'fretboard_borrowed_{b_root}'):
                    guitar_fretboard_visualization(note_colors, b_notes, b_degrees, show_degrees=True)
    

main_streamlit_layout()


#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
    # Checkbox to show related chords
    # if st.checkbox('Show related chords', key='related_chords_checkbox'):
    #     show_related_chords_section(root_note, chord_type)


#     circle_of_fifths_notes = ['C', 'G', 'D', 'A', 'E', 'B', 'F♯/Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F']
