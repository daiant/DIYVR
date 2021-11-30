#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, json, sys
from pygame.locals import *
import serial
import pyautogui

# Constantes
WIDTH = 640
HEIGHT = 480
pyautogui.PAUSE = 0.001 
arduino = serial.Serial('/dev/ttyACM0')  # open serial port

# Clases
class Bola(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("hola.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [0.25, -0.25]
    def update(self, time, pala):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        if pygame.sprite.collide_rect(self, pala):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
            
class Pala(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("pala.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5
    def update(self, time, direction):
        if self.rect.top >= 0:
            if direction > 0:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if direction < 0:
                self.rect.centery += self.speed * time
        
# Funciones
def read_serial():
    data = arduino.readline()
    return data

def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except Exception as e: 
        raise SystemExit

    image = image.convert()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas de pygame")
    background_image = load_image('fondo_pong.png')
    bola = Bola()
    pala = Pala(30)
    clock = pygame.time.Clock()
    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        values = {"x": "0", "y": "0", "z": "0"}
        ant_values = values
        try:
            values = json.loads(read_serial().decode().strip())
        except:
            values = {"x": "0", "y": "0", "z": "0"}
        print(values)
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
        bola.update(time, pala)
        pala.update(time, int(float(values["x"])) - int(float(ant_values["x"])))
        screen.blit(background_image, (0,0))
        screen.blit(bola.image, bola.rect)
        screen.blit(pala.image, pala.rect)
        pygame.display.flip()
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
