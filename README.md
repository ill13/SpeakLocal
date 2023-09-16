# SpeakLocal
![image](https://github.com/ill13/SpeakLocal/assets/10509740/1adac786-93ce-4b76-b8fa-0c36ad3f2e56)

A TTS [text-to-speech] extension for oobabooga text WebUI

- 100% offline
- No AI
- Low CPU
- Low network bandwidth usage
- No word limit

```silero_tts``` is great, but it seems to have a word limit, so I made **SpeakLocal**. 

- This extension uses *pyttsx4* for speech generation and *ffmpeg* for audio conversio.
- *Pyttsx4* uses the native TTS abilities of the host machine (Linux, MacOS, Windows) so you shouldn't need to install anything else for this to work.
- This extension re-encodes the locally generated .WAV file to an .MP3 and pre-pends a media player to the text output field.
  - The .MP3 encoding is set to ~18kbps compression so the output file is roughly 1 kilobyte for each second of audio. It's set low to conserve bandwidth when using mobile data. 


### How to use:

Fire up a command prompt | shell:

```cd PATH_TO_text-generation-webui/extensions```

Now clone this repo:

```git clone https://github.com/ill13/SpeakLocal```

You may have to do:

```pip install -r requirements```

...If *pytssx4* and *ffmpeg-python* are not installed.

Finally enable the extension in the *session* tab

![image](https://github.com/ill13/SpeakLocal/assets/10509740/f7f2844d-537d-426a-8110-0ce674e05d11)


### 2023-09-15

More audio options added.

- Voice selection: An enumerated list of TTS voices that are installed on the host.
- Speech rate: Speed up or slow down how fast the words are spoken
- Bitrate: Ability to adjust sound quality. Beware, higher bitrate means more data used!

![image](https://github.com/ill13/SpeakLocal/assets/10509740/11d9d652-7bdc-469f-a5a4-3e072e293338)
