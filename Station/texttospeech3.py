import pyttsx3

def getTextTOSpeech(speechText):
    engine = pyttsx3.init()
    engine.say(speechText)
    engine.setProperty('rate',100)  
    engine.runAndWait()

getTextTOSpeech("Mama ")