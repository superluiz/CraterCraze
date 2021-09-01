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

ImageFile.LOAD_TRUNCATED_IMAGES = True
cda = CDA()
mypath = 'C:/Users/Luiz/Documents/POSGRADUACAO_ASTRONOMIA/Mapa_Marte/AllImages/'
timestart = time.time()
tamanhoImg = 7680
mpp = 463.1

def ler_arquivos():
    infoExtras = open("informacoes.csv", "w")
    infoExtras.write("\nEscala;LaguraAltura;MetrosPorPixel\n")
    infoExtras.close()
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]

def contar_cratera(img,escala):
    if(False == pular_se_ja_existe(img)):    
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
        except:
            checkPoint('erro na imagem: ' + img)
            #pass
    
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
 
def checkPoint(texto):    
    tempo = time.time() - timestart
    print('\t' + str(tempo)[0:5] + ' - '+texto)

def info_extra(escala):
    infoExtras = open("informacoes.csv", "a")    
    infoExtras.write(str(escala) 
    + ';' + str(round(escala*tamanhoImg/100)) 
    + ';' + str(round((100/escala)*mpp)) + '\n')
    infoExtras.close()

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
        

checkPoint('inicio')
# escalas = [5,20,50,80,100]
escalas = [100]
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