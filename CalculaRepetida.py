# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 21:22:20 2021

@author: Luiz
"""
import csv
import math as Math
from geopy import distance
from math import radians, cos, sin, asin, sqrt

import time
mars_radius = 3389500 # em metros
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
        #checkPoint(self.mostrarLog,'Distancia A e B: '+ str(self.retorno) + ' metros')
        #checkPoint(self.mostrarLog,'Raio cratera: '+ str(self.crateraA / 2) + ' metros')            
        if(float(self.retorno) < float(self.crateraA / 2)):                
            #checkPoint(True, 'crateras similares encontrada!')
            return True
        return False
    def analisaCrateras(self):
        self.margemCratera = float("%0.5f" % (margem_erro * self.crateraA / 100))
        self.minCratera = float("%0.5f" % (self.crateraA - self.margemCratera))
        self.maxCratera = float("%0.5f" % (self.crateraA + self.margemCratera))
        if(self.minCratera < self.crateraB) and (self.crateraB < self.maxCratera):
            #checkPoint(self.mostrarLog,'## Crateras de diametro semelhantes ##')
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
        # converte graus decimais em radianos
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])    
        # formula haversine  
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 3389500 #raio de Marte em metros
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
    writer.writerow(['latitude','longitude','diametro'])
    csv_dest.close()        

def insere_processado(linha, flag):
    writer = csv.writer(csv_dest, delimiter=';')
    writer.writerow([linha[0], linha[1], linha[2], flag])
    

def insere_processado2(cd):
    csv_dest = open(mypath+'csv_proc/'+fileName, 'a', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    if(cd.idB > 0):
        writer.writerow([cd.idA, cd.pontoA_lat, cd.pontoA_lng, cd.crateraA, cd.idB ])
    else:
        writer.writerow([cd.idA, cd.pontoA_lat, cd.pontoA_lng, cd.crateraA])
    csv_dest.close()
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
    
#pontoa = [0, 1, 18400.08944]
#pontob = [0, 0, 18401.08944]
#pontoa = [-37.89844, 14.98047, 1884.08944]
#pontob = [-73.51562, 14.8125,  1955.21202]
#cd = CalculaDistancia(pontoa, pontob)
#cd.analisaDistancia()
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
                    cd.printDados(x)
                    flag = False
                    x = y
            else:                
                break
        insere_processado(lista_ordenada[x], flag)
def grava_resultado():
    teste_lista = []
    checkPoint(True,str(len(final_lista)) + ' de 783860')
    checkPoint(True,str(len(teste_lista)) + ' de 783860')

    csv_dest = open(mypath+'csv_proc/'+fileName, 'a', encoding='UTF8', newline='')
    writer = csv.writer(csv_dest, delimiter=';')
    teste_lista = lista_ordenada
    for idpop in range(0, len(final_lista)):
        for idx in range(0, len(lista_ordenada)):
            if(final_lista[idpop] == lista_ordenada[idx]):
                teste_lista.pop(idx)
            
    for idx in teste_lista:
        writer.writerow(idx)
    checkPoint(True,str(len(lista_ordenada)) + '!!')
    csv_dest.close()    
        
checkPoint(True,'Inicio')
fileName = 'crateraSimilar14.csv'
novo_arquivo_csv()
lista_ordenada = ler_e_ordena()
csv_dest = open(mypath+'csv_proc/'+fileName, 'a', encoding='UTF8', newline='')
grava_similares()  
#grava_resultado()  
csv_dest.close()        
checkPoint(True,'Termino')
