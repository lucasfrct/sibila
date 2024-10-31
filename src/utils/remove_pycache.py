import signal
import os
import shutil
import sys


def remove_pycache(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for d in dirs:
            if d == '__pycache__':
                shutil.rmtree(os.path.join(root, d))


# Caminho do diretório do seu projeto
# project_dir = './src'
# remove_pycache(project_dir)

def signal_handler(sig, frame):
    print("\nCtrl+C capturado! Limpando pastas __pycache__...")
    # Substitua 'my_project' pelo caminho do seu diretório de projeto
    remove_pycache('my_project')
    print("Pastas __pycache__ removidas. Saindo...")
    sys.exit(0)


def kill_terminal():
    # Registrando a função de tratamento de sinal para SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
