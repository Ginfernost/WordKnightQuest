# Word Knight Quest

A small English vocabulary game for elementary school kids, set in a medieval castle. I built it in 2024 with Python and Pygame. It was my first game.

![Title screen](Menu.jpg)

## How it's built

Each stage practises the same words in a different way: spelling them, unscrambling them, using them in a sentence, matching them with words that mean the same, and finally saying them out loud. The last stage only lets you move on once you've actually said the word.

## The five stages

| Stage | What you do |
|---|---|
| 1. Hidden words | Pick up scattered letter blocks and drop them into the right slots to spell the word. A short clue tells you what it means. |
| 2. Scrambled scrolls | Unscramble a jumbled word and type it in. You get 30 seconds and a limited number of hints. |
| 3. The library | Fill the gap in a sentence by choosing the right word. 30 seconds per question. |
| 4. Memory match | Flip tiles to match words with their synonyms (happy / joyful, big / large) before time runs out. |
| 5. Say it | A word appears and you say it into the microphone. Speech recognition checks it before you can go on. |

The words live in plain text files (`wordlist1.txt` to `wordlist5.txt`), so a teacher can swap in their own list without touching the code.

## Running it

You need Python 3 and a microphone for stage 5.

```bash
pip install pygame SpeechRecognition sounddevice pyaudio
python menu.py
```

Notes:

- The game opens in full screen. Use the in-game Quit button to leave.
- Stage 5 sends your recording to Google's free speech recognition service, so it needs an internet connection.
- I built and tested it on Windows. On macOS or Linux, rename `Menu.jpg` to `menu.jpg` first, because those systems care about capital letters in file names.

## Built with

Python, Pygame, SpeechRecognition, sounddevice

## About me

I'm Nicholas Hendryson (楊國立). I teach, translate, and build AI tools for migrant workers in Taipei. More of my work is at [nicholashendryson.netlify.app](https://nicholashendryson.netlify.app).
