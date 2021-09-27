# Crater Craze
## _Contador de crateras Marcianas usando MOLA e PyCDA_
### Luiz Ahumada - luiz.ahumada@gmail.com

Esta documentação mostra como usar este projeto.

- Imagens coletadas do site http://www.mars.asu.edu/data/mola_color/
- Bilbioteca PyCDA https://github.com/AlliedToasters/PyCDA

## O que é cada arquivo
- **Programas em Python**
  - **1_AnaliseImagens.py** - Primeiro arquivo a ser executado, lê as imagens originais e gera o relatório csv
  - **2_ConversorLatLong.py** - O relatório gera as latitudes e longitudes em pixels, e é preciso converter para graus
  - **3_CalculaRepetida.py** - Analisa as crateras similares detectadas e as remove
  - **4_RegioesDeMarte.py** Baseado em um arquivo contendo as regioes geográficas de marte, este programa categoriza cada cratera em sua região correta.
- **Planilha CSV**
  - **RegioesMarte.csv** arquivo contendo latitude inicial e final e longitude inicial e final de cada região marciana
  - **resultadoCrateraMOLA.csv** - Arquivo exemplo com o 'resultado final'
- **Diretórios**
  - **/AllImages** Contem as imagens originais e diretórios intermediários de análise.
    - **/mola_color_N00_000.png** Imagem original exemplo
  - **/AllImages/csv** Resultado da primeira analise, arquivos analisados com imagens redimencionadas ficam com com sufixo "E" e a porcentagem "05" (que é 5%)
  - **/AllImages/csv_proc** Agrupado em um unico arquivo as crateras detectadas
  - **/AllImages/plot** imagens menores com a identificação (ponto vermelho) do PyCDA nas crateras
  - **/AllImages/rsz** Diretório para guardar as imagens redimensionadas.

