# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 22:18:36 2021
Refatorado para maior clareza, eficiência e robustez.
@author: Luiz Ahumada
"""
from pathlib import Path
import csv
import time

# Parâmetros iniciais
BASE_DIR = Path("C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/AllImages")
CSV_PROC_DIR = BASE_DIR / "csv_proc"
ANALISE_CSV = CSV_PROC_DIR / "csvAnalisado.csv"
ORIGINAL_CSV_DIR = BASE_DIR / "csv"
TAMANHO_IMG = 7680  # pixels
MPP = 463.1  # metros por pixel
timestart = time.time()

# Criação de diretórios
CSV_PROC_DIR.mkdir(parents=True, exist_ok=True)

# Classe para calcular coordenadas e diâmetro das crateras
class RegiaoMarte:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.nome_array = nome_arquivo[12:-4].split("_")
        self.latitude = int(self.nome_array[0])
        self.longitude = int(self.nome_array[1])
        self.escala = int(self.nome_array[2].replace("E", "")) if len(self.nome_array) >= 3 else 100
        self.mpp = (100 / self.escala) * MPP
        self.tam_pixel = round(TAMANHO_IMG * self.escala / 100)

    def calcular_coordenada(self, input_coord):
        return round(int(input_coord) * 30 / self.tam_pixel, 5)

    def calcular_latitude(self, input_coord):
        return self.latitude + self.calcular_coordenada(input_coord)

    def calcular_longitude(self, input_coord):
        return self.longitude + self.calcular_coordenada(input_coord)

    def calcular_diametro(self, diam_pixel):
        return round(float(diam_pixel) * self.mpp, 5)

# Funções auxiliares
def check_point(message):
    """Exibe o tempo decorrido com uma mensagem."""
    elapsed = time.time() - timestart
    print(f"[{elapsed:.2f}s] {message}")

def criar_csv_vazio():
    """Cria um arquivo CSV vazio com o cabeçalho."""
    with ANALISE_CSV.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(["latitude", "longitude", "diametro"])
    check_point("Arquivo CSV criado.")

def ler_arquivos_csv():
    """Lê todos os arquivos CSV do diretório de origem."""
    return list(ORIGINAL_CSV_DIR.glob("*.csv"))

def processar_arquivo_csv(nome_arquivo):
    """Processa um arquivo CSV individual e grava os resultados no CSV final."""
    try:
        check_point(f"Processando: {nome_arquivo.name}")
        regiao = RegiaoMarte(nome_arquivo.name)
        with nome_arquivo.open(newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=",")
            for row in reader:
                latitude = regiao.calcular_latitude(row["lat"])
                longitude = regiao.calcular_longitude(row["long"])
                diametro = regiao.calcular_diametro(row["diameter"])
                linha = [latitude, longitude, diametro]
                insere_no_csv(linha)
    except Exception as e:
        check_point(f"Erro ao processar {nome_arquivo.name}: {e}")

def insere_no_csv(linha):
    """Insere uma linha de dados no arquivo CSV final."""
    with ANALISE_CSV.open("a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(linha)

# Execução principal
def main():
    criar_csv_vazio()
    arquivos_csv = ler_arquivos_csv()
    for arquivo_csv in arquivos_csv:
        processar_arquivo_csv(arquivo_csv)
    check_point("Processamento concluído.")

if __name__ == "__main__":
    main()
