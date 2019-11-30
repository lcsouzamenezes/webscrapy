#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from requests import get
from datetime import datetime
import time, json, sys

now = datetime.now()
print('## __SPYDER CRAWLLER | Start: '+str(now))

# parametros de busca
page = '1'
searchLimit = '2000' # maximo de 5000
searchCidade = '2700'
searchOrdenacao = '5'
ddd = "(03"

print('buscando '+searchLimit+' veículos, no site semiNovos.com.br... Crawling')

# pega todos os ids dos veículos
urlVeiculos = 'https://seminovos.com.br/carro/cidade[]-'+str(searchCidade)+'?page='+str(page)+'?ordenarPor='+str(searchOrdenacao)+'&registrosPagina='+str(searchLimit)
response = get(urlVeiculos)
soapVeiculos = BeautifulSoup(response.text, 'html.parser')

temVeiculo = soapVeiculos.find_all('h2')
temVeiculo = temVeiculo[1].get_text()

if(response != '<Response [200]>'):

    if(temVeiculo == 'Nenhum veículo encontrado'):

        print(json.dumps({'mensagem' : temVeiculo}))
        sys.exit()

    else:

        print('o site semiNovos.com.br respondeu: '+str(response)+' | '+str(now))

        idDosVeiculos = soapVeiculos.findAll("span", {"itemprop": "sku"})

        # todas as informacoes do veiculo
        marca = soapVeiculos.find("span", {"itemprop": "brand"}).get_text()
        modelo = soapVeiculos.find("span", {"itemprop": "model"}).get_text()
        name = soapVeiculos.find("span", {"itemprop": "name"}).get_text()
        price = soapVeiculos.find("span", {"itemprop": "price"}).get_text()

        #abro o arquivo gravacao
        arquivo = open('resultado.json', 'w')

        a = 0
        dados = []

        for idDosVeiculo in idDosVeiculos:
            
            print('aguardamos 2 segundos para buscar o veículo '+str(idDosVeiculo.text)+' | '+str(now))
            time.sleep(2)
            a+=1
            idDosVeiculo = idDosVeiculo.text

            # pega todos os dados de contato
            urlPegaVeiculos = 'https://seminovos.com.br/comparar?idVeiculos='+idDosVeiculo
            response = get(urlPegaVeiculos)

            # pego as proximas informacoes
            soapVeiculos = BeautifulSoup(response.text, 'html.parser')
            check = soapVeiculos.find(class_ = 'block-title clean')

            if (str(check) == "None" ):
                name = soapVeiculos.find(class_ = 'owner-info').find('h5').get_text()
                links = soapVeiculos.find_all('a', href=True)
                numeros = []
                
                print('buscando telefones | '+str(now))
                for telefones in links:

                    print('adicionando telefone | '+str(now))
                    # busca por DDD 31, 11 etc...
                    if(telefones.text.find(ddd) > 0):
                        numeros.append(telefones.text.strip())

                # por fim crio um json
                dados.append( {'id': int(idDosVeiculo), "name": str(name), "telephones": numeros, "marca": str(marca), "modelo": str(modelo), "price" : float(price)} )
                print('------------------------')
                print(dados)
                print('------------------------')
            else:
                print('Veículo já foi vendido | '+str(now))
        
    # gravo o arquivo resultado.json 
    arquivo.write(json.dumps(dados))
    arquivo.close()

else:
    print(json.dumps({'mensagem' : 'Não houve comunicação com o site'}))
    print('o site semiNovos.com.br respondeu: '+str(response)+' | '+str(now))
    
sys.exit()