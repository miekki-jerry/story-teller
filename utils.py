from elevenlabs import generate, save, voices
from elevenlabs import set_api_key
import os
import random
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

voices = voices()

female_voice_ids = [voice.name for voice in voices if 'gender' in voice.labels and voice.labels['gender'] == 'female']
female_voice_ids.remove('Nicole')

male_voice_ids = [voice.name for voice in voices if 'gender' in voice.labels and voice.labels['gender'] == 'male']
male_voice_ids.remove('Ethan')

def voice_selector(response):
    names_with_voices = []
    if 'Adam' in response:
        voice = random.choice(male_voice_ids)
        names_with_voices.append(('Adam', voice))
        male_voice_ids.remove(voice)  # optional, if you want unique voices for each male character
    if 'Lilly' in response:
        voice = random.choice(female_voice_ids)
        names_with_voices.append(('Lilly', voice))
        female_voice_ids.remove(voice)  # optional, if you want unique voices for each female character
    return names_with_voices


def text_to_list(text):
    dialogues = []
    lines = text.strip().split("\n")
    for line in lines:
        if ": " in line:
            character, dialogue = line.split(": ", 1)
            dialogue = dialogue.strip().strip('"')
            dialogues.append((character, dialogue))
        else:
            print(f"Skipping invalid line: {line}")
    return dialogues


def text_to_audio(text, names_list):
    generated_audio_chunks = []
    for character, dialogue in text:
        for name in names_list:
            if character == name[0]:
                print(f"Sending dialogue of {character} to Eleven Labs")
                audio = generate(
                    text=dialogue,
                    voice=name[1],
                    model='eleven_multilingual_v1',
                )
                print(f"Received audio for dialogue of {character}")
                generated_audio_chunks.append(audio)
                
    combined_audio = b''.join(generated_audio_chunks)
    combined_audio_path = "combined_audio.mp3"
    save(combined_audio, combined_audio_path)
    print("Combined audio saved!")

