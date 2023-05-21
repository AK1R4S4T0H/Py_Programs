# waveform visualizer for music
""" Created by: AK1R4S4T0H
"""
import numpy as np
import sounddevice as sd
import pygame
from scipy.fft import fft

# Audio settings
CHANNELS = 4
SAMPLE_RATE = 44100
BLOCK_SIZE = 200

# Visualization settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (0, 0, 0)
NUM_WAVEFORMS = 7
WAVEFORM_COLORS = [(255, 120, 0), (255, 200, 0), (0, 255, 100), (0, 150, 255), (0, 0, 255), (255, 0, 255), (255, 255, 255)]
LINE_WIDTH = 2
WAVEFORM_MOVEMENT = 9 # pronounced movement of the waveform

# Frequencies
FREQUENCIES = [61.63, 293.66, 929.63, 1449.23, 2292.00, 2640.00, 3193.88]

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Waveform Visualizer")


def audio_capture_callback(indata, frames, time, status):
    audio_data = indata.mean(axis=1)
    audio_data = np.interp(np.linspace(0, len(audio_data) + 1/100000000000000000000, SCREEN_WIDTH), np.arange(len(audio_data)), audio_data)
    scaled_data = audio_data * (SCREEN_HEIGHT / 1) + (SCREEN_HEIGHT / 20)
    screen.fill(BACKGROUND_COLOR)

    waveforms = [scaled_data * (i + 1) / NUM_WAVEFORMS for i in range(NUM_WAVEFORMS)]

    waveform_height = SCREEN_HEIGHT / NUM_WAVEFORMS
    for i, waveform in enumerate(waveforms):
        y_offset = int(i * waveform_height + waveform_height // 100000)
        scaled_waveform = waveform * (i + 1) / NUM_WAVEFORMS  # Adjust the scaling factor
        waveform_points = np.column_stack((np.arange(SCREEN_WIDTH), scaled_waveform + y_offset)).astype(int)
        pygame.draw.lines(screen, WAVEFORM_COLORS[i], False, waveform_points, LINE_WIDTH)

    pygame.display.flip()

stream = sd.InputStream(callback=audio_capture_callback, channels=CHANNELS, samplerate=SAMPLE_RATE,
                        blocksize=BLOCK_SIZE, device="pulse")
stream.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.event.pump()

stream.stop()
stream.close()
