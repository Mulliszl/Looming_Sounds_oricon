from datetime import datetime
import pygame
import random
import time
import csv
import os
import numpy as np
import random

image = pygame.image.load('greysquare.png')
pygame.font.init()
resolution = (1920, 1080)  # screen resolution
screen = pygame.display.set_mode(resolution)  # create display
font = pygame.font.SysFont("Arial", 50)  # set font and size

def add_noise(image, intensity):
    width, height = image.get_size()
    noisy_image = pygame.Surface((width, height))
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = image.get_at((x, y))
            noise = random.randint(-intensity, intensity)
            r = max(0, min(255, r + noise))
            g = max(0, min(255, g + noise))
            b = max(0, min(255, b + noise))
            noisy_image.set_at((x, y), (r, g, b, a))
            
    return noisy_image


noise_intensity = 20  # Adjust the intensity of noise
noisy_image = add_noise(image, noise_intensity)
def draw_screen(content, screen_color, content_color):
    center = (screen.get_width() // 2, screen.get_height() // 2)

    screen.fill(screen_color)
    if isinstance(content, str):
        text = font.render(content, True, content_color)
        text_rect = text.get_rect(center=center)
        screen.blit(text, text_rect)
    else:
        rect = content.get_rect(center=center)
        screen.blit(content, rect)

    pygame.display.update()
    
draw_screen(noisy_image, (127,127,127), (256,256,256))