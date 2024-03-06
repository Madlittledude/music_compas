import streamlit as st
from note_sets import circle_of_fifths_notes, chromatic_scale
"""
Note on Chord Notation Simplification:
In this implementation, we use a simplified model for chord notation that combines sharp(#) and flat(b) symbols together (e.g., A#/Bb) for enharmonic equivalents. This approach allows for a more straightforward representation and understanding of chords without delving into the complexities of classical music theory which distinguishes between enharmonically equivalent notes based on context (e.g., G# vs. Ab).

Specifically, for the diminished 7th chord, we list the 7th degree as '6' instead of the theoretically correct 'bb7' (double flat 7). This decision is made to keep the model simple and accessible, acknowledging that while it may not align with traditional theory's precise notation, it provides a practical and functional understanding suitable for most contemporary music applications. This simplification enables users to easily identify chord components without the need for advanced theory knowledge regarding enharmonic distinctions and double flattened intervals.
"""


# Define a color gradient from red to violet (using a simple example gradient)
earth_note_colors = {
    'C': '#8B4513',  # Saddle Brown
    'C#/Db': '#2E8B57',  # Sea Green
    'D': '#3CB371',  # Medium Sea Green
    'D#/Eb': '#A0522D',  # Sienna
    'E': '#D2B48C',  # Tan
    'F': '#BC8F8F',  # Rosy Brown
    'F#/Gb': '#CD853F',  # Peru
    'G': '#6B8E23',  # Olive Drab
    'G#/Ab': '#808000',  # Olive
    'A': '#556B2F',  # Dark Olive Green
    'A#/Bb': '#9ACD32',  # Yellow Green
    'B': '#8FBC8F'  # Dark Sea Green
}

light_note_colors = {
    'C': '#FFC0CB',  # Pink
    'C#/Db': '#FFD700',  # Gold
    'D': '#ADFF2F',  # Green Yellow
    'D#/Eb': '#7FFFD4',  # Aquamarine
    'E': '#E0FFFF',  # Light Cyan
    'F': '#DEB887',  # Burlywood
    'F#/Gb': '#DDA0DD',  # Plum
    'G': '#87CEFA',  # Light Sky Blue
    'G#/Ab': '#FFB6C1',  # Light Pink
    'A': '#98FB98',  # Pale Green
    'A#/Bb': '#DB7093',  # Pale Violet Red
    'B': '#FFDEAD'  # Navajo White
}
_light_note_colors = {
    'C': '#FFA07A',  # Light Salmon
    'C#/Db': '#20B2AA',  # Light Sea Green
    'D': '#FFDAB9',  # Peach Puff
    'D#/Eb': '#E6E6FA',  # Lavender
    'E': '#FAFAD2',  # Light Goldenrod Yellow
    'F': '#90EE90',  # Light Green
    'F#/Gb': '#AFEEEE',  # Pale Turquoise
    'G': '#FFC0CB',  # Pink (moved from 'C' to 'G' for variety)
    'G#/Ab': '#FFA07A',  # Light Salmon (alternative option)
    'A': '#B0E0E6',  # Powder Blue
    'A#/Bb': '#F08080',  # Light Coral
    'B': '#D3D3D3'   # Light Grey
}


chord_intervals = {
    'major': [0, 4, 7],
    'minor': [0, 3, 7],
    'power': [0, 7],  # Optionally add 12 for the octave: [0, 7, 12]
    'dominant_7th': [0, 4, 7, 10],
    'major_7th': [0, 4, 7, 11],
    'minor_7th': [0, 3, 7, 10],
    'suspended_4th': [0, 5, 7],
    'suspended_2nd': [0, 2, 7],
    'augmented': [0, 4, 8],
    'diminished': [0, 3, 6],
    'diminished_7th': [0, 3, 6, 9],
    'half_diminished_7th': [0, 3, 6, 10],
    'add9': [0, 4, 7, 14],
    'minor_add9': [0, 3, 7, 14],
    '6th': [0, 4, 7, 9],
    'minor_6th': [0, 3, 7, 9]
}


#### SECTIONS ####
def calculate_chord_notes(root_note, chord_type):
    print('root_note:', root_note)
    root_index = -1
    for i, note in enumerate(chromatic_scale):
        # Direct comparison, looking for an exact match in the chromatic_scale
        if root_note == note:
            root_index = i
            break
    if root_index == -1:
        return [], []

    intervals = chord_intervals[chord_type]
    chord_notes = []
    degrees = []
    for interval in intervals:
        note_index = (root_index + interval) % 12
        note_name = chromatic_scale[note_index]  # Use the note as is from chromatic_scale
        chord_notes.append(note_name)
        degrees.append(interval_to_degree(interval))
    return chord_notes, degrees



def interval_to_degree(interval):
    degree_names = {
        0: 'R',
        1: 'b2',
        2: '2',
        3: 'b3',
        4: '3',
        5: '4',
        6: 'b5',
        7: '5',
        8: '#5',
        9: '6',
        10: 'b7',
        11: '7',
        12: 'R',  # Octave
        13: 'b9',
        14: '9',
        15: '#9',
        17: '11',
        18: '#11',
        20: 'b13',
        21: '13',
        # Add more as necessary
    }
    return degree_names.get(interval, '?')


# Function to format chord names more nicely (removing underscores and capitalizing)
def format_chord_name(chord_name):
    return chord_name.replace('_', ' ').capitalize()

# Updated function to find related chords that also calculates the notes for display
def find_related_chords_and_notes_categorized(selected_chord_type, chord_intervals, root_note):
    related_chords = {
        'Superset': {},
        'Subset': {},
        'Shares common intervals with': {}
    }
    selected_intervals = set(chord_intervals[selected_chord_type])
    
    for chord, intervals in chord_intervals.items():
        if selected_chord_type != chord:
            interval_set = set(intervals)
            relation = None
            if selected_intervals.issubset(interval_set):
                relation = 'Superset'
            elif selected_intervals.issuperset(interval_set):
                relation = 'Subset'
            elif selected_intervals & interval_set:
                relation = 'Shares common intervals with'

            if relation:
                # Calculate the chord notes for display
                chord_notes = calculate_chord_notes(root_note, chord)
                related_chords[relation][chord] = chord_notes
    
    return related_chords

def is_note_in_chord(note, chord_notes):
    return note in chord_notes



def format_chord_notes_for_display(selected_notes, related_notes):
    """
    Format the related chord's notes by adding extra spaces around any note
    that is not part of the selected chord's notes.
    """
    formatted_notes_list = []
    for note in related_notes:
        if note not in selected_notes:
            # Add white spaces around notes not in the selected chord
            formatted_note = f" ..{note}.. "
        else:
            formatted_note = note
        formatted_notes_list.append(formatted_note)
    
    return '  '.join(formatted_notes_list)







def show_related_chords_section(root_note, chord_type):
    selected_chord_notes = calculate_chord_notes(root_note, chord_type)
    related_chords_categorized = find_related_chords_and_notes_categorized(chord_type, chord_intervals, root_note)
    for category, chords in related_chords_categorized.items():
        if chords:
            st.write(f"**{category}:**")
            for chord, notes in chords.items():
                formatted_chord_name = format_chord_name(chord)
                formatted_notes = format_chord_notes_for_display(selected_chord_notes, notes)
                st.markdown(f"    * **{formatted_chord_name}**: {formatted_notes}")





chord_symbols = {
    'major': "",
    'minor': "m",
    'dominant_7th': "7",
    'major_7th': "M7",
    'minor_7th': "m7",
    'diminished': "dim",
    'augmented': "aug",
    'suspended_2nd': "sus2",
    'suspended_4th': "sus4",
    'power': "P",  
    'diminished_7th': "dim7",
    'half_diminished_7th': "m7(b5)", 
    'add9': "add9",
    'minor_add9': "m(add9)",
    '6th': "6",
    'minor_6th': "m6"
}


roman_numeral_intervals = {
    "Tonic": {"numerals": ["I", "i"], "interval": 0},
    "Supertonic": {"numerals": ["II", "ii"], "interval": 2},
    "Mediant": {"numerals": ["III", "iii"], "interval": 4},
    "Subdominant": {"numerals": ["IV", "iv"], "interval": 5},
    "Dominant": {"numerals": ["V", "v"], "interval": 7},
    "Submediant": {"numerals": ["VI", "vi"], "interval": 9},
    "Leading Tone": {"numerals": ["VII", "vii"], "interval": 11}
}

def get_chord_type_from_part(part):
    if 'm6' in part:
        return 'minor_6th'
    if part[0].islower():
        return 'minor'
    # Updated to handle complex chords and return the exact chord type based on the symbols in the part
    if "m7(b5)" in part:
        return 'half_diminished_7th'
    if "add9" in part:
        return 'add9'
    elif "dim7" in part:
        return 'diminished_7th'
    elif "m7" in part:
        return 'minor_7th'
    elif "M7" in part or "maj7" in part:
        return 'major_7th'
    elif "7" in part:
        return 'dominant_7th'
    elif "dim" in part:
        return 'diminished'
    elif "aug" in part:
        return 'augmented'
    elif "sus2" in part:
        return 'suspended_2nd'
    elif "sus4" in part:
        return 'suspended_4th'
    elif "P" in part:
        return 'power'
    # elif "m" in part:
    #     return 'minor'
    elif "M" in part or part.isupper():
        return 'major'
    else:
        return 'major'  # Default chord type if no specific symbol is found



def progression_to_root_notes(root_note, progression):
    progression_parts = progression.split('-')
    root_notes = []

    for part in progression_parts:
        # Remove chord quality symbols to find the interval for the root note of this chord
        print('part:', part)
        cleaned_part = part.replace("m6","").replace("m", "").replace("M", "").replace("7", "")
        interval = None

        # Find the interval for the current part
        for key, value in roman_numeral_intervals.items():
            if cleaned_part in value["numerals"]:
                interval = value["interval"]
                break

        if interval is not None:
            # Calculate the root note for this chord in the progression
            root_index = chromatic_scale.index(root_note)
            note_index = (root_index + interval) % 12
            new_root_note = chromatic_scale[note_index]
            root_notes.append(new_root_note)
        else:
            # If we couldn't find an interval, just append the root_note as a fallback
            root_notes.append(root_note)

    return root_notes
