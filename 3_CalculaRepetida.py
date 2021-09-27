# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 21:22:20 2021

@author: Luiz Ahumada
"""
import csv
from math import radians, cos, sin, asin, sqrt
import time
mars_radius = 3389500 # raio de Marte em metros
margem_erro = 5 #%
timestart = time.time()
metrosporgrau = 59288.88888
mypath = 'C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/AllImages/'
lista_ordenada = []
final_lista = []
contaCrat = 0
class CalculaDistancia:
    def __init__(self, pontoA, pontoB):
        self.pontoA_lat = float(pontoA[0])
        self.pontoB_lat = float(pontoB[0])        
        self.pontoA_lng = float(pontoA[1])
        self.pontoB_lng = float(pontoB[1])
        self.crateraA = float(pontoA[2])
        self.crateraB = float(pontoB[2])
        self.resultado = 0
        self.mostrarLog = False
        self.minCratera = 0
        self.maxCratera = 0
        self.idPontoA = 0
        self.idPontoB = 0
    def setIds(self, idA, idB):
        self.idPontoA = idA
        self.idPontoB = idB
    def analisaDistancia(self):
        self.retorno = self.haversine(self.pontoA_lng, self.pontoA_lat,self.pontoB_lng, self.pontoB_lat )
        if(float(self.retorno) < float(self.crateraA / 2)):                
            return True
        return False
    def analisaCrateras(self):
        self.margemCratera = float("%0.5f" % (margem_erro * self.crateraA / 100))
        self.minCratera = float("%0.5f" % (self.crateraA - self.margemCratera))
        self.maxCratera = float("%0.5f" % (self.crateraA + self.margemCratera))
        if(self.minCratera < self.crateraB) and (self.crateraB < self.maxCratera):
            return self.analisaGraus()
        return False
    def analisaGraus(self):
        self.dtLat = abs(self.pontoA_lat - self.pontoB_lat)
        self.dtLng = abs(self.pontoA_lng - self.pontoB_lng)
        if(self.dtLat < 5 and self.dtLng < 5):
            return True
        return False
    def haversine(self,lon1, lat1, lon2, lat2):
        self.resultado = 0
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])    
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = mars_radius
        self.resultado = float("%0.5f" % (c * r))
        return self.resultado 
    def printDados(self, index):
        self.mensagem = 'Index: '+str(index)+ ' de 783860\n'
        self.mensagem = self.mensagem + '\tCratera: '+str(self.crateraA) +' ' +str(self.crateraB) + '\n'
        self.mensagem = self.mensagem + '\tDistancia: '+str(self.resultado) + '\n'
        self.mensagem = self.mensagem + '\tLat: '+str(self.pontoA_lat) +' ' +str(self.pontoB_lat) + '\n'
        self.mensagem = self.mensagem + '\tLng: '+str(self.pontoA_lng) +' ' +str(self.pontoB_lng) + '\n'
        checkPoint(True, self.mensagem)
        
        
''' Metodo incicial, quando executar este programa, cria um arquivo sem dados '''    
def novo_arquivo_csv():
    csv_dest = open(mypath+'csv_proc/'+fileName, 'w', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow(['latitude','longitude','diametro','unica'])
    csv_dest.close()        

def insere_processado(linha, flag, contaCrat):    
    if(flag == True):        
        writer = csv.writer(csv_dest, delimiter=';')
        writer.writerow(linha)
    else:
        checkPoint(True,'Out - '+str(linha))

def ler_e_ordena():
    with open (mypath+"csv_proc/csvAnalisado.csv", "r") as f:
        dados = csv.reader(f, delimiter=";")
        lista = list(dados)
        lista.pop(0)
        return sorted (lista, key = lambda dado: float(dado[2]), reverse = False)

''' Metodo de controle de tempo demandado, apenas acompanhamento ''' 
def checkPoint(mostrar,texto):
    if(mostrar):
        tempo = time.time() - timestart
        print('\t' + str(tempo)[0:5] + ' - '+str(texto))

''' Metodo que analisa cada cratera com a próxima na lista e verifica
se e a mesma cratera detectada (em outra imagem, por exemplo) '''
def grava_similares(): 
    flag = True
    checkPoint(True,'START: '+str(len(final_lista)) + ' de 783860')
    for x in range(0, len(lista_ordenada)):
        index = x+1
        flag = True
        if(index > len(lista_ordenada)):
            break
        for y in range(index, len(lista_ordenada)):
            cd = CalculaDistancia(lista_ordenada[x], lista_ordenada[y])
            if(cd.analisaCrateras()):
                if(cd.analisaDistancia()):
                    flag = False
                    x = y
            else:                
                break
        insere_processado(lista_ordenada[x], flag, contaCrat)

checkPoint(True,'Inicio')
fileName = 'crateraSimilares.csv'
novo_arquivo_csv()
lista_ordenada = ler_e_ordena()
csv_dest = open(mypath+'csv_proc/'+fileName, 'a', encoding='UTF8', newline='')
grava_similares()   
csv_dest.close()        
checkPoint(True,str(contaCrat)+' Termino '+fileName)
