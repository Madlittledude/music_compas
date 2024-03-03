import streamlit as st
import matplotlib.pyplot as plt

from chords import is_note_in_chord
from note_sets import guitar_strings_standard


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

chromatic_scale = [
    'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B'
]




def get_note_color(note, note_colors):
    # Directly return the color if the note exactly matches one of the keys
    if note in note_colors:
        return note_colors[note]
    
    # Handle notes written with sharp/flat notation
    for key in note_colors.keys():
        if note in key.split('/'):
            return note_colors[key]
    
    # Fallback color if note is not found
    return '#FFFFFF'  # White or any default color


def guitar_fretboard_visualization(note_colors, chord_notes, chord_degrees, show_degrees=False):
    fig, ax = plt.subplots(figsize=(18, 5))
    for string_number, string_name in enumerate(['E_low', 'A', 'D', 'G', 'B', 'E_high'], start=1):
        ax.plot([0, 15], [string_number, string_number], color='black', lw=2)
        
        for fret in range(0, 15):
            note = guitar_strings_standard[string_name][fret % 12]
            if is_note_in_chord(note, chord_notes):
                note_color = get_note_color(note, note_colors)  # Assume this function returns a color based on the note
                
                # Determine what to display (note or degree) and set color
                display_text = note if not show_degrees else chord_degrees[chord_notes.index(note)]
                text_color = 'black'  # Assuming white text for visibility against colored backgrounds
                
                ax.text(fret, string_number, display_text, ha='center', va='center', color=text_color, fontsize=12, bbox=dict(facecolor=note_color, edgecolor='none', boxstyle='round,pad=0.3'))
    
    for fret in range(1, 16):
        ax.plot([fret, fret], [1, 6], color='grey', lw=1)
    
    single_dot_frets = [3, 5, 7, 9]
    for fret in single_dot_frets:
        ax.plot(fret, 0.2, 'o', markersize=7, color='black', fillstyle='full')

    ax.plot(12, 0.1, 'o', markersize=7, color='black', fillstyle='full')
    ax.plot(12, 0.4, 'o', markersize=7, color='black', fillstyle='full')

    ax.axis([0, 15, 0, 7])
    ax.axis('off')
    st.pyplot(fig)


