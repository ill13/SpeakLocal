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
import re


#You'll need to install pyttsx4 and ffmpeg


myprompt="no data"
host_voices=[]
selected_voice=0

params = {
    "name": "SpeakLocal",
    "display_name": "SpeakLocal",
    "activate": True,
    'autoplay': True,
    "audio_bitrate": "18k",
}



class _TTS:

    global host_voices
    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx4.init()
        voices = self.engine.getProperty('voices') 
        self.engine.setProperty('voice', voices[selected_voice].id) # Set playback to the new selected voice
        # self.engine.setProperty('voice', voices[0].id) # Set playback to the default voice
        # self.engine.setProperty('voice', voices[1].id) # Set playback to the feminine voice
        # self.engine.setProperty('voice', voices[2].id) # Set playback to a freshly installed [french] voice

    def get_voices(self):
        voices = self.engine.getProperty('voices') 
        for voice in voices:
            print(voice.name)
            host_voices.append(voice.name)

    def start(self,text_,wav_file_):
        self.engine.save_to_file(text_, wav_file_) 
        #self.engine.say(text_) # Used for local debugging
        self.engine.runAndWait()
        self.engine.stop()
        
def speak_text(string):
    original_string=string
    string=html.unescape(string)
    # first try to remove special characters for issue #2
    string = re.sub('[^A-z0-9 -]', '', string).title()
    mydate=int(time.time())
    tmp_string=string.replace(" ","_")
    
    if not Path(f'extensions/{params["name"]}/output').exists():
        Path(f'extensions/{params["name"]}/output').mkdir()
    
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
    ffmpeg.input(wav_file).output(output_file, audio_bitrate=params["audio_bitrate"], loglevel="quiet" ).run()
    
    # A regular 'os.path' wont work with 'as_posix()', so use 'Path()'
    audio_file = Path(f'extensions/{params["name"]}/output/{tmp_string[:filename_length]}_{mydate}.mp3')
    
    string = f'<audio src="file/{audio_file.as_posix()}" controls></audio>'
    string += f'\n\n{original_string}'
    
    # Cleanup / remove the now un-needed wav files
    if os.path.exists(wav_file):
        os.remove(wav_file)
    else:
        print(f"The {wav_file} file does not exist") 
    
    return string
    

# def update_voice_list():
#     tts = _TTS()
#     tts.get_voices()
#     del(tts)
   
    
    

def setup():
    """
    Gets executed only once, when the extension is imported.
    """    
    tts = _TTS()
    tts.get_voices()
    del(tts)
    
def history_modifier(history):
    # Remove autoplay from the last reply
    if len(history['internal']) > 0:
        history['visible'][-1] = [
            history['visible'][-1][0],
            history['visible'][-1][1].replace('controls autoplay>', 'controls>')
        ]

    return history

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
    
    if not params['activate']:
        return string
    
    text_and_audio_data=speak_text(string)
    string=text_and_audio_data

    return string

def select_voice(option):
    index=host_voices.index(option)
    print(option)
    print(index)
    global selected_voice
    selected_voice=index

def ui():
    with gr.Accordion("SpeakLocal"):
        
        activate = gr.Checkbox(value=params['activate'], label='Activate SpeakLocal')
        #get_voices = gr.Button("Update installed voices")
        cb_voices=gr.Radio([hv for hv in host_voices],label="Voices")
            
   
   
    # Event functions to update the parameters in the backend
    activate.change(lambda x: params.update({"activate": x}), activate, None)
    cb_voices.change(fn=select_voice,inputs=cb_voices)
    #get_voices.click(update_voice_list)

