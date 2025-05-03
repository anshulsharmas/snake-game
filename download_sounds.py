import os
import requests
from pathlib import Path

# Create audio directory if it doesn't exist
audio_dir = Path('audio')
audio_dir.mkdir(exist_ok=True)

# Sound URLs (free sound effects from different sources)
sound_urls = {
    'background.mp3': 'https://github.com/anshul/snake/raw/main/audio/background.mp3',
    'eat.wav': 'https://github.com/anshul/snake/raw/main/audio/eat.wav',
    'powerup.wav': 'https://github.com/anshul/snake/raw/main/audio/powerup.wav',
    'game_over.wav': 'https://github.com/anshul/snake/raw/main/audio/game_over.wav'
}

def download_sound(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(audio_dir / filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

print("Downloading game sounds...")
for filename, url in sound_urls.items():
    if not (audio_dir / filename).exists():
        download_sound(url, filename)
    else:
        print(f"{filename} already exists, skipping...")

print("\nAll sounds downloaded! You can now run the game with sound effects.") 