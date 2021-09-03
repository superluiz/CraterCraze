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
''' Pametros inciais '''
mypath = '<path_your_dir>/AllImages/'
timestart = time.time()
''' Tamanho original da imagem '''
tamanhoImg = 7680
''' Escala original da imagem, em pixels '''
mpp = 463.1

'''
    Objeto que recebe e calcula as coordenadas e diametro da cratera
    conforme o nome do arquivo e a escala.
'''
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

''' Metodo incicial, quando executar este programa, cria um arquivo sem dados '''    
def novo_arquivo_csv():
    csv_dest = open(mypath+'csv_proc/csvAnalisado.csv', 'w', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow(['latitude','longitude','diametro'])
    csv_dest.close()
    
''' Metodo que le todos os arquvios csv e retorna um array '''
def ler_arquivos():
    return [f for f in listdir(mypath+'csv/') if isfile(join(mypath+'csv/', f))]

''' Metodo de controle de tempo demandado, apenas acompanhamento ''' 
def checkPoint(texto):    
    tempo = time.time() - timestart
    print('\t' + str(tempo)[0:5] + ' - '+texto)

''' Metodo que recebe um array contendo latitude, longitude e diametro
    Em metros e insere no arquivo csvAnalisado.csv.
    A cada chamada ele abre o arquivo e fecha, assim se der algum erro
    o trabalho nao estara totalmente perdido '''
def insere_processado(linha):
    csv_dest = open(mypath+'csv_proc/csvAnalisado.csv', 'a', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow(linha)
    csv_dest.close()

''' Metodo que atraves do nome do arquivo e o caminho onde está o csv
    analisado, ele cria o objeto RegiaoMarte e calcula tudo '''
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

''' ------------ INICIO ------------ '''
checkPoint('inicio')
novo_arquivo_csv()
onlyfiles = ler_arquivos()
for csvs in onlyfiles:      
    abre_analise_arquivo(csvs)    
checkPoint('Termino')    
