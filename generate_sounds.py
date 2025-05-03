import pygame
import numpy as np
import os
import wave
from pathlib import Path

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2)

# Create audio directory if it doesn't exist
audio_dir = Path('audio')
audio_dir.mkdir(exist_ok=True)

def generate_sound(frequency, duration, volume=0.5, fade_out=0.1):
    """Generate a simple sine wave sound"""
    sample_rate = pygame.mixer.get_init()[0]
    n_samples = int(duration * sample_rate)
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    
    # Generate sine wave
    t = np.linspace(0, duration, n_samples)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    
    # Apply volume and convert to 16-bit
    sine_wave = (sine_wave * volume * 32767).astype(np.int16)
    
    # Apply to both channels
    buf[:, 0] = sine_wave
    buf[:, 1] = sine_wave
    
    # Create fade out
    if fade_out > 0:
        fade_samples = int(fade_out * sample_rate)
        fade = np.linspace(1, 0, fade_samples)
        buf[-fade_samples:, :] = (buf[-fade_samples:, :].T * fade).T
    
    return buf

def generate_soothing_music(duration=4.0, volume=0.3):
    """Generate soothing background music with multiple harmonious frequencies"""
    sample_rate = pygame.mixer.get_init()[0]
    n_samples = int(duration * sample_rate)
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    
    # Define a pentatonic scale (peaceful sounding)
    frequencies = [
        262,  # C4
        294,  # D4
        330,  # E4
        392,  # G4
        440,  # A4
    ]
    
    # Create a gentle pattern
    t = np.linspace(0, duration, n_samples)
    for i, freq in enumerate(frequencies):
        # Add each note with different timing and volume
        start_time = (i * duration) / len(frequencies)
        note_duration = duration / 2
        mask = (t >= start_time) & (t <= start_time + note_duration)
        
        # Create envelope for smooth transitions
        envelope = np.ones_like(t)
        attack = 0.1
        decay = 0.2
        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        
        # Apply attack and decay
        if i > 0:  # Skip attack for first note
            envelope[mask] *= np.minimum(1, np.linspace(0, 1, sum(mask)))
        envelope[mask] *= np.maximum(0, np.linspace(1, 0, sum(mask)))
        
        wave = np.sin(2 * np.pi * freq * t) * envelope * (volume * 0.5)  # Reduced volume for layering
        buf[:, 0] += (wave * 32767).astype(np.int16)
        buf[:, 1] += (wave * 32767).astype(np.int16)
    
    # Add a gentle bass note
    bass_freq = 131  # C3
    bass_wave = np.sin(2 * np.pi * bass_freq * t) * volume * 0.3
    buf[:, 0] += (bass_wave * 32767).astype(np.int16)
    buf[:, 1] += (bass_wave * 32767).astype(np.int16)
    
    return buf

def save_wav(data, filename, sample_rate=44100):
    """Save numpy array as WAV file"""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)  # stereo
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())

# Generate sounds
print("Generating game sounds...")

# Eat sound (quick high-pitched sound)
eat_data = generate_sound(880, 0.1, 0.5)  # A5 note
save_wav(eat_data, os.path.join(audio_dir, 'eat.wav'))

# Power-up sound (ascending tone)
powerup_data = generate_sound(660, 0.2, 0.6)  # E5 note
save_wav(powerup_data, os.path.join(audio_dir, 'powerup.wav'))

# Game over sound (descending tone)
game_over_data = generate_sound(220, 0.3, 0.7)  # A3 note
save_wav(game_over_data, os.path.join(audio_dir, 'game_over.wav'))

# Generate soothing background music
print("Generating soothing background music...")
background_data = generate_soothing_music(duration=4.0, volume=0.3)
save_wav(background_data, os.path.join(audio_dir, 'background.wav'))

print("All sounds generated! You can now run the game with sound effects.") 