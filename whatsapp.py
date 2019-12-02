from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask, request, jsonify
import tempfile
import pickle
import sys
import time
import os

driver = webdriver.Chrome("./libs/chrome/win/chromedriver.exe")
driver.get("https://web.whatsapp.com/")

app = Flask(__name__)

@app.route("/whatsapp/enviar", methods = ['POST'])
def sendMenssage():
    data = request.json

    contact = driver.find_element_by_class_name('_2zCfw')
    contact.send_keys(str(''))
    for i in data:
        
        time.sleep(2)
        contato = i['contato']
        mensagem = i['mensagem']

        # selecino o contato que já existe
        contact = driver.find_element_by_class_name('_2zCfw')
        time.sleep(5)
        contact.send_keys(str(contato))

        # array usuarios list_msg[1]
        user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(str(contato)))
        time.sleep(5)
        user.click()

        # pego o campo de mensagem muda de 6 em 6 meses
        msg_box = driver.find_elements_by_class_name('_3u328')

        # mensagem
        msg_box[0].send_keys(str(mensagem))
        time.sleep(5)

        driver.find_element_by_class_name('_3M-N-').click()
        
    return jsonify(data)

@app.route("/whatsapp/qrcode", methods = ['GET'])

def get_qr( filename=None):

    driver.find_element_by_css_selector('div[data-ref]').get_attribute("data-ref")

    if "Clique para carregar o código QR novamente" in driver.page_source:
        reload_qr()
    qr = driver.find_element_by_css_selector('img[alt=\"Scan me!\"]')

    data = {'qrcode': qr.screenshot_as_base64, 'mensagem': 'QR disponível'}
    return jsonify(data)
    
def reload_qr():
    driver.find_element_by_css_selector('div[data-ref] > span > div').click()
    time.sleep(3)
    
app.run(debug=True)
sys.exit()
# Main 
def main():

    #Enter in Whatsapp Web and validate account
    try:

        driver = webdriver.Chrome("./libs/chrome/win/chromedriver.exe")
        driver.get("https://web.whatsapp.com/")

        input('Please enter the QR code, press any key to continue...')

    except:

        print('[ERROR] It has been impossible to enter WhatsApp Web...')

    os.system('cls')
    print('Welcome! n.n')

    while True:
        
        cmd = input()

        if isCMD_msg(cmd) == '/msg':
            list_msg = Parse_msg(cmd)

            send_msg(list_msg,driver)

#To parse cmd
def isCMD_msg(cmd):
    return cmd.split(' ')[0]

#To parse msg command to a list [count, person, msg]
def Parse_msg(cmd):
    # /msg [count] person@msg
      
    list_aux = []

    #Count msg
    list_aux.append((cmd.split('[')[1]).split(']')[0])

    #Person or Group
    list_aux.append((cmd.split('] ')[1]).split('@')[0])

    #Msg
    list_aux.append((cmd.split('] ')[1]).split('@')[1])

    return list_aux

#To send
def send_msg(list_msg,driver):

    # selecino o contato que já existe
    contact = driver.find_element_by_class_name('_2zCfw')
    contact.send_keys(list_msg[1])

    # array usuarios list_msg[1]
    user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(list_msg[1]))
    user.click()

    # pego o campo de mensagem muda de 6 em 6 meses
    msg_box = driver.find_elements_by_class_name('_3u328')

    # para cada qt de mensagem
    for i in range(int(list_msg[0])):
        time.sleep(20)
        msg_box[0].send_keys(list_msg[2])
        driver.find_element_by_class_name('_3M-N-').click()

if __name__ == '__main__':
    main()
sys.exit()