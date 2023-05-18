# waveform visualizer for music, lags about 7 second behind
""" Created by: AK1R4S4T0H
"""
import numpy as np
import sounddevice as sd
import pygame
import random

# Audio settings
CHANNELS = 7
SAMPLE_RATE = 44100
BLOCK_SIZE = 800
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
WAVEFORM_MOVEMENT = 17000  # Adjust the value to control the pronounced movement of the waveform

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
    scaled_data = audio_data * (SCREEN_HEIGHT / 200) + (SCREEN_HEIGHT / 200)
    screen.fill(BACKGROUND_COLOR)

    waveforms = [scaled_data * (i + 170.5) / NUM_WAVEFORMS for i in range(NUM_WAVEFORMS)]

    waveform_height = SCREEN_HEIGHT / NUM_WAVEFORMS
    for i, waveform in enumerate(waveforms):
        y_offset = int(i * waveform_height + waveform_height / 550)
        waveform_points = np.column_stack((np.arange(SCREEN_WIDTH), waveform + y_offset)).astype(int)
        pygame.draw.lines(screen, WAVEFORM_COLORS[i], False, waveform_points, LINE_WIDTH)

    for particle in particles:
        particle.update()

        # Calculate the movement of the particle based on audio data
        movement_x = int(np.mean(audio_data) * PARTICLE_SPEED)
        movement_y = int(np.mean(audio_data) * PARTICLE_SPEED)

        if movement_x > 0:  # Check if movement_x is greater than zero
            particle.x += random.randint(-movement_x, movement_x)
        if movement_y > 0:  # Check if movement_y is greater than zero
            particle.y += random.randint(-movement_y, movement_y)
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
