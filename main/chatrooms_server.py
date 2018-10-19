import mysql.connector

'''YOUR DATABASE DETAILS'''
chatroom_serv=mysql.connector.connect(
    host="xxxxxxxx",
    user="xxxxx",
    passwd="xxxxx",
    database="xxxxx"

)

rooms=chatroom_serv.cursor()

def all_rooms():
    room_list=[]
    rooms.execute("SELECT server_rooms FROM user_info.chatserver")
    chat_rooms_list=rooms.fetchall()
    for i in range(len(chat_rooms_list)):
        room_list.append(chat_rooms_list[i][0])
    return room_list

def new_room(room_name,idt):
    sql= "INSERT INTO user_info.chatserver (server_rooms,id) VALUE (%s,%s)"
    val=(room_name,idt)

    rooms.execute(sql,val)
    chatroom_serv.commit()
    