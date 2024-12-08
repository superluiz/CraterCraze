# -*- coding: utf-8 -*-
"""
Created on Sat Sep 4 21:22:20 2021
Refatorado para maior eficiência, robustez e clareza.
@author: Luiz Ahumada
"""
import csv
from math import radians, cos, sin, asin, sqrt
from pathlib import Path
import time

# Parâmetros iniciais
BASE_DIR = Path("C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/AllImages/csv_proc")
RESULT_FILE = BASE_DIR / "crateraSimilares.csv"
ANALYZED_FILE = BASE_DIR / "csvAnalisado.csv"
RAIO_MARTE = 3389500  # Raio de Marte em metros
MARGEM_ERRO = 5  # Percentual de margem de erro no diâmetro
timestart = time.time()

# Funções auxiliares
def check_point(message):
    """Exibe o tempo decorrido com uma mensagem."""
    elapsed = time.time() - timestart
    print(f"[{elapsed:.2f}s] {message}")

def haversine(lon1, lat1, lon2, lat2):
    """
    Calcula a distância esférica entre dois pontos (em metros) usando a fórmula de Haversine.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return c * RAIO_MARTE

def criar_csv_vazio():
    """Cria o arquivo CSV de saída vazio com o cabeçalho."""
    with RESULT_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["latitude", "longitude", "diametro", "unica"])
    check_point("Arquivo de saída criado.")

def ler_e_ordenar_csv():
    """Lê o arquivo CSV de crateras analisadas e ordena os dados pelo diâmetro."""
    with ANALYZED_FILE.open("r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Ignora o cabeçalho
        return sorted(reader, key=lambda row: float(row[2]))

def calcular_margem(raio):
    """Calcula a margem mínima e máxima para o raio de uma cratera."""
    margem = MARGEM_ERRO * raio / 100
    return raio - margem, raio + margem

# Classe para identificar crateras similares
class ComparadorCrateras:
    def __init__(self, cratera_a, cratera_b):
        self.lat_a = float(cratera_a[0])
        self.lon_a = float(cratera_a[1])
        self.diam_a = float(cratera_a[2])
        self.lat_b = float(cratera_b[0])
        self.lon_b = float(cratera_b[1])
        self.diam_b = float(cratera_b[2])
        self.distancia = haversine(self.lon_a, self.lat_a, self.lon_b, self.lat_b)

    def sao_similares(self):
        """
        Verifica se duas crateras são similares com base na distância e nos diâmetros.
        """
        min_diam, max_diam = calcular_margem(self.diam_a)
        if min_diam <= self.diam_b <= max_diam and self.distancia <= self.diam_a / 2:
            return True
        return False

def gravar_resultado(cratera, unica=True):
    """
    Grava a cratera no arquivo de saída, indicando se é única ou similar.
    """
    with RESULT_FILE.open("a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        linha = cratera + [1 if unica else 0]
        writer.writerow(linha)

def identificar_similares(lista_crateras):
    """
    Compara cada cratera com as próximas na lista para verificar similaridades.
    """
    total = len(lista_crateras)
    for i, cratera_a in enumerate(lista_crateras):
        unica = True
        for j in range(i + 1, total):
            cratera_b = lista_crateras[j]
            comparador = ComparadorCrateras(cratera_a, cratera_b)
            if comparador.sao_similares():
                unica = False
                break
        gravar_resultado(cratera_a, unica)
        check_point(f"Processada {i + 1}/{total}")

# Execução principal
def main():
    check_point("Início do processamento.")
    criar_csv_vazio()
    lista_crateras = ler_e_ordenar_csv()
    identificar_similares(lista_crateras)
    check_point("Processamento concluído.")

if __name__ == "__main__":
    main()
