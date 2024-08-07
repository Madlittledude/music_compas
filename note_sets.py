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
    'Melodic Minor Ascending': [0, 2, 3, 5, 7, 9, 11],
    'Melodic Minor Descending': [0, 2, 4, 5, 7, 8, 10]  # Same as natural minor when descending, but included so I don't need to write logic for that similarity. 
                                                        # Idk what it'd be for yet. Maybe a function to detect a similarity in interval pattern with something else...
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


mode_descriptions = {
    "Ionian": {
        "simple": "Uplifting, joyful, and stable, suitable for a wide range of musical genres.",
        "deep": "Ionian mode, synonymous with the major scale, establishes a bright tonal foundation, characterized by a sequence of whole and half steps that create a clear, consonant harmonic structure. This mode fosters a sense of resolution and completeness, making it ideal for conveying feelings of happiness and reassurance."
    },
    "Dorian": {
        "simple": "Jazzy, bluesy, and soulful with a touch of melancholy.",
        "deep": "Dorian mode modifies the natural minor scale by raising the sixth degree, introducing a lighter, more hopeful quality amidst its overall minor character. This alteration allows for a complex interplay of melancholy and optimism, suitable for expressive genres like jazz and blues where emotional depth and nuance are paramount."
    },
    "Phrygian": {
        "simple": "Dark, tense, and exotic, fitting for flamenco and metal.",
        "deep": "Phrygian mode, with its lowered second degree, provides a stark contrast to the foundational major scale, offering a sound that is both exotic and foreboding. This mode's intervallic structure, particularly the minor second interval, creates a tense and mysterious atmosphere, ideal for genres that rely heavily on drama and intensity."
    },
    "Lydian": {
        "simple": "Ethereal, dreamy, and floating, often used in film scores.",
        "deep": "Lydian mode stands out with its raised fourth degree, diverging from the major scale to produce an airy, mystical quality. This single alteration affects the tonal gravity of the scale, reducing tension and creating an open, unresolved sonic landscape that is ideal for invoking a sense of wonder and exploration."
    },
    "Mixolydian": {
        "simple": "Bluesy, relaxed, with a slightly unresolved tonal quality.",
        "deep": "Mixolydian mode alters the major scale by lowering the seventh degree, which introduces a subtle tension and an unfinished quality to the otherwise bright major tonality. This mode is favored in music that thrives on a laid-back, yet emotionally complex soundscape, such as blues, rock, and folk."
    },
    "Aeolian": {
        "simple": "Sorrowful, introspective, and richly nuanced.",
        "deep": "Aeolian mode, or the natural minor scale, deepens the emotional palette of music by employing a scale structure that naturally conveys sadness and introspection through its use of lowered third, sixth, and seventh degrees. This mode's capacity to articulate a broad spectrum of deep emotions makes it a fundamental tool in both classical and contemporary music composition."
    },
    "Locrian": {
        "simple": "Dissonant, unstable, and tense, rarely used in mainstream music.",
        "deep": "Locrian mode is characterized by a diminished fifth, which destabilizes the tonal center and creates inherent dissonance and tension within the scale. Due to its challenging nature, Locrian is seldom employed as a principal mode but is used effectively to create eerie and unsettling atmospheres in avant-garde and experimental music settings."
    }
}

def get_scale_notes_and_degrees(mode, root_note, ascending=True):
    """Retrieve scale notes and corresponding degrees for a given mode starting from the root note."""
    intervals = mode_intervals.get(mode, [])
    if not ascending and 'Melodic Minor' in mode:
        intervals = mode_intervals.get(mode.replace("Ascending", "Descending"), [])
    notes = []
    degrees = []
    root_index = chromatic_scale.index(root_note)
    for interval in intervals:
        note_index = (root_index + interval) % 12
        note = chromatic_scale[note_index]
        degree = interval_to_degree(interval)
        notes.append(note)
        degrees.append(degree)
    return notes, degrees

