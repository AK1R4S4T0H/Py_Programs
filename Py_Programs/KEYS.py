# waveform visualizer for music, lags about 7 second behind
""" Created by: AK1R4S4T0H
"""
import numpy as np
import sounddevice as sd
import pygame
import random

# Audio settings
CHANNELS = 20
SAMPLE_RATE = 44100
BLOCK_SIZE = 500
# Visualization settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = (0, 0, 0)
NUM_WAVEFORMS = 7
WAVEFORM_COLORS = [(255, 0, 0), (255, 255, 0), (0, 0, 255), (50, 255, 50), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
LINE_WIDTH = 2
NUM_PARTICLES = 20
PARTICLE_SPEED = 20
PARTICLE_RADIUS = 1
WAVEFORM_MOVEMENT = 9  # Adjust the value to control the pronounced movement of the waveform

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Waveform Visualizer")

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def update(self):
        self.x += random.randint(-PARTICLE_SPEED, PARTICLE_SPEED)
        self.y += random.randint(-PARTICLE_SPEED, PARTICLE_SPEED)
        self.x %= SCREEN_WIDTH
        self.y %= SCREEN_HEIGHT

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), PARTICLE_RADIUS)

particles = [Particle(random.randint(0, SCREEN_WIDTH - 1), random.randint(0, SCREEN_HEIGHT),
                      (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
             for _ in range(NUM_PARTICLES)]

def audio_capture_callback(indata, frames, time, status):
    audio_data = indata.mean(axis=1)
    scaled_data = audio_data * (SCREEN_HEIGHT / 200) + (SCREEN_HEIGHT / 2)
    screen.fill(BACKGROUND_COLOR)

    waveform_height = SCREEN_HEIGHT // NUM_WAVEFORMS
    for i in range(NUM_WAVEFORMS):
        y_offset = i * waveform_height

        # Apply the Fast Fourier Transform (FFT) to the waveform data
        spectrum = np.fft.fft(scaled_data)
        frequencies = np.fft.fftfreq(len(spectrum), d=1 / SAMPLE_RATE)
        amplitudes = np.abs(spectrum)

        
        freq_range_start = i * (SAMPLE_RATE // (NUM_WAVEFORMS * 2))
        freq_range_end = (i + 1) * (SAMPLE_RATE // (NUM_WAVEFORMS * 2))
        mask = np.logical_and(frequencies >= freq_range_start, frequencies < freq_range_end)
        waveform_spectrum = spectrum[mask]
        waveform_frequencies = frequencies[mask]
        waveform_amplitudes = amplitudes[mask]

      
        peak_index = np.argmax(waveform_amplitudes)
        peak_frequency = waveform_frequencies[peak_index]
        peak_amplitude = waveform_amplitudes[peak_index]

       
        frequency_range = (60, 3000)  # Adjust the frequency range as needed
        normalized_frequency = np.interp(peak_frequency, [0, SAMPLE_RATE / 2], frequency_range)

       
        line_position = int(SCREEN_WIDTH * (normalized_frequency - frequency_range[0]) / (frequency_range[1] - frequency_range[0]))

        line_start = (line_position, y_offset)
        line_end = (line_position, y_offset + waveform_height)
        pygame.draw.line(screen, WAVEFORM_COLORS[i], line_start, line_end, LINE_WIDTH)

    for particle in particles:
        particle.update()

        movement_x = np.mean(audio_data) * PARTICLE_SPEED
        movement_y = np.mean(audio_data) * PARTICLE_SPEED

        if movement_x > 0:
            particle.x += random.randint(-int(movement_x), int(movement_x))
        if movement_y > 0:
            particle.y += random.randint(-int(movement_y), int(movement_y))

        particle.x %= SCREEN_WIDTH
        particle.y %= SCREEN_HEIGHT

        particle.draw()

    pygame.display.flip()

stream = sd.InputStream(callback=audio_capture_callback, channels=CHANNELS, samplerate=SAMPLE_RATE,
                        blocksize=BLOCK_SIZE, device="pulse", latency=0.00000000000000000001)
stream.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.event.pump()

stream.stop()
stream.close()
pygame.quit()