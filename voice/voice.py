import pyttsx3

def change_voice(engine, voice_id):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)

def text_to_speech(text, voice_id=0):
    engine = pyttsx3.init()
    change_voice(engine, voice_id)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text = input("Введите текст для преобразования в голос: ")
    voice_id = int(input("Введите ID голоса (0 для мужского, 1 для женского): "))
    text_to_speech(text, voice_id)

