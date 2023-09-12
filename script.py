import gradio as gr
import modules.shared as shared
#import json
#from datetime import datetime
from pathlib import Path
import html
import time
import pyttsx4
#import pyttsx3
import ffmpeg
import os


#You'll need to install pyttsx4 and ffmpeg


myprompt="no data"

params = {
    "display_name": "SpeakLocal",
    "activate": True,
    "custom string": "n/a",
}

class _TTS:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx4.init()
        voices = self.engine.getProperty('voices') 
        self.engine.setProperty('voice', voices[1].id) # Set playback to the feminine voice


    def start(self,text_,wav_file_):
        self.engine.save_to_file(text_, wav_file_) 
        #self.engine.say(text_) # Used for local debugging
        self.engine.runAndWait()
        self.engine.stop()
        
def speak_text(string):
    original_string=string
    string=html.unescape(string)
    mydate=int(time.time())
    tmp_string=string.replace(" ","_")
    
    if not Path('extensions/SpeakLocal/output').exists():
        Path('extensions/SpeakLocal/output').mkdir()
    
    filename_length=16    
    wav_file = os.path.dirname(__file__)+f'/output/{tmp_string[:filename_length]}_{mydate}.wav'
    output_file = os.path.dirname(__file__)+f'/output/{tmp_string[:filename_length]}_{mydate}.mp3'
  
    # This class bit is because there's a bug in .runAndWait() 
    # that never returns control to a script
    # By using this class hack we can fire-and-forget and workaround the bug
    tts = _TTS()
    tts.start(string,wav_file)
    del(tts)
    
    # Convert the .wav to .mp3 | Safari doesn't support .ogg
    # Using a low audio bitrate so you don't use up all your mobile data!
    ffmpeg.input(wav_file).output(output_file, audio_bitrate='18k', loglevel="quiet" ).run()
    
    # A regular 'os.path' wont work with 'as_posix()', so use 'Path()'
    audio_file = Path(f'extensions/speak_text/output/{tmp_string[:filename_length]}_{mydate}.mp3')
    
    string = f'<audio src="file/{audio_file.as_posix()}" controls></audio>'
    string += f'\n\n{original_string}'
    
    # Cleanup / remove the now un-needed wav files
    if os.path.exists(wav_file):
        os.remove(wav_file)
    else:
        print(f"The {wav_file} file does not exist") 
    
    return string
    

    
    
def save_audio():
    pass
    

def input_modifier(string):
    """
    This function is applied to your text inputs before
    they are fed into the model.
    """ 
    global myprompt
    myprompt=string
    print (f"Prompt: {myprompt}")

    return string

def output_modifier(string):
    """
    This function is applied to the model outputs.
    """
    
    text_and_audio_data=speak_text(string)
    string=text_and_audio_data

    return string

def bot_prefix_modifier(string):
    """
    This function is only applied in chat mode. It modifies
    the prefix text for the Bot and can be used to bias its
    behavior.
    """

    # if params['activate'] == True:
    #     return f'{string} {params["custom string"].strip()} '
    # else:
    #     return string
    return string

def ui():
    # Gradio elements
    activate = gr.Checkbox(value=params['activate'], label='Activate SpeakText')
   
    # Event functions to update the parameters in the backend
    activate.change(lambda x: params.update({"activate": x}), activate, None)

