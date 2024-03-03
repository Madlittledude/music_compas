guitar_strings_standard = {
    'E_low': ['E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E'],
    'A': ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A'],
    'D': ['D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D'],
    'G': ['G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G'],
    'B': ['B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B'],
    'E_high': ['E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E']
}



# The Circle of Fifths notes (simplified for visualization)
circle_of_fifths_notes = ['C','F','A#/Bb','D#/Eb','G#/Ab','C#/Db','F#/Gb','B','E','A','D','G']

# ['C','F','Bb','Eb','Ab','Db','Gb','B','E','A','D','G']

# Comprehensive chromatic scale including both sharps and flats
# Note: This simplification serves to explain the concept. In a real application,
# you would need to dynamically adjust the chromatic scale based on the root note.
chromatic_scale = [
    'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B'
]


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
