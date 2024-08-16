import subprocess
import tkinter as tk
from tkinter import filedialog, Text, StringVar, OptionMenu
from pydub import AudioSegment
import os

def dividir_audio(caminho_audio, duracao_segmento=30000):
    audio = AudioSegment.from_file(caminho_audio)
    segmentos = [audio[i:i + duracao_segmento] for i in range(0, len(audio), duracao_segmento)]
    return segmentos

def transcrever_audio():
    caminho_audio = filedialog.askopenfilename(
        title="Selecione o arquivo de áudio",
        filetypes=(("Arquivos de Áudio", "*.wav *.mp3 *.ogg *.mp4"), ("Todos os arquivos", "*.*"))
    )

    if caminho_audio:
        # Criar uma nova pasta para os arquivos
        nome_pasta = os.path.splitext(os.path.basename(caminho_audio))[0] + "_transcricao"
        if not os.path.exists(nome_pasta):
            os.makedirs(nome_pasta)

        segmentos = dividir_audio(caminho_audio)
        
        # Inicia o arquivo de transcrição
        transcricao_completa_path = os.path.join(nome_pasta, "transcricao_completa.txt")
        with open(transcricao_completa_path, "w") as f:
            f.write("")

        for i, segmento in enumerate(segmentos):
            segmento_path = os.path.join(nome_pasta, f"segmento_{i}.wav")
            segmento.export(segmento_path, format="wav")
            
            # Comando Whisper para o segmento
            comando = ["path/venv/bin/python", "-m", "whisper", segmento_path, "--language", "Portuguese", "--model", "small", "--output_format", "txt", "--output_dir", nome_pasta]
            
            # Executar o comando
            subprocess.run(comando)
            
            # Ler o conteúdo do arquivo gerado pelo Whisper e adicionar ao arquivo de transcrição completa
            segmento_txt_path = os.path.join(nome_pasta, f"segmento_{i}.txt")
            if os.path.exists(segmento_txt_path):
                with open(segmento_txt_path, "r") as seg_txt_file:
                    transcricao_segmento = seg_txt_file.read()
                    with open(transcricao_completa_path, "a") as f:
                        f.write(transcricao_segmento)
                
                # Remover o arquivo de texto do segmento
                os.remove(segmento_txt_path)
            
            # Remover o arquivo de áudio do segmento
            os.remove(segmento_path)
        
        # Atualizar a interface com a transcrição completa
        with open(transcricao_completa_path, "r") as f:
            transcricao_completa = f.read()
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, transcricao_completa)

root = tk.Tk()
root.title("Transcrição de Áudio com Whisper")

output_format = StringVar(root)
output_format.set("txt")  # Formato padrão

format_menu = OptionMenu(root, output_format, "txt", "srt", "vtt", "json")
format_menu.pack()

text_area = Text(root, wrap='word', height=20, width=60)
text_area.pack()

btn_transcrever = tk.Button(root, text="Selecionar e Transcrever Áudio", command=transcrever_audio)
btn_transcrever.pack()

root.mainloop()
