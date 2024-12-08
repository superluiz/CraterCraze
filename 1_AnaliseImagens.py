# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 2021
Refatorado para maior robustez, eficiência e clareza.
@author: Luiz Ahumada
"""
from pathlib import Path
from pycda import CDA, load_image
from PIL import Image
import csv
import time

# Parâmetros iniciais
BASE_DIR = Path("C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/AllImages")
RESIZED_DIR = BASE_DIR / "rsz"
CSV_DIR = BASE_DIR / "csv"
PLOT_DIR = BASE_DIR / "plot"
INFO_CSV = BASE_DIR / "informacoes.csv"
TAMANHO_IMG = 7680  # Tamanho original da imagem em pixels
MPP = 463.1  # Metros por pixel
ESCALAS = [3, 5, 20, 50, 80, 100]  # Escalas a serem processadas
timestart = time.time()

# Configuração da biblioteca CDA
cda = CDA()

# Criação de diretórios
for directory in [RESIZED_DIR, CSV_DIR, PLOT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Funções auxiliares
def check_point(message):
    """Exibe o tempo decorrido com uma mensagem."""
    elapsed = time.time() - timestart
    print(f"[{elapsed:.2f}s] {message}")

def ler_arquivos():
    """Lê todos os arquivos de imagem do diretório base."""
    return list(BASE_DIR.glob("*.png"))

def registrar_info(escala):
    """Grava informações de escala no arquivo 'informacoes.csv'."""
    with INFO_CSV.open("a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([escala, f"{escala * TAMANHO_IMG // 100}", round((100 / escala) * MPP)])

def redimensionar_imagem(img_path, escala):
    """Redimensiona uma imagem para uma escala percentual e salva no diretório 'rsz'."""
    imagem = Image.open(img_path)
    tam_em_escala = round(TAMANHO_IMG * escala / 100)
    nome_redimensionado = RESIZED_DIR / f"{img_path.stem}_E{escala:02d}.png"
    imagem.resize((tam_em_escala, tam_em_escala)).save(nome_redimensionado, optimize=True, quality=85)
    return nome_redimensionado

def pular_se_ja_existe(nome_base):
    """Verifica se o arquivo CSV correspondente já existe no diretório 'csv'."""
    return (CSV_DIR / f"{nome_base}.csv").exists()

def processar_imagem(img_path, escala):
    """Redimensiona, processa e gera relatórios para uma imagem."""
    nome_base = img_path.stem
    if escala < 100:
        nome_base += f"_E{escala:02d}"
    if pular_se_ja_existe(nome_base):
        check_point(f"Pulando {nome_base}.csv (já processado).")
        return

    try:
        resized_img = img_path
        escala_mpp = MPP
        if escala != 100:
            resized_img = redimensionar_imagem(img_path, escala)
            escala_mpp = (100 / escala) * MPP

        imagem = load_image(resized_img)
        predicao = cda.get_prediction(imagem)
        predicao.set_scale(escala_mpp)
        predicao.to_csv(CSV_DIR / f"{nome_base}.csv", likelihoods=False)
        predicao.show(threshold=0.5, include_ticks=True, save_plot=PLOT_DIR / f"{nome_base}.png")
        check_point(f"Processada: {nome_base}")
    except Exception as e:
        check_point(f"Erro ao processar {img_path.name} na escala {escala}%: {e}")

# Execução principal
def main():
    # Criação do arquivo de informações
    with INFO_CSV.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Escala (%)", "LarguraAltura (px)", "MetrosPorPixel"])

    check_point("Início do processamento.")
    imagens = ler_arquivos()
    for escala in ESCALAS:
        registrar_info(escala)
        for img_path in imagens:
            check_point(f"Processando {img_path.name} na escala {escala}%.")
            processar_imagem(img_path, escala)
    check_point("Processamento concluído.")

if __name__ == "__main__":
    main()
