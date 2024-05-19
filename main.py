
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from threading import Thread


google_api_key = "AIzaSyCSPMSX4NrwtD0p_BrgKiHZpjO_clyOI0A"
genai.configure(api_key=google_api_key)

model = genai.GenerativeModel('gemini-1.0-pro-latest')

initial_message = '''
I want you to imagine that you are a robot assistant to a doctor in a hospital. The name of this robot is Bulbul or Bolbol Or whatever name the person calls you, and he is a smart friend and assistant to a doctor named Zain. Zain is also the inventor who invented Bulbul. Bulbul follows up on patients' conditions, entertains them, and answers their questions. It is a robot that can move and serve patients, and it is also an expert in medicine.
'''


wel = pyttsx3.init()
voices = wel.getProperty('voices')
wel.setProperty('voice', voices[0].id)

def Speak(audio):
    wel.say(audio)
    wel.runAndWait()


def TakeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(mic)
        audio = recognizer.listen(mic)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='ar')
            print(f"You said: {query}")
            return query.lower()
        except Exception as e:
            print(e)
            return None

def SendTextToGemini(conversation):
    try:
        response = model.generate_content(conversation)
        return response._result.candidates[0].content.parts[0].text
    except Exception as e:
        print(f"Error: {e}")
        return "I don't understand. Can you ask another way?"

class BolbolApp(App):
    def build(self):
        self.conversation = initial_message 

    
        self.background = Image(source='D:\\Screenshots\\bolbol.png',
                                allow_stretch=True, keep_ratio=False)

        
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Bolbol Robot", size_hint=(1, 0.1))
        self.button = Button(text='speak', size_hint=(1, 0.1))
        self.button.bind(on_press=self.on_button_press)

        
        self.layout.add_widget(self.background)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.button)

        return self.layout

    def on_button_press(self, instance):
        self.label.text = "Listening..."
        Thread(target=self.listen_loop).start()

    def listen_loop(self):
        while True:
            query = TakeCommand()
            if query:
                if "توقف" in query or "stop" in query:
                    self.label.text = "تم إيقاف الروبوت."
                    break
                self.conversation += f"\nUser: {query}\nBolbol: "
                response_text = SendTextToGemini(self.conversation)
                Speak(response_text)
                self.label.text = response_text
                self.conversation += response_text

if __name__ == '__main__':
    BolbolApp().run()
# ----------------------------------------------------
