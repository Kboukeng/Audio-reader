import PyPDF2
import pyttsx3
import PySimpleGUI as sg
import io

def choose_pdf_file():
    layout = [
        [sg.Text('Select a PDF file:')],
        [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse()],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]

    window = sg.Window('Choose PDF File', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return None
        elif event == 'OK':
            file_path = values['-FILE-']
            window.close()
            return file_path

def read_pdf(file_path):
    book = open(file_path, "rb")
    reader = PyPDF2.PdfReader(book)
    pages = len(reader.pages)

    current_page = 0
    playing = False

    def play_current_page():
        nonlocal current_page
        if current_page < pages:
            page = reader.pages[current_page]
            text = page.extract_text()
            engine.say(text)
            engine.runAndWait()

    def play():
        nonlocal playing
        if not playing:
            playing = True
            play_current_page()

    def pause():
        nonlocal playing
        if playing:
            playing = False
            engine.stop()

    def stop():
        nonlocal playing
        if playing:
            playing = False
            engine.stop()
        current_page = 0
        window['-PAGE-'].update(f"Page {current_page + 1}/{pages}")

    def next_page():
        nonlocal current_page
        if current_page < pages - 1:
            current_page += 1
            play_current_page()
            window['-PAGE-'].update(f"Page {current_page + 1}/{pages}")

    def previous_page():
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            play_current_page()
            window['-PAGE-'].update(f"Page {current_page + 1}/{pages}")

    layout = [
        [sg.Text(f"Page {current_page + 1}/{pages}", key='-PAGE-')],
        [sg.Button('Previous', key='-PREVIOUS-'), sg.Button('Play', key='-PLAY-'), sg.Button('Pause', key='-PAUSE-'),
         sg.Button('Stop', key='-STOP-'), sg.Button('Next', key='-NEXT-')]
    ]

    window = sg.Window('PDF Reader', layout)
    

    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-PLAY-':
            play()
        elif event == '-PAUSE-':
            pause() 
        elif event == '-STOP-':
            stop()
        elif event == '-NEXT-':
            next_page()
        elif event == '-PREVIOUS-':
            previous_page()

    window.close()

# Main code
file_path = choose_pdf_file()
if file_path is not None:
    engine = pyttsx3.init()
    read_pdf(file_path)