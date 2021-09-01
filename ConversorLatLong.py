# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 22:18:36 2021

@author: Luiz
"""
from PIL import ImageFile
from PIL import Image
from os import listdir
from os.path import isfile, join
import time
import csv

mypath = 'C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/AllImages/'
timestart = time.time()
tamanhoImg = 7680
mpp = 463.1

class RegiaoMarte:
    def __init__(self, nomearquivo):
        self.nomearquivo = nomearquivo[12:-4]
        self.nomeArray = self.nomearquivo.split('_')
        self.mpp = 0
        self.escala = 100
        self.latitude = 0
        self.longitude = 0
        self.getLat()
        self.getLon()
        self.getEscala()
        self.getMpp()
    def getLat(self):
        self.latitude = int(self.nomeArray[0])
    def getLon(self):
        self.longitude = int(self.nomeArray[1])
    def getEscala(self):
        if(len(self.nomeArray)>=3):
            self.escala = int(self.nomeArray[2].replace("E", ""))
    def getMpp(self):
        self.mpp = (100/self.escala) * mpp
    def getCalcCoord(self, inputCoord):
        self.tamPixel = round(tamanhoImg * self.escala / 100)
        return float("%0.5f" % (int(inputCoord) * 30 / self.tamPixel))
    def getLatCalc(self, inputCoord):
        return self.latitude + self.getCalcCoord(inputCoord)
    def getLonCalc(self, inputCoord):
        return self.longitude + self.getCalcCoord(inputCoord)    
    def getDiamCratera(self, diamPixel):
        return float("%0.5f" % (float(diamPixel) * self.mpp))

def ler_arquivos():
    return [f for f in listdir(mypath+'csv/') if isfile(join(mypath+'csv/', f))]
 
def checkPoint(texto):    
    tempo = time.time() - timestart
    print('\t' + str(tempo)[0:5] + ' - '+texto)

def insere_processado(linha):
    csv_dest = open(mypath+'csv_proc/csvAnalisado.csv', 'a', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow(linha)
    csv_dest.close()
    
def novo_arquivo_csv():
    csv_dest = open(mypath+'csv_proc/csvAnalisado.csv', 'w', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow(['latitude','longitude','diametro'])
    csv_dest.close()

def abre_analise_arquivo(nomearquivo):
    checkPoint(nomearquivo)
    rm = RegiaoMarte(nomearquivo)
    with open(mypath+'csv/'+nomearquivo, newline='') as csvfile:
     reader = csv.DictReader(csvfile, delimiter=',')
     for row in reader:
         linha = []
         linha.append(rm.getLatCalc(row['lat']) )
         linha.append(rm.getLonCalc(row['long']) )
         linha.append(rm.getDiamCratera(row['diameter']) )
         insere_processado(linha)

checkPoint('inicio')
novo_arquivo_csv()
onlyfiles = ler_arquivos()
for csvs in onlyfiles:      
    abre_analise_arquivo(csvs)
    
checkPoint('Termino')    