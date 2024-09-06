import nltk
import speech_recognition as sr
import streamlit as st
from nltk.chat.util import Chat, reflections

# Exemple de paires de questions-réponses pour le chatbot
pairs = [
    (r'Bonjour', 'Bonjour! Comment puis-je vous aider aujourd\'hui?'),
    (r'(.*) (nom|appelle) (.*)', 'Enchanté, {0}!'),
    (r'(.*) (heure|temps|date)', 'Je ne peux pas vous donner l\'heure ou la date, mais vous pouvez vérifier sur votre appareil.'),
    (r'(.*)', 'Je suis désolé, je ne comprends pas.')
]

# Créez une instance du chatbot
chatbot = Chat(pairs, reflections)

def transcrire_parole():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Parlez maintenant...")
        audio = recognizer.listen(source)
        try:
            texte = recognizer.recognize_google(audio, language='fr-FR')
            st.write(f"Vous avez dit : {texte}")
            return texte
        except sr.UnknownValueError:
            st.write("Je n'ai pas pu comprendre ce que vous avez dit.")
            return None
        except sr.RequestError:
            st.write("Erreur de demande au service de reconnaissance vocale.")
            return None

def repondre_au_chatbot(entrée):
    réponse = chatbot.respond(entrée)
    return réponse


def main():
    st.title("Chatbot à Commande Vocale")

    choix = st.radio("Choisissez le mode d'entrée :", ("Texte", "Voix"))

    if choix == "Texte":
        texte = st.text_input("Entrez votre message:")
        if st.button("Envoyer"):
            réponse = repondre_au_chatbot(texte)
            st.write(f"Chatbot: {réponse}")

    elif choix == "Voix":
        if st.button("Parlez maintenant"):
            texte = transcrire_parole()
            if texte:
                réponse = repondre_au_chatbot(texte)
                st.write(f"Chatbot: {réponse}")


if __name__ == "__main__":
    main()
