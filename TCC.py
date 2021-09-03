# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 2021

@author: Luiz
"""
from pycda import CDA, load_image
from PIL import ImageFile
from PIL import Image
from os import listdir
from os.path import isfile, join
import time
''' Pametros inciais '''
ImageFile.LOAD_TRUNCATED_IMAGES = True
cda = CDA()
mypath = 'C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/AllImages/'
timestart = time.time()
tamanhoImg = 7680
mpp = 463.1

''' Metodo de controle de tempo demandado, apenas acompanhamento ''' 
def checkPoint(texto):    
    tempo = time.time() - timestart
    print('\t' + str(tempo)[0:5] + ' - '+texto)

''' Metodo que le todos os arquivos (imagens originais) do diretorio
    /AllImages e cria um relatorio chamado informacoes.csv contendo
    dados de metros por pixel usados nas escalas'''
def ler_arquivos():
    infoExtras = open("informacoes.csv", "w")
    infoExtras.write("\nEscala;LaguraAltura;MetrosPorPixel\n")
    infoExtras.close()
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]

''' Metodo que grava quando uma escala nova entrou na lista de conversao'''
def info_extra(escala):
    infoExtras = open("informacoes.csv", "a")    
    infoExtras.write(str(escala) 
    + ';' + str(round(escala*tamanhoImg/100)) 
    + ';' + str(round((100/escala)*mpp)) + '\n')
    infoExtras.close()
    
''' Metodo principal onde ira ler as imagens (no tamanho
    correspondete a escala informada) e contara as crateras 
    gerando um csv salvo no diretorio correspondente '''    
def contar_cratera(img,escala):
    if(escala <100):        
        if(escala<10):
            img2 = img[0:-4] + '_E0' + str(escala) + '.csv'
        else:
            img2 = img[0:-4] + '_E' + str(escala) + '.csv'
    else:
        img2 = img
    if(False == pular_se_ja_existe(img2)):    
        try:
            resized = ''
            local_mpp = mpp
            if(escala != 100):
                img = redimensionar_imagem(img, escala)
                local_mpp = (100/escala) * mpp      
                resized = 'rsz/'
            nomeSemExtensao = img[0:-4]
            imagem = load_image(mypath + resized + img)        
            pred_img_orig = cda.get_prediction(imagem)    
            pred_img_orig.set_scale(local_mpp)        
            pred_img_orig.to_csv(mypath +'csv/'+ nomeSemExtensao+'.csv', likelihoods=False)
            pred_img_orig.show(threshold=0.5, include_ticks=True, save_plot=mypath+'plot/'+img)
        except Exception as e:
            checkPoint('erro na imagem: ' + img)
            checkPoint('\t' + str(e))
            
''' Metodo para redimensionar a imagem confome a escala em % e
    salvar em outro diretório '''    
def redimensionar_imagem(img, escala):    
    imagem = Image.open(mypath+img)    
    nomeSemExtensao = img[0:-4]
    tamEmEscala = escala*tamanhoImg/100
    imgAlvo = imagem.resize((round(tamEmEscala),round(tamEmEscala)))
    if(escala<10):
        nomeImgRedimensionada = nomeSemExtensao +'_E0' + str(escala) + '.png'
    else:
        nomeImgRedimensionada = nomeSemExtensao +'_E' + str(escala) + '.png'
    imgAlvo.save(mypath+'rsz/' + nomeImgRedimensionada, optimize=True, quality=85)    
    return nomeImgRedimensionada   
 

''' Metodo verifica se a imagem ja foi calculada, caso execute este 
    prorgama partir da segunda vez. Otimiza tempo. '''
def pular_se_ja_existe(img):
    jaTem = False
    imgSemExtensao = img[0:-4]
    csvsCalculados = [f for f in listdir(mypath+'csv/') if isfile(join(mypath+'csv/', f))]
    for csvCalc in csvsCalculados:
        csvSemExtensao = csvCalc[0:-4]        
        if(csvSemExtensao == imgSemExtensao):
            jaTem = True
            checkPoint(' imagem ja calculada. ')
            break
    return jaTem
        
''' -------------- INICIO ----------------'''
checkPoint('inicio')
''' 3% é o menor tamanho possivel de conversao '''
escalas = [3, 5,20,50,80,100]
onlyfiles = ler_arquivos()
for pct in escalas:
    info_extra(pct)
    for img in onlyfiles:
        checkPoint(img + ' ' + str(pct)+ '%')
        contar_cratera(img, pct)        
checkPoint('Termino')
# 	273.0 - erro na imagem: mola_color_N-30_300.png
# 	9678. - erro na imagem: mola_color_N00_240.png
#	2510. - erro na imagem: mola_color_N-60_180.png