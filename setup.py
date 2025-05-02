from setuptools import setup, find_packages

setup(
    name="snake-game",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame==2.5.2",
    ],
    entry_points={
        'console_scripts': [
            'snake-game=snake_game.main:main',
        ],
    },
) 