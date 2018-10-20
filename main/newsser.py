from ftplib import FTP
import os

def newsse():
    ly=[]   
    '''YOUR FTP DETAILS'''
    ftp=FTP('your.com')
    ftp.login(user="********",passwd="*******")
    ftp.cwd('/xxxxxxxxx')

    os.chdir(os.getcwd()+'\\xxxxxxxxx')
    filename = "your_news_file_name.txt"
    localfile=open(filename,'wb')
    ftp.retrbinary('RETR '+filename,localfile.write,1024)
    print(" ")
    ftp.quit()
    localfile.close()

    filename="your_news_file_name.txt"
    file = open(filename, "r")

    for line in file:
        ly.append(line)
    os.chdir(os.getcwd()+'\\..')
    return ly