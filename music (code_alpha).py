import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
import pygame
from music21 import converter, instrument, note, chord, stream
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, Activation
from keras.optimizers import Adam
import keras.utils
from PyQt5.QtGui import QFont


class MidiPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for MIDI playback
        self.generated_midi_file = 'output.mid'  # Default name for generated MIDI file
        self.midi_file = None

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()

        self.label = QLabel("Wellcome to Ai music generator.", self)
        self.label.setStyleSheet("background-color: #091833; color: white; font-size: 20px;")
        self.label.setFont(QFont('BROCHA',10))
        layout.addWidget(self.label)

        # Button to generate new MIDI file
        self.generateButton = QPushButton('Generate Music', self)
        self.generateButton.clicked.connect(self.generate_music)
        self.generateButton.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        layout.addWidget(self.generateButton)

        # Button to load MIDI file
        self.loadButton = QPushButton('Load MIDI File', self)
        self.loadButton.clicked.connect(self.load_midi)
        self.loadButton.setStyleSheet("background-color: #2196F3; color: white; font-size: 16px;")
        layout.addWidget(self.loadButton)

        # Button to play MIDI file
        self.playButton = QPushButton('Play MIDI', self)
        self.playButton.clicked.connect(self.play_midi)
        self.playButton.setEnabled(False)
        self.playButton.setStyleSheet("background-color: #FF9800; color: white; font-size: 16px;")
        layout.addWidget(self.playButton)

        # Button to stop MIDI playback
        self.stopButton = QPushButton('Stop', self)
        self.stopButton.clicked.connect(self.stop_midi)
        self.stopButton.setEnabled(False)
        self.stopButton.setStyleSheet("background-color: #f44336; color: white; font-size: 16px;")
        layout.addWidget(self.stopButton)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle('AI-Powered MIDI Player')
        self.setGeometry(300, 300, 500, 400)  # Increased the size of the window

    def generate_music(self):
        try:
            # Generate music using AI model
            self.generate_music_sequence()
            self.label.setText('Music generated successfully. You can now play it.')
            self.playButton.setEnabled(True)
            self.stopButton.setEnabled(True)
        except Exception as e:
            self.label.setText(f'Error generating music: {e}')

    def load_midi(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, "Select MIDI File", "", "MIDI Files (*.mid);;All Files (*)", options=options)
        if filePath:
            self.label.setText(f'Selected File: {filePath}')
            self.midi_file = filePath
            self.playButton.setEnabled(True)
            self.stopButton.setEnabled(True)

    def play_midi(self):
        if self.midi_file:
            pygame.mixer.music.load(self.midi_file)
        else:
            pygame.mixer.music.load(self.generated_midi_file)
        pygame.mixer.music.play()

    def stop_midi(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def closeEvent(self, event):
        if pygame.mixer.music.get_busy():
            self.stop_midi()
        pygame.mixer.quit()
        pygame.quit()
        event.accept()

    def generate_music_sequence(self):
        # Music generation using AI model
        # Simplified example: using predefined or random notes to simulate AI-generated sequence
        # In a real-world scenario, this method would integrate your RNN or GAN model to generate notes
        notes = ['C4', 'E4', 'G4', 'C5']
        offset = 0
        output_notes = []
        for pattern in notes:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)
            offset += 0.5

        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp=self.generated_midi_file)

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    player = MidiPlayer()
    player.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
