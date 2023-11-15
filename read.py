import PyPDF2
import pyttsx3

book = open("AI-intr.pdf", "rb")
reader = PyPDF2.PdfReader(book)
pages = len(reader.pages)
print (pages)

audio = pyttsx3.init()
for num in range (0, pages):
    page = reader.pages[3]
    text = page.extract_text()
    audio.say (text)
    audio.runAndWait()