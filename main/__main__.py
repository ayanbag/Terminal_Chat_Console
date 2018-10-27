from __future__ import print_function, unicode_literals
import os
import colour 
import getpass
from pyfiglet import Figlet
import sys
from PyInquirer import style_from_dict, Token, prompt
import time
import login_auth_reg
from termcolor import colored,cprint
from pusher import Pusher
import pysher
from dotenv import load_dotenv
import json
import chatrooms_server
import getpass
import random

from progress.bar import FillingCirclesBar
from os import path
import env_platform

load_dotenv(dotenv_path='.env')

class TerminalChat():

    version=1.2 
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
    temp_dir=os.getcwd()
    os.chdir("C:")
    if path.isdir("TCN_Downloads")==True:
        pass
    else:
        os.system('mkdir TCN_Downloads')

    if path.isdir('TCN_To_Be_Upload')==True:
        pass
    else:
        os.system('mkdir TCN_To_Be_Upload')

    os.chdir(temp_dir)
    plat=env_platform.get_platform()
    if plat=='Linux' or plat=='OS X':
        value_plat=True
    elif plat=='Windows':
        value_plat=False

    def clear(self):
        if self.value_plat==True:
            os.system('clear')
        else:
            os.system('cls')
        


    def newsview(self):
        import newsser

        nwtemp=[]
        nwtemp=newsser.newsse()
        cprint(" NEWS :","magenta")
        for nw in nwtemp:
            print("        {}".format(nw))


    def sleep(self):
        t = 0.02
        t += t * random.uniform(-0.1, 0.1)
        time.sleep(t)
        
    def welcome(self):
        cprint(" Hi..There",'green',attrs=['bold'],file=sys.stderr)
        time.sleep(1)
        cprint(" Welcome to Secure Terminal Chat Network",'green',attrs=['bold'],file=sys.stderr)
        self.newsview()
        print("")
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

        self.clear()
        time.sleep(0.05)
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
        self.clear()

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
                    self.clear()
                    self.logincred()
            else:
                cprint(" incorrect username","red")
                print("")
                time.sleep(0.56)
                self.clear()
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
            self.clear()
            


        chatrooms=chatrooms_server.all_rooms()
        self.chatrooms=chatrooms

        if chatroom in self.chatrooms:
            self.chatroom=chatroom
            self.initPusher()
            self.clear()
            cprint(" ChatSpace Security Code: {}".format(self.chatroom),"red")
            print("")
        else:
            cprint(" No Secure Chat Room is found !!")
            print("")
            time.sleep(0.2)
            self.clear()
            self.chatselector()

    


    ''' Server Side '''
    def initPusher(self):
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', None), key=os.getenv('PUSHER_APP_KEY', None), secret=os.getenv('PUSHER_APP_SECRET', None), cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher = pysher.Pusher(os.getenv('PUSHER_APP_KEY', None), os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()
    
    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)

    def pusherCallback(self, message):
        from playsound import playsound
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
            os.chdir('C:\\TCN_To_Be_Upload')
            time.sleep(0.5)
            print("")
            os.system('dir')
            print("")
            flt=ftpserver.uploadfile()
            message=formate+"file is uploaded.[filename = {}]".format(flt)
            os.chdir(self.temp_dir)
        if message=='download file' or message=='ddf':
            os.chdir('C:\\TCN_Downloads')
            import ftpserver
            ftpserver.dwnldfile()
            os.chdir(self.temp_dir)
            message="........."
        if message=='exit':
            self.clear()
            self.main()
        if message=='open file':
            os.chdir('C:\\TCN_Downloads')
            fl=input(" [system]: filename -> ")
            os.system(fl)
            os.chdir(self.temp_dir)
            message="......."
        self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})

    def about(self):
        print("")
        cprint(" Terminal Chat Network v1.1","yellow")
        print("")
        cprint(" Version: {}".format(self.version),"yellow")
        print("")
        time.sleep(0.1)
        cprint(" Devoloped by Ayan Bag","yellow")
        time.sleep(1)
        k=input()
        self.main()
        

    def main(self):


        style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#00FFFF',
        Token.Instruction: '', 
        Token.Answer: '#2196f3 bold',
        Token.Question: '#7FFF00 bold',
        })

        self.clear()
        self.welcome()

        qus=[
            {
                'type':'list',
                'name':'choice',
                'message':'Enter :',
                'choices':['terminal chat','update','help','about','exit'],
                'default':'terminal chat'

            }
        ]

        answer=prompt(qus,style=style)

        if answer['choice']=='terminal chat':
                
            self.logincred()
            time.sleep(1)
            self.clear()
            self.chatselector()
            
            while True:
                self.getInput()

        elif answer['choice']=='about':
            self.about()

        elif answer['choice']=='exit':
            print("")
            print(" closing")
            time.sleep(0.5)
            self.clear()
            sys.exit(1)
        
        elif answer['choice']=='update':


            style = style_from_dict({
            Token.QuestionMark: '#E91E63 bold',
            Token.Selected: '#00FFFF',
            Token.Instruction: '', 
            Token.Answer: '#2196f3 bold',
            Token.Question: '#7FFF00 bold',
            })


            qus1=[
            {
                'type':'list',
                'name':'upd',
                'message':'Enter :',
                'choices':['update now','update release','exit'],
                'default':'terminal chat'

            }
            ]

            ans1=prompt(qus1,style=style)

            print("")
            if ans1['upd']=='update release':
                print('''UPDATE RELEASE:
                v1.1 : In-app file view is added
                    News feature is added to keep you updated with Updates news and new features
                v1.2 : Linux/UNIX enviroment support is added.''')
                time.sleep(1)
                a=input()
                chk=input(" want to go back ? (y/n): ")
                if chk=='y':
                    self.clear()
                    self.main()
                else:
                    time.sleep(0.5)
                    self.clear()
                    sys.exit(1)
            
            elif ans1['upd']=='update now':
                print(" ")
                os.system('pip install tcn_app')
                print("")
                cprint(" successfully updated")
                print("")
                self.clear()
                a=input(" want to go back(y/n) ->")
                if a=='y':
                    self.main()
                else:
                    sys.exit()
            elif ans1['udp']=='exit':
                print("")
                print(" closing")
                time.sleep(1)
                self.clear()
                sys.exit(1)
                
        elif answer['choice']=='help':
            print("")
            time.sleep(1)
            cprint(" ----------HELP----------","red")
            print("")
            print(colored(" note:","green")+" <> commands are only applicable inside ChatSpace.")
            print("       <> to upload the files put your desired file in To_Be_Upload folder in your C: Drive.")
            print("")
            print(" commands: sdf or send file -> to distribute a file in personal ChatSpace")
            print("           ddf or download file -> to collect the file which is distributed in ChatSpace")
            print("           open file -> to open the recently downloaded file")
            print("           exit -> to exit from current ChatSpace")
            print("")
            time.sleep(1)
            print("")
            k=input()
            chk=input(" want to go back ? (y/n): ")
            if chk=='y':
                self.clear()
                self.main()
            else:
                time.sleep(0.5)
                self.clear()
                sys.exit(1)

def mainload():
    TerminalChat().main()

if __name__=="__main__":
    TerminalChat().main()
