from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys
import nltk
nltk.download('omw-1.4')

recognizer = speech_recognition.Recognizer()
bot = tts.init()
bot.setProperty('rate', 170)

todo_list = ['Go edit', 'Clean room', 'Go study']


def create_note():
    global recognizer
    bot.say("What's your note going to be?")
    bot.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                bot.say("Choose a filename!")
                bot.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                bot.say(f"I sucessfully created the note {filename}")
                bot.runAndWait
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            bot.say("I did not understand you! Please try again!")
            bot.runAndWait()


def add_todo():
    global recognizer

    bot.say("What is your addition to the todo list?")
    bot.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True
                bot.say(f"I added {item} to the to do list!")
                bot.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            bot.say("I didn't quite get what you said. Could you please repeat?")
            bot.runAndWait()


def show_todos():

    bot.say("The items in your to do list are these")
    for item in todo_list:
        bot.say(item)
    bot.runAndWait


def hello():
    bot.say("Hello, what can I do for you, Victor?")
    bot.runAndWait()


def quit():
    bot.say("Bye bye!")
    bot.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todo": show_todos,
    "exit": quit
}


assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()
        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
