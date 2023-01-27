import speech_recognition as sr
import soundfile as sf
import pygame, colorama, json, os, time, gtts, playsound, subprocess
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
__IDIOMA__ = 'es-ES'
__NOMBRE__ = 'chat'
__AUDIO__ = True
__SPEED__ = 2
__MULTI_ACCOUNT__ = True
__CURRENT_ACCOUNT__ = 0



#FUNCTIONS
def escucha():
    """Escucha lo que va diciendo el usuario"""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print(f"{CYAN}[{WHITE}·{CYAN}] {MAGENTA}Escuchando...{RESET}")
        audio = r.listen(source)

    try:
        #He comentado la linea de result2 para que no se muestre el texto feo
        print(f"{GREEN}[{WHITE}·{GREEN}]{MAGENTA} Has dicho: {RESET}" + r.recognize_google(audio, language=__IDIOMA__)) 
        return r.recognize_google(audio, language=__IDIOMA__)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass


def log(frase):
    """Guarda en un archivo la hora y la frase que se ha dicho"""
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write(str(datetime.now()) +': '+ ' '.join(frase) + '\n')


def personalizadas(sentencia,):
    """Frases personalizadas"""
    if sentencia == '{} hola'.format(__NOMBRE__):
        voice_process(f'Hola, soy {__NOMBRE__}, tu asistente personal')
        return True
    
    if sentencia == '{} vete a dormir'.format(__NOMBRE__):
        voice_process('Voy a dormir')
        return 2

    if sentencia == '{} dime la hora'.format(__NOMBRE__):
        voice_process("Son las " + datetime.now().strftime('%H:%M:%S'))
        return True


def scale_speed(frase):
    """Escala la velocidad de la frase"""
    speed = int(__SPEED__)
    data, sr = sf.read("temp.mp3")
    data = data[::speed]
    sf.write("temp.mp3", data, sr)

def play_response():
    """Reproduce la frase"""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def voice_process(frase):
    """Procesa la frase"""
    try:
        if os.path.exists('temp.mp3'):
            os.remove('temp.mp3')
            time.sleep(0.5)
        
        print(f"{GREEN}[{WHITE}·{GREEN}]{CYAN} Ha llegado la frase: {RESET}", frase)
        tts = gtts.gTTS(frase, lang=__IDIOMA__).save('temp.mp3')
        time.sleep(2)

        if __AUDIO__:
            if __SPEED__ != 1: scale_speed(frase)
            play_response()   
    
    except:
        print(f"{RED}[{WHITE}·{RED}] {DARKRED}Ha ocurrido un error al reproducir la frase{RESET}")


def send_to(frase):
    """Envia la frase a la api de chat gpt"""""
    try:
        response = chatbot.ask(' '.join(frase))
        log(frase)
        response = response['message']
        response2 = response.split(' ')
        log(response2)
        voice_process(response)
        
    except:
        login()
        

def login():
    """Inicia sesión en la api de chat gpt"""
    global chatbot
    global __CURRENT_ACCOUNT__
    
    try:
        config = json.load(open("config.json"))
        if __MULTI_ACCOUNT__:
            print (f"{CYAN}[{WHITE}·{CYAN}] {MAGENTA}Iniciando sesión con la cuenta {__CURRENT_ACCOUNT__}{RESET}")
            chatbot = Chatbot(config[__CURRENT_ACCOUNT__], conversation_id=None)
            __CURRENT_ACCOUNT__ = (__CURRENT_ACCOUNT__ + 1) % len(config)
        else:
            chatbot = Chatbot(config[0], conversation_id=None)
        
        return chatbot
    except:
        print(f"{RED}[{WHITE}·{RED}] {DARKRED}Ha ocurrido un error al iniciar sesión{RESET}")
        return False


if __name__ == '__main__':
    """Inicia el programa"""
    
    chatbot = False
    
    while chatbot == False:
        chatbot = login()
        time.sleep(1)

    while(True):
        finalizar = False
        frase = []
        sentencia = escucha()
        
        if sentencia != None:
            frase = sentencia.split(' ')
            if frase[0].lower() == __NOMBRE__.lower():
                frase = frase[1:]
                personalizada = personalizadas(sentencia)
                print(f"{GREEN}[{WHITE}·{GREEN}] {MAGENTA}Te he entendido{RESET}")
                
                if not personalizada:
                    send_to(frase)

                if personalizada == 2:
                    finalizar = True
                    break
                    
            else:
                print(f"{GREEN}[{WHITE}·{GREEN}] {CYAN}Esperando ordenes hacia mi persona...{RESET}")
        
        if finalizar:
            break
