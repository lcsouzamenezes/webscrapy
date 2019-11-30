
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