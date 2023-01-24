import speech_recognition as sr
import pygame
from datetime import datetime
from revChatGPT.ChatGPT import Chatbot
import os, time, gtts, subprocess
import colorama, json
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

# SETTINGS
__IDIOMA__ = 'es-ES'
__NOMBRE__ = 'chatgpt' #Name to activate the assistant
config = json.load(open("config.json")) #Configuration in order to use chatgpt
chatbot = Chatbot(config, conversation_id=None)


def escucha():
    """Escucha lo que va diciendo el usuario"""
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print(f"{CYAN}[{WHITE}·{CYAN}] {MAGENTA}Escuchando...{RESET}")
        audio = r.listen(source)

    try:
        print(f"{GREEN}[{WHITE}·{GREEN}]{MAGENTA} Has dicho: {RESET}" + r.recognize_google(audio, language=__IDIOMA__)) 
        return r.recognize_google(audio, language=__IDIOMA__)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        pass

def log(frase):
    """Guarda en un archivo la hora y la frase que se ha dicho"""
    with open('log.txt', 'a') as file:
        file.write(str(datetime.now()) + ' '+ ' '.join(frase) + '\n')

def personalizadas(sentencia, speed):
    """Frases personalizadas"""
    #Añade aqui una frase personalizada para que realice en tu equipo
    if sentencia == '{} hola'.format(__NOMBRE__):
        voice_process('Hola, soy tu asistente personal', speed)
        return True
    
    if sentencia == '{} vete a dormir'.format(__NOMBRE__):
        voice_process('Voy a dormir', speed)
        return 2


    if sentencia == '{} dime la hora'.format(__NOMBRE__):
        voice_process("Son las " + datetime.now().strftime('%H:%M:%S'), speed)
        return True



def voice_process(frase, speed=1):
    """Procesa la frase y la reproduce"""
    try:
        if os.path.exists('temp.mp3'):
            os.remove('temp.mp3')
            time.sleep(0.5)
        
        print(f"{GREEN}[{WHITE}·{GREEN}]{CYAN} Ha llegado la frase: {RESET}", frase)
        tts = gtts.gTTS(frase, lang=__IDIOMA__).save('temp.mp3')
        time.sleep(2)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("temp.mp3")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except:
        print(f"{RED}[{WHITE}·{RED}] {DARKRED}Ha ocurrido un error al reproducir la frase{RESET}")

def send_to(frase):
    """Envia la frase a la api de chat gpt"""""
    try:
        response = chatbot.ask(' '.join(frase))
        response = response['message']
        voice_process(response)
        log(frase)
        log(response)
        
    except:
        pass

    
if __name__ == '__main__':
    """Inicia el programa"""
    while(True):
        finalizar = False
        frase = []
        sentencia = escucha()
        speed = 3
        
        if sentencia != None:
            frase = sentencia.split(' ')
            

            if frase[0] == __NOMBRE__:
                frase = frase[1:]
                personalizada = personalizadas(sentencia, speed)
                print(f"{GREEN}[{WHITE}·{GREEN}] {MAGENTA}Te he entendido{RESET}")
                
                if not personalizada:
                    frase = frase[1:]
                    send_to(frase)
                    log(frase)

                if personalizada == 2:
                    finalizar = True
                    break
                    
            else:
                print(f"{GREEN}[{WHITE}·{GREEN}] {CYAN}Esperando ordenes hacia mi persona...{RESET}")
        
        if finalizar:
            break
