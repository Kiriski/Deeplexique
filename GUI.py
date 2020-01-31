from functools import partial
from PIL import Image, ImageTk
from PIL. Image import core as _imaging
import tkinter as tk
from SpeechToText import SpeechToText


class GUI():

    def __init__(self):
        pass


    def build(self):
        root = tk.Tk()
        root.title('DeepLexique')
        root.geometry("1280x720")
        root.configure(bg='#ccccff')

        # main frame #5ADC78
        # wallpaper = ImageTk.PhotoImage(file='Data/Image/wallpaper.jpg')
        # background_label = tk.Label(root, image=wallpaper)
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # mainframe = tk.Frame(root)
        # mainframe.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)
        text = tk.Text(root, height=30, width=80, padx=5, pady=5, wrap='word')

        text_test = """Le contenu que représentent les données, les modèles, les tests et les points de terminaison est organisée en projet sur le portail custom speech. Chaque projet est propre à un domaine et un pays langue. Par exemple, vous pouvez créer un projet pour des centres d'appels dont la langue est l'anglais des États-Unis, point pour créer votre premier projet sélectionné, speech to text ai custom speech, puis cliquez sur New Project. Suivez les instructions fournies par l'assistant pour créer votre projet. Une fois le projet créé, vous devez disposer de 4 onglets data, testing, training et diplômes ont. Utiliser les liens fournis dans l'étape suivante pour savoir comment utiliser chaque onglet."""

        text.insert('end', text_test, ('notread'))
        font = ('Comic Sans MS', 12, 'bold')
        text.configure(font=font)
        text.tag_configure('read', background='yellow', font=font)
        text.tag_configure('notread', font=font, background='White')

        stt = SpeechToText('0cf90ceec03c44a6942e8ae5066457ee', 'francecentral')

        buttonSTT = tk.Button(root, text='Lecture assistée', background='#4600FF', font=font,
                              command=partial(stt.speech_recognize_continuous_from_microphone, text.get('1.0', 'end'), text))
        buttonSTT.place(relx=0.805, rely=0.4, relwidth=0.1, relheight=0.03)

        button_stop = tk.Button(root, text='Stop lecture', background='#4600FF', font=font,
                                command=partial(stt.stop_recognizing))
        button_stop.place(relx=0.805, rely=0.44, relwidth=0.1, relheight=0.03)

        text.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.8)
        root.mainloop()

if __name__ == '__main__':
   gui= GUI()
   gui.build()