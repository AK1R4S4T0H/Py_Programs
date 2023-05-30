import numpy as np
import sounddevice as sd
import pygame
from scipy.fft import fft
import tkinter as tk
from tkinter import ttk

# Audio settings
CHANNELS = 7
SAMPLE_RATE = 44100
BLOCK_SIZE = 512

# Visualization settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (0, 0, 0)
NUM_WAVEFORMS = 7
WAVEFORM_COLORS = [(255, 120, 0), (255, 200, 0), (0, 255, 100), (0, 150, 255), (0, 0, 255), (255, 0, 255), (255, 255, 255)]
LINE_WIDTH = 2
WAVEFORM_MOVEMENT = 99000  # pronounced movement of the waveform

# Frequency settings
LOW_FREQ = 60
HIGH_FREQ = 3000
NUM_FREQ_BINS = 700

freq_bins = np.logspace(np.log10(LOW_FREQ), np.log10(HIGH_FREQ), NUM_FREQ_BINS)

waveform_freq_ranges = np.linspace(LOW_FREQ, HIGH_FREQ, NUM_WAVEFORMS + 1)
waveform_freq_ranges = list(zip(waveform_freq_ranges[:-1], waveform_freq_ranges[1:]))

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Waveform")


def audio_capture_callback(indata, frames, time, status):
    audio_data = indata.mean(axis=1)
    audio_data = np.interp(np.linspace(7, len(audio_data) + 1/100000000000, SCREEN_WIDTH), np.arange(len(audio_data)), audio_data)
    scaled_data = audio_data * (SCREEN_HEIGHT / 40) + (SCREEN_HEIGHT / 40)
    screen.fill(BACKGROUND_COLOR)

    fft_data = np.abs(fft(audio_data))
    freq_magnitudes = np.interp(freq_bins, np.linspace(0, SAMPLE_RATE, len(fft_data)), fft_data)

    waveforms = [scaled_data * (i + 22) / NUM_WAVEFORMS for i in range(NUM_WAVEFORMS)]

    waveform_height = SCREEN_HEIGHT / NUM_WAVEFORMS
    for i, waveform in enumerate(waveforms):
        y_offset = int(i * waveform_height / 300)
        scaled_waveform = waveform * (i + 25) / NUM_WAVEFORMS
        freq_range = list(waveform_freq_ranges)[i]
        waveform_points = np.column_stack((np.arange(SCREEN_WIDTH), scaled_waveform + y_offset)).astype(int)
        pygame.draw.lines(screen, WAVEFORM_COLORS[i], False, waveform_points, LINE_WIDTH)

    for i, waveform in enumerate(waveforms):
        y_offset = int(i * waveform_height / 100)
        scaled_waveform = waveform * (i + 40) / NUM_WAVEFORMS
        freq_range = list(waveform_freq_ranges)[i]
        waveform_points = np.column_stack((np.arange(SCREEN_WIDTH), scaled_waveform + y_offset)).astype(int)
        pygame.draw.lines(screen, WAVEFORM_COLORS[i], False, waveform_points, LINE_WIDTH)


    for i, waveform in enumerate(waveforms):
        y_offset = int(i * waveform_height / 150)
        scaled_waveform = waveform * (i + 60) / NUM_WAVEFORMS
        freq_range = list(waveform_freq_ranges)[i]
        waveform_points = np.column_stack((np.arange(SCREEN_WIDTH), scaled_waveform + y_offset)).astype(int)
        pygame.draw.lines(screen, WAVEFORM_COLORS[i], False, waveform_points, LINE_WIDTH)

    for i, waveform in enumerate(waveforms):
        y_offset = int(i * waveform_height / 300)
        scaled_waveform = waveform * (i + 15) / NUM_WAVEFORMS
        freq_range = list(waveform_freq_ranges)[i]
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
