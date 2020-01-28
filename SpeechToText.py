import azure.cognitiveservices.speech as speechsdk
import time
import pandas as pd
import re
import tkinter as tk

class SpeechToText():


    def __init__(self, subscription_key, service_region):
        self.subscription_key = subscription_key
        self.service_region = service_region


    def speech_recognize_continuous_from_file(self, filepath):
        """performs continuous speech recognition with input from an audio file"""
        # <SpeechContinuousRecognitionWithFile>
        speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.service_region,
                                               speech_recognition_language='fr-FR')
        audio_config = speechsdk.audio.AudioConfig(filename=filepath)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False

        def stop_cb(evt):
            """callback that stops continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True

        # Connect callbacks to the events fired by the speech recognizer
        speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

    def speech_recognize_continuous_from_microphone(self, text, text_gui):
        """performs continuous speech recognition with input from microphone"""

        speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.service_region,
                                               speech_recognition_language='fr-FR')
        #     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        audio_config = speechsdk.audio.AudioConfig(filename='data/audio1.wav')

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False
        df_recognizing = pd.DataFrame(clean_text(text).split(' '), columns=['words'])
        df_recognizing['read'] = False
        df_recognized = df_recognizing.copy()
        current_index = 0
        global_index = 0
        current_text = ""
        global_text = ""

        def stop_cb(evt):
            """callback that stops continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            nonlocal global_text
            speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True

        def recognizing_cb(evt):
            """callback for recognizing event : current sentence being said returned in the evt"""
            nonlocal current_text
            nonlocal df_recognizing
            nonlocal current_index
            nonlocal global_index
            current_text = evt.result.text
            print(current_text)
            # change the words said to 'read' in the df_recognizing
            # can't handle if 2 words are added at once
            print(" RECOGNIZING : current_text : " + current_text + " \nlast word : " +
                  clean_text(evt.result.text).split(' ')[-1]
                  + "\nword to find : " + str(df_recognizing.iloc[current_index, 0]))
            # test if the last word given in the event is the one we're looking for
            if clean_text(evt.result.text).split(' ')[-1] == df_recognizing.iloc[current_index, 0]:
                df_recognizing.iloc[current_index, 1] = True
                current_index += 1
            # check the last two words
            elif clean_text(evt.result.text).split(' ')[-2] == df_recognizing.iloc[current_index, 0]:
                df_recognizing.iloc[current_index, 1] = True
                current_index += 1
                if clean_text(evt.result.text).split(' ')[-1] == df_recognizing.iloc[current_index, 0]:
                    df_recognizing.iloc[current_index, 1] = True
                    current_index += 1

        def recognized_cb(evt):
            """callback for recognized event : full sentence returned in the evt
            """
            nonlocal global_text
            nonlocal df_recognized
            nonlocal current_index
            nonlocal global_index
            global_text = global_text + " " + evt.result.text
            print("RECOGNIZED : " + evt.result.text)
            # change the words said to 'read' in the df_recognized
            for word in clean_text(evt.result.text).split(' '):
                if word == df_recognized.iloc[global_index, 0]:
                    df_recognized.iloc[global_index, 1] = True
                    global_index += 1

        #         if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
        #             print('RECOGNIZED KEYWORD: {}'.format(evt))
        #         elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        #             print('RECOGNIZED: {}'.format(evt))
        #         elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        #             print('NOMATCH: {}'.format(evt))

        # Connect callbacks to the events fired by the speech recognizer
        #     speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognizing.connect(recognizing_cb)
        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.speech_end_detected.connect(lambda evt: print('SPEECH END DETECTED: {}'.format(evt)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition_async()
        while not done:
            time.sleep(0.5)

    def speech_recognize_continuous_from_microphone2(self, text, text_gui):
        """performs continuous speech recognition with input from microphone"""

        speech_config = speechsdk.SpeechConfig(subscription=self.subscription_key, region=self.service_region,
                                               speech_recognition_language='fr-FR')
        # audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        audio_config = speechsdk.audio.AudioConfig(filename='data/audio1.wav')

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        done = False
        df_recognizing = pd.DataFrame(text.split(' '), columns=['original'])
        df_recognizing['read'] = False
        df_recognizing['clean'] = df_recognizing['original'].apply(lambda x: clean_text((x)))
        df_recognized = df_recognizing.copy()
        current_index = 0
        global_index = 0
        char_index = 0
        current_text = ""
        global_text = ""

        def stop_cb(evt):
            """callback that stops continuous recognition upon receiving an event `evt`"""
            print('CLOSING on {}'.format(evt))
            nonlocal global_text
            speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True

        def recognizing_cb(evt):
            """callback for recognizing event : current sentence being said returned in the evt"""
            nonlocal current_text
            nonlocal df_recognizing
            nonlocal current_index
            nonlocal global_index
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

        def recognized_cb(evt):
            """callback for recognized event : full sentence returned in the evt
            """
            nonlocal global_text
            nonlocal df_recognized
            nonlocal current_index
            nonlocal global_index
            global_text = global_text + " " + evt.result.text
            # print("RECOGNIZED : " + evt.result.text)
            # change the words said to 'read' in the df_recognized
            for word in clean_text(evt.result.text).split(' '):
                if word == df_recognized.iloc[global_index, 0]:
                    df_recognized.iloc[global_index, 1] = True
                    global_index += 1

        #         if evt.result.reason == speechsdk.ResultReason.RecognizedKeyword:
        #             print('RECOGNIZED KEYWORD: {}'.format(evt))
        #         elif evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        #             print('RECOGNIZED: {}'.format(evt))
        #         elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        #             print('NOMATCH: {}'.format(evt))

        # Connect callbacks to the events fired by the speech recognizer
        #     speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
        speech_recognizer.recognizing.connect(recognizing_cb)
        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.speech_end_detected.connect(lambda evt: print('SPEECH END DETECTED: {}'.format(evt)))
        speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        # stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()
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