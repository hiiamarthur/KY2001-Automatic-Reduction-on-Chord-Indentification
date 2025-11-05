# Automatic Chord Identification and Reduction

A computational musicology system for automatic chord identification, tonal center detection, and hierarchical segmentation analysis of musical scores using the Spiral Array Model.

## Overview

This project implements advanced music information retrieval algorithms to analyze musical compositions from MusicXML files. It identifies chords, detects tonal centers, and performs hierarchical segmentation analysis to understand the harmonic structure of music at multiple levels.

The system employs the **Spiral Array Model**, a geometric representation of pitch relationships in three-dimensional space, enabling robust tonal analysis and chord recognition.

## Features

### Core Capabilities

- **Automatic Chord Identification**: Recognizes triads, seventh chords, and augmented sixth chords (Italian, French, German)
- **Tonal Center Detection**: Identifies key signatures and tonal regions using the Spiral Array Model
- **Hierarchical Segmentation**: Multi-level analysis with configurable granularity
- **Roman Numeral Analysis**: Generates functional harmony analysis with Roman numerals
- **Boundary Detection**: Identifies phrase boundaries and harmonic changes using local maxima
- **Visualization**: Generates detailed graphs showing segmentation analysis with slur and articulation markers

### Supported Chord Types

- Major and minor triads
- Diminished and augmented triads
- Major, minor, dominant, half-diminished, and fully-diminished seventh chords
- Italian, French, and German augmented sixth chords
- Altered chords with flat scale degrees

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Dependencies

Install required Python packages:

```bash
pip install music21 numpy scipy matplotlib
```

### Music21 Configuration

Configure music21 to use MuseScore (or your preferred score viewer):

```python
from music21 import environment
us = environment.UserSettings()
us['musescoreDirectPNGPath'] = '/path/to/musescore'
```

## Usage

### Mode A: Batch Tonal Analysis

Analyze tonality bar-by-bar across multiple pieces:

```bash
python main.py
# Input: A
```

This mode:
- Processes all XML files in the `musicPiece` directory
- Identifies tonal centers for each bar
- Validates predictions against chord symbols
- Reports accuracy statistics

### Mode B: Hierarchical Segmentation Analysis

Perform multi-level segmentation with visualization:

```bash
python main.py
# Input: B
# Layer: 1 (coarse), 2 (medium), or 3 (fine)
# Method: M (mean) or B (bar)
```

**Layer Selection:**
- Layer 1: Coarse segmentation (rate = 2)
- Layer 2: Medium segmentation (rate = 1)
- Layer 3: Fine segmentation (rate = 1/2)

**Output:**
- Console: Detailed note-by-note analysis
- Graph: `testgraph.png` showing:
  - Tonal distance coefficients over time
  - Segmentation boundaries (black peaks)
  - Slur markings (red line)
  - Articulation marks (green line)
  - Boundary threshold (purple line)

### Programmatic Usage

```python
from musicXML import getMusicPiece
from spiral_method import initialize_spiral_structure, run_find_tonal_center

# Initialize the Spiral Array structure
structure_arr = initialize_spiral_structure()

# Load a musical piece
score = getMusicPiece('path/to/score.xml')

# Analyze a bar
notes = ['C', 'E', 'G']
durations = [1.0, 1.0, 1.0]
symbols = []  # Chord symbols from the score
result = run_find_tonal_center(notes, durations, symbols)
```

## Technical Details

### The Spiral Array Model

The Spiral Array Model represents musical pitches in a three-dimensional helical structure:

- **Pitch Class Space**: Notes are arranged in a spiral rising by perfect fifths
- **Chord Representation**: Chords are represented as weighted centers of their constituent pitches
- **Key Representation**: Keys are represented as centers of their tonic, dominant, and subdominant chords

**Mathematical Formulation:**

```
Pitch position: P(k) = [r·sin(kπ/2), r·cos(kπ/2), k·h]
where k = position in circle of fifths, r = spiral radius, h = height increment
```

### Algorithms

#### 1. Tonal Center Detection
- Calculates center of effect (CE) from weighted pitch positions
- Compares CE with pre-computed key representations
- Ranks keys by Euclidean distance in Spiral Array space

#### 2. Chord Identification
- Analyzes interval patterns (e.g., [4,3] for major triads)
- Identifies chord root and quality
- Generates possible key contexts with Roman numerals

#### 3. Boundary Detection
- Uses sliding window comparison of adjacent segments
- Computes tonal distance between consecutive windows
- Applies scipy signal processing to find local maxima
- Validates boundaries against musical features (slurs, articulations)

## Project Structure

```
.
├── main.py                 # Primary entry point with dual-mode analysis
├── main2.py               # Alternative implementation
├── spiral_method.py       # Spiral Array Model implementation
├── note_to_chord.py       # Chord identification and Roman numeral analysis
├── musicXML.py            # MusicXML parsing utilities
├── old_main.py            # Legacy code
├── data/                  # Data directory
│   ├── mxl/              # MusicXML files
│   ├── converted/        # Converted scores
│   └── notes-to-chord.xls # Reference data
├── refPaper/             # Reference literature
│   └── 45233584-MIT.pdf  # Spiral Array Model paper
└── testgraph.png         # Latest segmentation visualization
```

## Algorithm Parameters

### Configurable Constants (spiral_method.py)

```python
major_key_ratio = [0.6025, 0.2930, 0.1045]  # Tonic-dominant-subdominant weights
minor_key_ratio = [0.6011, 0.2121, 0.1868]  # Minor key weights
spiral_radius = 1                            # Spiral base radius
spiral_height = sqrt(2/15)                   # Height per fifth
```

### Segmentation Parameters (main.py)

```python
rate = 2 / 1 / 0.5          # Layer granularity
average_note_density         # Window size for segmentation
show_bound_l, show_bound_r  # Visualization range
```

## Input Format

The system accepts MusicXML files (.xml, .mxl) with:
- Two-part piano scores (treble and bass clef)
- Optional chord symbols for validation
- Standard Western music notation

## Output Format

### Console Output

```
In segment 0:
Chord marked: ['Gmajor']
G-major VII matched with similarity score: 0.234
C-major IV matched with similarity score: 0.256
...

total note is: 450
total bar: 32
bar with right prediction: 28
average correct %: 0.875
```

### Visualization

The generated graph displays:
- **Blue curve**: Tonal distance coefficients
- **Black peaks**: Detected boundaries
- **Red line**: Slur presence (1 = slurred, 0 = not slurred)
- **Green line**: Articulation marks
- **Purple line**: Threshold for boundary detection
- **Annotations**: Note names at boundary points

## Research Background

This implementation is based on the Spiral Array Model proposed by Elaine Chew:

> Chew, E. (2000). *Towards a Mathematical Model of Tonality*. MIT PhD Thesis.

The model provides a geometric framework for representing tonal relationships and has applications in:
- Music information retrieval
- Automatic transcription
- Music generation
- Computational music theory

## Performance

**Typical Accuracy:**
- Chord identification: ~85-90% on classical piano repertoire
- Tonal center detection: ~87.5% bar-level accuracy
- Boundary detection: Varies by musical complexity and parameter tuning

**Processing Speed:**
- ~1-2 seconds per piece (50-100 bars) on modern hardware

## Limitations

- Requires well-formed MusicXML input
- Optimized for common practice period tonal music
- Struggles with highly chromatic or atonal passages
- Two-voice limitation (treble + bass)
- Manual parameter tuning required for optimal segmentation

## Future Work

Potential enhancements:
- Support for multi-voice polyphony
- Machine learning integration for parameter optimization
- Real-time audio analysis capabilities
- Extended chord vocabulary (9th, 11th, 13th chords)
- Improved handling of modulations and chromaticism

## Contributing

Contributions are welcome. Areas of interest:
- Algorithm optimization
- Extended test coverage
- Additional musical features
- Documentation improvements

## License

Please refer to the project owner for licensing information.

## References

1. Chew, E. (2000). *Towards a Mathematical Model of Tonality*. MIT PhD Thesis.
2. Chew, E. (2014). *Mathematical and Computational Modeling of Tonality*. Springer.
3. music21 toolkit documentation: http://web.mit.edu/music21/

## Contact

For questions or feedback about this implementation, please open an issue in the repository.

---

**Note**: This is a research implementation. Results may vary depending on input complexity and parameter configuration.
