"""
Particle system for visual effects
"""
import random
import math
import pygame
from ..constants import (
    PARTICLE_COLORS, PARTICLE_LIFETIME,
    PARTICLE_SPEED, PARTICLE_COUNT
)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(PARTICLE_COLORS)
        self.lifetime = PARTICLE_LIFETIME
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, PARTICLE_SPEED)
        self.size = random.randint(2, 4)
        self.created_at = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.created_at
        if elapsed > self.lifetime:
            return False
        
        # Move particle
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Fade out
        alpha = int(255 * (1 - elapsed / self.lifetime))
        self.color = (*self.color[:3], alpha)
        
        return True

    def render(self, surface):
        if self.color[3] > 0:  # Check alpha value
            pygame.draw.circle(surface, self.color[:3], (int(self.x), int(self.y)), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particles(self, x, y, count=PARTICLE_COUNT):
        for _ in range(count):
            self.particles.append(Particle(x, y))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def render(self, surface):
        for particle in self.particles:
            particle.render(surface) 