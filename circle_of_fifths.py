import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.font_manager import FontProperties

from note_sets import circle_of_fifths_notes


# Assuming circle_of_fifths_notes and other necessary variables are defined outside this function
def draw_circle_of_fifths(root, chord_notes, chord_degrees):
    fig, ax = plt.subplots(figsize=(8, 8))
    circle_radius = 1.1  # Increase the radius slightly to spread out the notes
    circle = plt.Circle((0, 0), circle_radius, color='lightgray', linewidth=2, fill=False)
    ax.add_artist(circle)

    font = FontProperties(family='Times New Roman', style='normal', size=14)

    # Assuming circle_of_fifths_notes is a list that contains your circle of fifths notes
    try:
        root_index = circle_of_fifths_notes.index(root)
    except ValueError:
        # This will handle cases where the root note is an enharmonic equivalent not directly listed in circle_of_fifths_notes
        for i, note in enumerate(circle_of_fifths_notes):
            if root in note.split('/'):
                root_index = i
                break

    rotation = (root_index * -30) % 360

    text_radius = 1.15  # Slightly larger radius for text placement

    for i, circle_note in enumerate(circle_of_fifths_notes):
        angle = np.deg2rad((i * 30) + rotation + 90)
        x, y = np.cos(angle) * text_radius, np.sin(angle) * text_radius

        # Splitting the circle note if it contains a '/'
        split_notes = circle_note.split('/')
        matched_note = None

        # Check if any of the split notes or the whole note is in chord_notes
        for chord_note in chord_notes:
            if chord_note in split_notes or chord_note == circle_note:
                matched_note = chord_note
                break

        if matched_note:
            note_degree = chord_degrees[chord_notes.index(matched_note)]
            note_text = f"{circle_note}$_{{{note_degree}}}$"  # Using LaTeX for subscript with degree
            ax.text(x, y, note_text, ha='center', va='center', fontproperties=font, weight='bold', fontsize=16, color='blue')
        else:
            ax.text(x, y, circle_note, ha='center', va='center', fontproperties=font, color='black')

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    plt.show()


    st.pyplot(fig)


