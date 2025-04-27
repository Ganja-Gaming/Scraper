import PySimpleGUI as sg
import subprocess
import sys
import os

def run_streamlit_app():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(application_path)

    python_executable = sys.executable
    subprocess.Popen([python_executable, "-m", "streamlit", "run", "app.py"], shell=True)

layout = [
    [sg.Text('LinkedPickle Pro Launcher', size=(30,1), justification='center', font=("Helvetica", 20))],
    [sg.Button('Launch LinkedPickle Pro', size=(30,2), button_color=('white', 'green'))],
    [sg.Button('Exit', size=(30,1), button_color=('white', 'firebrick3'))]
]

window = sg.Window('LinkedPickle Pro Launcher', layout, element_justification='c')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Launch LinkedPickle Pro':
        run_streamlit_app()

window.close()
