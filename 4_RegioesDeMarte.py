# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 23:29:03 2021
Refatorado para eficiência, legibilidade e robustez.
@author: Luiz Ahumada
"""
import csv
from pathlib import Path
import time

# Parâmetros iniciais
BASE_DIR = Path("C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte")
INPUT_FILE = BASE_DIR / "AllImages/csv_proc/crateraSimilar.csv"
REGIOES_FILE = BASE_DIR / "RegioesMarte.csv"
OUTPUT_FILE = BASE_DIR / "resultadoCrateraMOLA.csv"
timestart = time.time()

# Funções auxiliares
def check_point(message):
    """Exibe o tempo decorrido com uma mensagem."""
    elapsed = time.time() - timestart
    print(f"[{elapsed:.2f}s] {message}")

def criar_csv_vazio():
    """Cria o arquivo CSV de saída vazio com o cabeçalho."""
    with OUTPUT_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["ID", "Regiao", "latitude", "longitude", "diametro"])
    check_point("Arquivo de saída criado.")

def ler_csv(filepath, expected_columns=None):
    """
    Lê um arquivo CSV e retorna os dados como uma lista de listas.
    Valida se contém as colunas esperadas, se especificado.
    """
    try:
        with filepath.open("r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            header = next(reader)
            if expected_columns and not all(col in header for col in expected_columns):
                raise ValueError(f"Colunas esperadas: {expected_columns}, mas encontradas: {header}")
            return [row for row in reader]
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao ler {filepath}: {e}")

def gravar_no_csv(cratera, regiao):
    """Grava a cratera e sua região correspondente no arquivo de saída."""
    with OUTPUT_FILE.open("a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow([regiao[0], regiao[1], cratera[0], cratera[1], cratera[2]])

def associar_crateras_a_regioes(crateras, regioes):
    """
    Associa cada cratera à sua região correspondente.
    Se não encontrar uma região, registra como "Região não encontrada".
    """
    check_point("Iniciando associação de crateras às regiões.")
    for cratera in crateras:
        latitude = float(cratera[0])
        longitude = float(cratera[1])
        regiao_encontrada = None

        # Verifica se a cratera está dentro dos limites de alguma região
        for regiao in regioes:
            lat_min, lat_max = float(regiao[2]), float(regiao[3])
            lon_min, lon_max = float(regiao[4]), float(regiao[5])
            if lat_min <= latitude <= lat_max and lon_min <= longitude <= lon_max:
                regiao_encontrada = regiao
                break

        if regiao_encontrada:
            gravar_no_csv(cratera, regiao_encontrada)
        else:
            gravar_no_csv(cratera, ["---", "Região não encontrada"])
    check_point("Associação concluída.")

# Execução principal
def main():
    check_point("Início do processamento.")
    
    # Cria o arquivo de saída vazio
    criar_csv_vazio()

    # Lê os arquivos de entrada
    regioes = ler_csv(REGIOES_FILE, expected_columns=["ID", "Regiao", "LatMin", "LatMax", "LonMin", "LonMax"])
    crateras = ler_csv(INPUT_FILE, expected_columns=["latitude", "longitude", "diametro"])

    # Processa as crateras e associa às regiões
    associar_crateras_a_regioes(crateras, regioes)

    check_point("Processamento concluído.")

if __name__ == "__main__":
    main()
