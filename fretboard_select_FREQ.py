import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

class SineWave:
    def __init__(self, frequency, amplitude=1.0, phase=0.0, sample_rate=44100, duration=1):
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        self.sample_rate = sample_rate
        self.duration = duration
        self.time = np.arange(0, self.duration, 1 / self.sample_rate)
        self.wave = self.generate_wave()

    def generate_wave(self):
        return self.amplitude * np.sin(2 * np.pi * self.frequency * self.time + self.phase)

    @staticmethod
    def combine_waves(waves):
        combined_wave = np.sum([wave.wave for wave in waves], axis=0)
        return combined_wave

def update_selected_notes_display(graph_placeholders):
    # Function to update the graphs based on selected notes
    # This function now takes a list of placeholders to dynamically update the graphs

    # Checkbox for each note to control whether it's displayed in the combined wave
    frequencies = []
    selected_notes_list = []  # List to hold selected notes for printing

    for idx, note_info in enumerate(st.session_state['selected_notes']):
        frequency = float(note_info['frequency'].split('(')[1].split(' ')[0])
        display_note = st.checkbox(
            f"Display Note {idx + 1}: {note_info['note']} ({note_info['frequency']}) - String: {note_info['string']}, Fret: {note_info['fret']}",
            value=True,
            key=f"checkbox_{idx}"
        )
        if display_note:
            frequencies.append(frequency)
            selected_notes_list.append(frequency)

    # Convert the list of frequencies to string representation
    selected_notes_str = str(selected_notes_list)

    # Update a text element with the string representation of the list
    st.text("Selected Frequencies:")
    st.text(selected_notes_str)

    # Button to generate the combined sine wave
    if st.button("Generate Combined Wave"):
        if frequencies:
            waves = [SineWave(freq) for freq in frequencies]
            combined_wave = SineWave.combine_waves(waves)

            fig, ax = plt.subplots()
            ax.plot(waves[0].time[:1000], combined_wave[:1000])
            ax.set_title('Combined Sine Waves')
            ax.set_xlabel('Time')
            ax.set_ylabel('Amplitude')

            # Reduce the size of the graph by 30%
            fig.set_size_inches(fig.get_size_inches() * 0.7)
            graph_placeholders[0][1].pyplot(fig)




def display_history():
    st.write("History of Chords:")
    for chord_index, chord in enumerate(st.session_state['notes_history'], start=1):
        # Gather the notes and frets as before
        notes = [note['note'] for note in chord]
        # Extract the frequency numbers, convert to float, and remove " Hz"
        frequencies = [float(note['frequency'].split(' ')[0][1:]) for note in chord]
        frets = [f"String: {note['string']}, Fret: {note['fret']}" for note in chord]
        
        # Format the details into a compact representation
        chord_details = f"Chord {chord_index}:\nNotes: {notes}\nFrequencies: {frequencies}\nFrets: {frets}"
        
        # Display the formatted chord details
        st.code(chord_details, language='python')


def main():
    # Containers for layout management
    fretboard_container = st.container()
    graph_container = st.container()

    with fretboard_container:
        fretboard_select()

    with graph_container:
        # This list will hold triplets of placeholders: one for note text, one for graph, one for checkbox
        graph_placeholders = []

        # This placeholder will be dynamically updated with notes, graphs, and checkboxes
        for idx in range(len(st.session_state['selected_notes'])):
            note_placeholder = st.empty()
            graph_placeholder = st.empty()
            checkbox = st.empty()
            graph_placeholders.append((note_placeholder, graph_placeholder, checkbox))

        update_selected_notes_display(graph_placeholders)
        # Display the history of chords
        display_history()

        
def fretboard_select():
    guitar_string_frequencies = {
        'strings': ['E_low', 'A', 'D', 'G', 'B', 'E_high'],
        'fretboard': [
            ['E (82.41 Hz)', 'F (87.31 Hz)', 'F#/Gb (92.5 Hz)', 'G (98.0 Hz)', 'G#/Ab (103.83 Hz)', 'A (110.0 Hz)', 'A#/Bb (116.55 Hz)', 'B (123.48 Hz)', 'C (130.82 Hz)', 'C#/Db (138.6 Hz)', 'D (146.84 Hz)', 'D#/Eb (155.57 Hz)', 'E (164.82 Hz)'],
            ['A (110.0 Hz)', 'A#/Bb (116.54 Hz)', 'B (123.47 Hz)', 'C (130.81 Hz)', 'C#/Db (138.59 Hz)', 'D (146.83 Hz)', 'D#/Eb (155.56 Hz)', 'E (164.81 Hz)', 'F (174.61 Hz)', 'F#/Gb (185.0 Hz)', 'G (196.0 Hz)', 'G#/Ab (207.65 Hz)', 'A (220.0 Hz)'],
            ['D (146.83 Hz)', 'D#/Eb (155.56 Hz)', 'E (164.81 Hz)', 'F (174.61 Hz)', 'F#/Gb (184.99 Hz)', 'G (195.99 Hz)', 'G#/Ab (207.65 Hz)', 'A (220.0 Hz)', 'A#/Bb (233.08 Hz)', 'B (246.94 Hz)', 'C (261.62 Hz)', 'C#/Db (277.18 Hz)', 'D (293.66 Hz)'],
            ['G (196.0 Hz)', 'G#/Ab (207.65 Hz)', 'A (220.0 Hz)', 'A#/Bb (233.08 Hz)', 'B (246.94 Hz)', 'C (261.63 Hz)', 'C#/Db (277.19 Hz)', 'D (293.67 Hz)', 'D#/Eb (311.13 Hz)', 'E (329.63 Hz)', 'F (349.23 Hz)', 'F#/Gb (370.0 Hz)', 'G (392.0 Hz)'],
            ['B (246.94 Hz)', 'C (261.62 Hz)', 'C#/Db (277.18 Hz)', 'D (293.66 Hz)', 'D#/Eb (311.12 Hz)', 'E (329.63 Hz)', 'F (349.23 Hz)', 'F#/Gb (369.99 Hz)', 'G (391.99 Hz)', 'G#/Ab (415.3 Hz)', 'A (440.0 Hz)', 'A#/Bb (466.16 Hz)', 'B (493.88 Hz)'],
            ['E (329.63 Hz)', 'F (349.23 Hz)', 'F#/Gb (370.0 Hz)', 'G (392.0 Hz)', 'G#/Ab (415.31 Hz)', 'A (440.0 Hz)', 'A#/Bb (466.17 Hz)', 'B (493.89 Hz)', 'C (523.26 Hz)', 'C#/Db (554.37 Hz)', 'D (587.33 Hz)', 'D#/Eb (622.26 Hz)', 'E (659.26 Hz)']
        ]
    }

    if 'selected_notes' not in st.session_state:
        st.session_state['selected_notes'] = []

    if 'notes_history' not in st.session_state:
        st.session_state['notes_history'] = []

    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            margin: 0;
        }
        .string-line {
            height: 1px;
            background-color: black;
            position: relative;
            top: -20px;
            z-index: -1;
        }
        </style>
        """, unsafe_allow_html=True)

    strings = guitar_string_frequencies['strings'][::-1]  # Reverse the order of strings for display

    for i, string_name in enumerate(strings):
        st.markdown('<div class="string-line"></div>', unsafe_allow_html=True)
        cols = st.columns(13)
        for idx in range(13):
            # Note that we access the fretboard using the original index of the string before it was reversed
            original_string_index = len(guitar_string_frequencies['strings']) - 1 - i
            note_info = guitar_string_frequencies['fretboard'][original_string_index][idx]
            # Splitting the note_info to extract the note name correctly
            note_parts = note_info.split(' ')
            # Assuming the note name is everything except the last two elements (frequency and Hz)
            note_name = ' '.join(note_parts[:-2])
            frequency = note_parts[-2]  # The frequency value
            
            button_key = f"button_{string_name}_{idx}"
            if cols[idx].button(note_name, key=button_key):  # Ensure note_name is a string
                selected_note_info = {
                    'note': note_name,
                    'string': string_name,
                    'fret': idx,
                    'frequency': frequency + ' Hz'  # Adding 'Hz' for clarity
                }
                if selected_note_info not in st.session_state['selected_notes']:
                    st.session_state['selected_notes'].append(selected_note_info)

    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button("Clear Selected Notes"):
            # Check if there are any selected notes before clearing and appending to history
            if st.session_state['selected_notes']:
                st.session_state['notes_history'].append(st.session_state['selected_notes'].copy())
                st.session_state['selected_notes'] = []

    with action_col2:
        if st.button("Reset All"):
            # Check if there are any selected notes or notes in history before resetting
            if st.session_state['selected_notes'] or st.session_state['notes_history']:
                st.session_state['selected_notes'] = []
                st.session_state['notes_history'] = []



if __name__ == "__main__":
    main()
