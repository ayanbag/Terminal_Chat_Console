from __future__ import print_function, unicode_literals
import os
import colour 
import getpass
from pyfiglet import Figlet
import sys
from PyInquirer import style_from_dict, Token, prompt
import time
import login_auth_reg
from tqdm import tqdm
from termcolor import colored,cprint
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import json
import chatrooms_server
import getpass
import random
from playsound import playsound
from progress.bar import FillingCirclesBar

load_dotenv(dotenv_path='.env')

class TerminalChat():
        
    pusher=None
    channel=None
    answ=None
    clientPusher=None
    user=None
    users=dict()
    temp_data=login_auth_reg.searchuser_password()
    for i in range(len(temp_data)):
        users[temp_data[i][0]]=temp_data[i][1]

    chatrooms=[]
    chatrooms=chatrooms_server.all_rooms()
    
    
    def sleep(self):
        t = 0.06
        t += t * random.uniform(-0.1, 0.1)
        time.sleep(t)
        
    def welcome(self):
        cprint(" Hi..There",'green',attrs=['bold'],file=sys.stderr)
        time.sleep(1)
        cprint(" Welcome to Secure Terminal Chat Network",'green',attrs=['bold'],file=sys.stderr)
        time.sleep(1)
        print("")
        print(" commands: sdf or send file -> to distribute a file in persona ChatSpace")
        print("           ddf of download file -> to collect the file which is distributed in ChatSpace")
        print("           exit -> to exit from current ChatSpace")
        time.sleep(1)
        print("")
        
    def logincred(self):
        style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#00FFFF',
        Token.Instruction: '', 
        Token.Answer: '#2196f3 bold',
        Token.Question: '#7FFF00 bold',
        })
        
    
        time.sleep(0.2)
        questions=[ 
            {
                'type':'list',
                'name':'log',
                'message':'Choose one :',
                'choices': ['login','registration'],
                'default':'login'
            }
        ]

        answers=prompt(questions,style=style)
        os.system('cls')
        time.sleep(0.01)
        print("")
        #########################################################
        suffix = '%(index)d/%(max)d [%(elapsed)d / %(eta)d / %(eta_td)s]'
        bar = FillingCirclesBar(" connecting to TCN server ", suffix=suffix)
        for i in bar.iter(range(100)):
            self.sleep()
        #########################################################
        time.sleep(1.0)
        os.system("cls")
        colour.prGreen("connected")
        time.sleep(0.5)
        os.system('cls')

        colour.prGreen("=================")
        colour.prGreen("||    LOGIN    ||")
        colour.prGreen("=================")
        print(" ")
        user1=dict()
        temp_data=login_auth_reg.searchuser_password()
        for i in range(len(temp_data)):
                user1[temp_data[i][0]]=temp_data[i][1]
        self.users=user1
        

        if answers['log']=='login':
            username=input(" username: ")
            password=getpass.getpass(" password: ")
            time.sleep(0.1)
            print("")
            
            #############################################
            a=0
            s="."
            sys.stdout.write( ' please wait ' )
            while a<=10:
                sys.stdout.write( s )
                sys.stdout.flush()
                time.sleep(0.3)
                a=a+1
            ##############################################
            
            print("")
            time.sleep(0.67)

            if username in self.users:
                if self.users[username]== password:
                    self.user=username
                    print("")
                    cprint(" logged in successfully","cyan")
                    time.sleep(1)

                else:
                    cprint(" incorrect password","red")
                    print(" ")
                    time.sleep(0.56)
                    os.system('cls')
                    self.logincred()
            else:
                cprint(" incorrect username","red")
                print("")
                time.sleep(0.56)
                os.system('cls')
                self.logincred()


        elif answers["log"]=="registration":
            name=input(" name: ")
            username=input(" username: ")
            password=getpass.getpass(" password: ")
            uniqid=name+random.choice(["q","@","%","w","r","g","hg","crate","traitor","aligator","unknw","@@@@@","&&&&","###"])+username
            checker=login_auth_reg.register(uniqid,name,username,password)
            time.sleep(0.95)
            cprint(" registration successfull","yellow")
            time.sleep(1)
            self.logincred()
        
    



    def chatselector(self):
        
        chatroom=input(" Enter the ChatSpace Secure Code: ")
    
        if chatroom in self.chatrooms:
            print("")
        else:
            cprint(" New ChatSpace code is detected !!!","red")
            time.sleep(1)
            chatrooms_server.new_room(chatroom,0)
            print("")
            time.sleep(1)
            os.system('cls')
            


        chatrooms=chatrooms_server.all_rooms()
        self.chatrooms=chatrooms

        if chatroom in self.chatrooms:
            self.chatroom=chatroom
            self.initPusher()
            os.system('cls')
            cprint(" ChatSpace Security Code: {}".format(self.chatroom),"red")
            print("")
        else:
            cprint(" No Secure Chat Room is found !!")
            print("")
            time.sleep(0.2)
            os.system('cls')
            self.chatselector()
    


    ''' Server Side '''

    def initPusher(self):
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', None), key=os.getenv('PUSHER_APP_KEY', None), secret=os.getenv('PUSHER_APP_SECRET', None), cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher = pysher.Pusher(os.getenv('PUSHER_APP_KEY', None), os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()
    
    def connectHandler(self,data):
        self.channel=self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage',self.pusherCallback)

    def pusherCallback(self, message):
        formate="["+self.user+"]: "
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored("[{}]: {}".format(message['user'], message['message']), "yellow"))
            playsound('intuition.mp3')
            print(colored(formate,"green"))
    
    def getInput(self):
        
        formate="["+self.user+"]: "
        message = input(colored(formate,"green"))
        if message=="send file" or message=="sdf":
            import ftpserver
            ftpserver.uploadfile()
            message=formate+"File is uploaded. Download it."
        if message=='download file' or message=='ddf':
            import ftpserver
            ftpserver.dwnldfile()
        if message=='exit':
            os.system('cls')
            self.main()
        self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})

    def about(self):
        print("")
        cprint(" Terminal Chat Network v1.0","yellow")
        print("")
        cprint(" Version: 1.0","yellow")
        print("")
        time.sleep(0.1)
        cprint(" Devoloped by Ayan Bag","yellow")
        time.sleep(5)
        self.main()
        

    def main(self):


        style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#00FFFF',
        Token.Instruction: '', 
        Token.Answer: '#2196f3 bold',
        Token.Question: '#7FFF00 bold',
        })

        os.system('cls')
        self.welcome()

        qus=[
            {
                'type':'list',
                'name':'choice',
                'message':'Enter :',
                'choices':['terminal chat','about','exit'],
                'default':'terminal chat'

            }
        ]

        answer=prompt(qus,style=style)

        if answer['choice']=='terminal chat':
                
            self.logincred()
            time.sleep(1)
            os.system('cls')
            self.chatselector()
            while True:
                self.getInput()
        
        elif answer['choice']=='about':
            self.about()

        elif answer['choice']=='exit':
            print(" closing")
            time.sleep(0.5)
            os.system('cls')
            sys.exit(1)

if __name__=="__main__":
    TerminalChat().main()
