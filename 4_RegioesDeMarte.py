# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 23:29:03 2021

@author: Luiz Ahumada
"""
import csv
import time
timestart = time.time()
mypath = 'C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/'
lista_ordenada = []
fileName = 'resultadoCrateraMOLA.csv'

def ler_RegioesMarte():
    with open (mypath+"RegioesMarte.csv", "r") as f:
        dados = csv.reader(f, delimiter=";")
        lista = list(dados)
        lista.pop(0)
        return lista

def ler_crateraSimilar_ordena():
    with open (mypath+"AllImages/csv_proc/crateraSimilar.csv", "r") as f:
        dados = csv.reader(f, delimiter=";")
        lista = list(dados)
        lista.pop(0)
        return sorted (lista, key = lambda dado: (dado[3]), reverse = False)

''' Metodo incicial, quando executar este programa, cria um arquivo sem dados '''    
def novo_arquivo_csv():
    csv_dest = open(mypath+fileName, 'w', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow(['ID','Regiao','latitude','longitude','diametro'])
    csv_dest.close()        

''' grava informacao da cratera com a Regiao no arquivo '''
def insere_processado(cratera, regiao):
    csv_dest = open(mypath+fileName, 'a', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow([regiao[0], regiao[1],cratera[0], cratera[1], cratera[2]])
    csv_dest.close()
    
''' Metodo para comparar a latitude e longitude com as regioes de Marte '''
def categoriza_crateras_regiao():
    listaRegioes = ler_RegioesMarte()
    listaCrateras = ler_crateraSimilar_ordena()
    achouRegiao = False
    for cratera in listaCrateras:
        achouRegiao = False
        for regiao in listaRegioes:                
            if(float(regiao[2]) < float(cratera[0]) and float(regiao[3]) >= float(cratera[0]) and
                float(regiao[4]) < float(cratera[1]) and float(regiao[5]) >= float(cratera[1])):
                insere_processado(cratera, regiao)                    
                achouRegiao = True
        if(achouRegiao == False):
            insere_processado(cratera, ['---','Regiao nao encontrada'])

''' Metodo de controle de tempo demandado, apenas acompanhamento ''' 
def checkPoint(mostrar,texto):
    if(mostrar):
        tempo = time.time() - timestart
        print('\t' + str(tempo)[0:5] + ' - '+str(texto))
            
checkPoint(True,'Inicio')         
novo_arquivo_csv()
categoriza_crateras_regiao()
checkPoint(True,'Final')