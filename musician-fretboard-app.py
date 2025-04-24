import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(page_title="Guitar Scale Visualizer", layout="wide")
st.title("Guitar Scale Visualizer")

# Define notes and their enharmonic equivalents
NOTES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

# Define common modes and their interval patterns
MODES = {
    'Major (Ionian)': [0, 2, 4, 5, 7, 9, 11],
    'Dorian': [0, 2, 3, 5, 7, 9, 10],
    'Phrygian': [0, 1, 3, 5, 7, 8, 10],
    'Lydian': [0, 2, 4, 6, 7, 9, 11],
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'Minor (Aeolian)': [0, 2, 3, 5, 7, 8, 10],
    'Locrian': [0, 1, 3, 5, 6, 8, 10],
    'Pentatonic Major': [0, 2, 4, 7, 9],
    'Pentatonic Minor': [0, 3, 5, 7, 10],
    'Blues': [0, 3, 5, 6, 7, 10]
}

# Standard guitar tuning (from high to low string)
GUITAR_TUNING = ['E', 'B', 'G', 'D', 'A', 'E']

# Number of frets to display
NUM_FRETS = 15

def get_note_at_position(string_note, fret):
    """Calculate the note at a specific fret position"""
    start_index = NOTES.index(string_note) if string_note in NOTES else NOTES.index(string_note.split('/')[0])
    note_index = (start_index + fret) % 12
    return NOTES[note_index]

def get_scale_notes(root_note, mode):
    """Get all notes in a scale based on root note and mode"""
    start_index = NOTES.index(root_note) if root_note in NOTES else NOTES.index(root_note.split('/')[0])
    return [NOTES[(start_index + interval) % 12] for interval in MODES[mode]]

def is_note_in_scale(note, scale_notes):
    """Check if a note is in the scale, handling enharmonic equivalents"""
    if '/' in note:
        return note.split('/')[0] in scale_notes or note.split('/')[1] in scale_notes
    return note in scale_notes

def display_fretboard(root_note, mode):
    """Display the fretboard with highlighted notes"""
    scale_notes = get_scale_notes(root_note, mode)
    
    # Create a header with fret numbers
    cols = st.columns([0.8] + [1] * NUM_FRETS)
    with cols[0]:
        st.markdown("### String")
    for i in range(NUM_FRETS):
        with cols[i+1]:
            st.markdown(f"### {i}")
    
    # Display each string with its notes
    for string in GUITAR_TUNING:
        cols = st.columns([0.8] + [1] * NUM_FRETS)
        with cols[0]:
            st.markdown(f"### {string}")
        
        for fret in range(NUM_FRETS):
            note = get_note_at_position(string, fret)
            with cols[fret+1]:
                is_root = note == root_note or (('/' in note) and (root_note in note.split('/')))
                
                if is_note_in_scale(note, scale_notes):
                    if is_root:
                        st.markdown(f"<div style='background-color: #ff5733; color: white; border-radius: 50%; padding: 10px; text-align: center;'>{note}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='background-color: #4287f5; color: white; border-radius: 50%; padding: 10px; text-align: center;'>{note}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='padding: 10px; text-align: center;'>{note}</div>", unsafe_allow_html=True)

# Create sidebar controls
st.sidebar.title("Scale Settings")

# Simplify display names for the dropdown
display_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note_mapping = {
    'C#': 'C#/Db',
    'D#': 'D#/Eb',
    'F#': 'F#/Gb',
    'G#': 'G#/Ab',
    'A#': 'A#/Bb'
}

selected_note = st.sidebar.selectbox("Select Root Note", display_notes)
# Map display note to internal representation
if selected_note in note_mapping:
    selected_note = note_mapping[selected_note]

selected_mode = st.sidebar.selectbox("Select Mode", list(MODES.keys()))

# Display explanatory text
st.sidebar.markdown("---")
st.sidebar.markdown("""
### How to use:
1. Select your root note
2. Choose a mode/scale
3. The fretboard will highlight all notes in the selected scale
4. Root notes are highlighted in orange
5. Other scale notes are highlighted in blue
""")

# Display the fretboard with the selected scale
display_fretboard(selected_note, selected_mode)

# Add legend
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    st.markdown("<div style='background-color: #ff5733; color: white; border-radius: 50%; padding: 10px; text-align: center; margin: 5px;'>Root Note</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='background-color: #4287f5; color: white; border-radius: 50%; padding: 10px; text-align: center; margin: 5px;'>Scale Note</div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"**Current Scale:** {selected_note} {selected_mode}")

# Display scale notes
scale_notes = get_scale_notes(selected_note, selected_mode)
st.markdown(f"**Notes in this scale:** {', '.join(scale_notes)}")

# Add explanation of the selected mode
mode_explanations = {
    'Major (Ionian)': "The standard major scale with a bright, happy sound.",
    'Dorian': "Minor scale with a raised 6th, has a jazzy, slightly minor sound.",
    'Phrygian': "Dark minor scale with a lowered 2nd, has a Spanish or Middle Eastern feel.",
    'Lydian': "Major scale with a raised 4th, has a dreamy, floating quality.",
    'Mixolydian': "Major scale with a lowered 7th, common in rock, blues and jazz.",
    'Minor (Aeolian)': "The standard natural minor scale with a melancholic sound.",
    'Locrian': "The darkest mode with a lowered 2nd and 5th, used in jazz and metal.",
    'Pentatonic Major': "Five-note scale derived from the major scale, very common in folk and pop.",
    'Pentatonic Minor': "Five-note scale derived from the minor scale, popular in rock, blues, and many forms of music.",
    'Blues': "Minor pentatonic with an added b5 'blue note', the foundation of blues music."
}

st.markdown(f"**About {selected_mode}:** {mode_explanations.get(selected_mode, '')}")
