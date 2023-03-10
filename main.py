import speech_recognition as sr
import soundfile as sf
import json, time, pyttsx3
from datetime import datetime
from revChatGPT.ChatGPT import Chatbot
from colorama import Fore, Back, Style





# COLORS
CYAN = Fore.LIGHTCYAN_EX
YELLOW = Fore.LIGHTYELLOW_EX
GREEN = Fore.LIGHTGREEN_EX
RED = Fore.LIGHTRED_EX
WHITE = Fore.LIGHTWHITE_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
DARKRED = Fore.RED
RESET = Fore.RESET




# GENERAL SETTINGS
__LANGUAGE__ = 'en'
__NAME__ = 'chat'
__MULTI_ACCOUNT__ = True
__CURRENT_ACCOUNT__ = 0
__NO_VOICE__ = False
__AUDIO__ = True
__WORDS_PER_MINUTE__ = 150




#FUNCTIONS
def listen():
    """Listen to the microphone and return the audio as a string"""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print(f"{CYAN}[{WHITE}·{CYAN}] {MAGENTA}listening...{RESET}")
        audio = r.listen(source)

    try:
        #result2 line has been commented to avoid disturbing message
        print(f"{GREEN}[{WHITE}·{GREEN}]{MAGENTA} You said: {RESET}" + r.recognize_google(audio, language=__LANGUAGE__)) 
        return r.recognize_google(audio, language=__LANGUAGE__)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass


def log(sentence):
    """Save the log"""
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write(str(datetime.now()) +': '+ ' '.join(sentence) + '\n')


def customs(sentence):
    """custom sentences"""
    if sentence == '{} hola'.format(__NAME__):
        voice_process(f'Hola, soy {__NAME__}, tu asistente personal')
        return True
    
    if sentence == '{} vete a dormir'.format(__NAME__):
        voice_process('Voy a dormir')
        return 2

    if sentence == '{} dime la hora'.format(__NAME__):
        voice_process("Son las " + datetime.now().strftime('%H:%M:%S'))
        return True


def play_response(sentence):
    """Play the response"""
    engine = pyttsx3.init()
    engine.setProperty('rate', __WORDS_PER_MINUTE__)
    voices = engine.getProperty('voices')
    for voice in voices:
        if __LANGUAGE__ in voice.name:
            engine.setProperty('voice', voice.id)
            break
    engine.say(sentence)
    engine.runAndWait()


def voice_process(sentence):
    """Process the voice"""
    try:
        print(f"{GREEN}[{WHITE}·{GREEN}]{CYAN} Received sentence: {RESET}", sentence)
        
        if __AUDIO__:
            play_response(sentence)
            time.sleep(2) 
            
    except:
        print(f"{RED}[{WHITE}·{RED}] {DARKRED}An error ocurred during reproduction{RESET}")


def send_to(sentence):
    """Send the sentence to the api and process the response"""""
    try:
        response = chatbot.ask(' '.join(sentence))
        log(sentence)
        response = response['message']
        response2 = response.split(' ')
        
        if sentence[0].lower() == 'guarda' or sentence[0].lower() == 'save':
            code_save(response)

        log(response2)
        voice_process(response)
        
    except:
        login()
        

def pickextension(type):
    """Pick the extension of the file to save the code"""
    if type == 'json':
        return '.json'
    elif type == 'csv':
        return '.csv'
    elif type == 'txt':
        return '.txt'
    elif type == 'html':
        return '.html'
    elif type == 'md':
        return '.md'
    elif type == 'python':
        return '.py'
    elif type == 'javascript':
        return '.js'
    elif type == 'java':
        return '.java'
    elif type == 'c':
        return '.c'
    elif type == 'c++':
        return '.cpp'
    elif type == 'c#':
        return '.cs'
    elif type == 'php':
        return '.php'
    elif type == 'sql':
        return '.sql'
    elif type == 'xml':
        return '.xml'
    elif type == 'yaml':
        return '.yaml'
    elif type == 'yml':
        return '.yml'
    elif type == 'css':
        return '.css'
    elif type == 'scss':
        return '.scss'
    else :
        return '.txt'
    #Add more extensions here


def code_save(response):
    """Save the code in a file"""
    extension = pickextension(sentence[2].lower())
    start = response.index("```") + 4
    end = response.index("```", start)
    extracted_string = response[start:end]

    filename = "saves/" + str(datetime.now()).replace('-', '').replace(':', '').replace('.', '').replace(' ', '') + extension
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(extracted_string)
        print(f"{GREEN}[{WHITE}·{GREEN}]{CYAN} File saved: {RESET}", filename)


def login():
    """Login into chatgpt in order to get the token"""
    global chatbot
    global __CURRENT_ACCOUNT__
    
    try:
        config = json.load(open("config.json"))
        if __MULTI_ACCOUNT__:
            print (f"{CYAN}[{WHITE}·{CYAN}] {MAGENTA}Login in to account: {__CURRENT_ACCOUNT__}{RESET}")
            chatbot = Chatbot(config[__CURRENT_ACCOUNT__], conversation_id=None)
            __CURRENT_ACCOUNT__ = (__CURRENT_ACCOUNT__ + 1) % len(config)
        else:
            chatbot = Chatbot(config[0], conversation_id=None)
        
        return chatbot
    except:
        print(f"{RED}[{WHITE}·{RED}] {DARKRED}An error ocurred while login in{RESET}")
        return False


if __name__ == '__main__':
    """Runs the main program"""
    
    chatbot = False
    
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)

    while chatbot == False:
        chatbot = login()
        time.sleep(1)

    while(True):
        finalizar = False
        sentence = []
        
        if not __NO_VOICE__:
            sentence = listen()

        else:
            sentence = input(f"{CYAN}[{WHITE}·{CYAN}]{MAGENTA} Enter a sentence: {RESET}")
        
        if sentence != None:
            sentence = sentence.split(' ')
            if sentence[0].lower() == __NAME__.lower():
                sentence = sentence[1:]
                personalizada = customs(sentence)
                print(f"{GREEN}[{WHITE}·{GREEN}] {MAGENTA}I understood you{RESET}")
                
                if not personalizada:
                    send_to(sentence)

                if personalizada == 2:
                    finalizar = True
                    break
                    
            else:
                print(f"{GREEN}[{WHITE}·{GREEN}] {CYAN}Waiting for orders...{RESET}")
        
        if finalizar:
            break
