import azure.cognitiveservices.speech as speechsdk
import time
import pandas as pd
import re
import tkinter as tk

class SpeechToText():


    def __init__(self, subscription_key, service_region):
        self.subscription_key = subscription_key
        self.service_region = service_region
        self.speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.service_region,
                                               speech_recognition_language='fr-FR')
        self.speech_recognizer = speechsdk.SpeechRecognizer(self.speech_config)


    def speech_recognize_continuous_from_file(self, filepath):
        """performs continuous speech recognition with input from an audio file"""
        # <SpeechContinuousRecognitionWithFile>
        audio_config = speechsdk.audio.AudioConfig(filename=filepath)

        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        done = False

        def stop_cb(evt):
            """callback that stops continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            self.speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
        self.speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        self.speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        self.speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        self.speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        self.speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # stop continuous recognition on either session stopped or canceled events
        self.speech_recognizer.session_stopped.connect(stop_cb)
        self.speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        self.speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

    def stop_recognizing(self):
        print("STOP")
        self.speech_recognizer.stop_continuous_recognition()
        self.speech_recognizer.session_started.disconnect_all()
        self.speech_recognizer.recognized.disconnect_all()
        self.speech_recognizer.session_stopped.disconnect_all()
        self.speech_recognizer.canceled.disconnect_all()
        self.speech_recognizer.recognizing.disconnect_all()

    def speech_recognize_continuous_from_microphone(self, text, text_gui):
        """performs continuous speech recognition with input from microphone"""

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        # audio_config = speechsdk.audio.AudioConfig(filename='data/audio1.wav')

        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        df_recognizing = pd.DataFrame(text.split(' '), columns=['original'])
        df_recognizing['read'] = False
        df_recognizing['clean'] = df_recognizing['original'].apply(lambda x: clean_text((x)))
        current_index = 0
        char_index = 0

        def stop_cb(evt):
            """callback that stops continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            self.speech_recognizer.stop_continuous_recognition()


        def recognizing_cb(evt):
            """callback for recognizing event : current sentence being said returned in the evt"""
            nonlocal df_recognizing
            nonlocal current_index
            nonlocal char_index
            current_text = evt.result.text
            # print(current_text)
            # change the words said to 'read' in the df_recognizing

            # Debugging print
            # print(" RECOGNIZING : current_text : " + current_text + " \nlast word : " +
            #       clean_text(evt.result.text).split(' ')[-1]
            #       + "\nword to find : " + str(df_recognizing.iloc[current_index, 0]) +
            #       '\nchar index : ' + str(char_index))


            # test if the last word given in the event is the one we're looking for
            # print('this : ' + clean_text(evt.result.text).split(' ')[-1]  + '\nCompared to : '+ df_recognizing.iloc[current_index, 2])
            if clean_text(evt.result.text).split(' ')[-1] == df_recognizing.iloc[current_index, 2]:
                df_recognizing.iloc[current_index, 1] = True
                char_index += len(df_recognizing.iloc[current_index, 0]) + 1
                current_index += 1

            # check the last two words
            elif clean_text(evt.result.text).split(' ')[-2] == df_recognizing.iloc[current_index, 2]:
                df_recognizing.iloc[current_index, 1] = True
                char_index += len(df_recognizing.iloc[current_index, 0]) + 1
                current_index += 1

                if clean_text(evt.result.text).split(' ')[-1] == df_recognizing.iloc[current_index, 2]:
                    df_recognizing.iloc[current_index, 1] = True
                    char_index += len(df_recognizing.iloc[current_index, 0]) + 1
                    current_index += 1

            text_gui.tag_add('read', "1.0", f'1.0 + {char_index} c')
            # print('char index end : ' + str(char_index))

        # Connect callbacks to the events fired by the speech recognizer
        #     speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        self.speech_recognizer.recognizing.connect(recognizing_cb)
        # speech_recognizer.recognized.connect(recognized_cb)
        self.speech_recognizer.speech_end_detected.connect(lambda evt: print('SPEECH END DETECTED: {}'.format(evt)))
        self.speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        self.speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        self.speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # stop continuous recognition on either session stopped or canceled events
        self.speech_recognizer.session_stopped.connect(stop_cb)
        self.speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        self.speech_recognizer.start_continuous_recognition()
        # while not done:
        #     time.sleep(0.5)

def clean_text(text):
    '''
    Cleans the text deleeting punctuation
    INPUTS
    :param text: text to clean

    OUTPUTS
    :return: cleaned text
    '''
    text = re.sub('[.;,?:!§#\(\)"]+', ' ', text).replace('\\', ' ').strip()
    for i in range(5):
        text = text.replace('  ', ' ')
    return text.lower()