import subprocess
import tkinter as tk
from tkinter import filedialog, Text, StringVar, OptionMenu
from pydub import AudioSegment

def dividir_audio(caminho_audio, duracao_segmento=30000):  # 30 segundos por segmento
    audio = AudioSegment.from_file(caminho_audio)
    segmentos = [audio[i:i + duracao_segmento] for i in range(0, len(audio), duracao_segmento)]
    return segmentos

def transcrever_audio():
    caminho_audio = filedialog.askopenfilename(
        title="Selecione o arquivo de áudio",
        filetypes=(("Arquivos de Áudio", "*.wav *.mp3 *.ogg *.mp4"), ("Todos os arquivos", "*.*"))
    )

    if caminho_audio:
        segmentos = dividir_audio(caminho_audio)
        
        transcricao_completa = ""
        
        for i, segmento in enumerate(segmentos):
            segmento_path = f"segmento_{i}.wav"
            segmento.export(segmento_path, format="wav")
            
            # Comando Whisper para o segmento
            comando = ["whisper", segmento_path, "--language", "Portuguese", "--model", "small", "--output_format", "txt"]
            
            # Executar o comando e capturar a saída
            resultado = subprocess.run(comando, capture_output=True, text=True)
            
            # Adicionar o resultado ao texto completo
            transcricao_completa += resultado.stdout
        
        # Salvar a transcrição completa em um arquivo
        with open("transcricao_completa.txt", "w") as f:
            f.write(transcricao_completa)
        
        # Exibir a transcrição na interface
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, transcricao_completa)

root = tk.Tk()
root.title("Transcrição de Áudio com Whisper")

text_area = Text(root, wrap='word', height=20, width=60)
text_area.pack()

btn_transcrever = tk.Button(root, text="Selecionar e Transcrever Áudio", command=transcrever_audio)
btn_transcrever.pack()

root.mainloop()
