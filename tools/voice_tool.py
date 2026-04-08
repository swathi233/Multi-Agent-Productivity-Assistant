def listen():
    try:
        import speech_recognition as sr

        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=5)

        return r.recognize_google(audio)

    except:
        return "Voice not available"