import os
import logging
import socket
import select

'''
import csv
import hashlib
import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
'''


class Room:
    def __init__(self, name):
        self.__room_name = name
        self.__Sockt = []
        self.__Nickin = []
        self.__isopen = False

    def give_name_to_room(self, name):
        self.__room_name = name

    def get_name(self):
        return self.__room_name

    def add_to_room(self, s1):
        self.__Sockt.append(s1)

    def add_to_room_nick(self, nick):
        self.__Nickin.append(nick)

    def change_room_status(self):
        if self.__isopen == False:
            self.__isopen = True
        else:
            self.__isopen = False

    def who_in_room(self):
        return self.__Sockt

    def who_in_room_nicks(self):
        return self.__Nickin

    def get_status(self):
        return self.__isopen

    def desp_room(self):
        return [self.__room_name, self.__isopen, len(self.__Sockt)]

    def __str__(self):
        return self.__room_name + " " + str(self.__isopen) + " " + str(len(self.__Sockt))

#format len chr retrun the len in 2 chr
def one_or_two_chr(my_len):
    ''' get int return str with two byte'''
    try:
        if my_len < 10:
            my_len = "0{}".format(my_len)
        else:
            my_len = str(my_len)
        return my_len
    except ValueError or TypeError:
        logging.error("one or two get str instead int")
        return None

# txt loggin file for debug and data
def logapp():
    try:
        mypath = os.getcwd()
        try:
            os.mkdir(mypath + r'\log')
        except FileExistsError:
            print ("the dir exist")
        finally:
            FORMAT = '%(asctime)s [ %(levelname)s ]  :  %(message)s'
            logging.basicConfig(filename=mypath + '\\log\server.txt', level=logging.INFO, filemode="w", format=FORMAT, datefmt="Date %d/%m/%y Time: %I:%M:%S %p")
    except:
        print("err the file wasn't open")
        logging.warning("error: the log file wasn't open")


def note_all(Nick, msg, client_list):
    try:
        MSG_len = len(msg) + len(Nick) + Nick_len_byte
        MSG_len = one_or_two_chr(MSG_len)
        Nick_len = one_or_two_chr(len(Nick))
        msg_to_send = "{}{}{}{}{}".format(protocol_connect, MSG_len, Nick_len, Nick, msg)
        print(msg)
        logging.info(msg_to_send)
        for connect in client_list:
            connect.send(msg_to_send.encode())
    except IndexError or Exception:
        logging.error("index error or {one or two} err")


def broadcastMsg(Nick, MSG, client_list, client):
    MSG_len = len(MSG) + len(Nick) + Nick_len_byte
    MSG_len = one_or_two_chr(MSG_len)
    Nick_len = one_or_two_chr(len(Nick))
    msg_to_send = "{}{}{}{}{}".format(protocol_broadcast, MSG_len, Nick_len, Nick, MSG)
    logging.info(msg_to_send)
    for i in client_list:
        if i is not client:
            i.send(msg_to_send.encode())


# enter to room
def go_to_room(client, nick, room_num):
    try:
        if rooms[room_num].get_status() is True:
            rooms[room].add_to_room(client)
            rooms[room].add_to_room_nick(nick)
            return 1
        else:
            return 0
    except Exception as EX:
        logging.warning(EX)


def drap_the_Client(client):
    where_the_client_in = what_is_client_room(client)
    if where_the_client_in is not None:
        inx = 0
        for cl in rooms[where_the_client_in].who_in_room():
            if cl == client:
                rooms[where_the_client_in].who_in_room().remove(cl)
                break
            inx += 1
        try:
            nic = rooms[where_the_client_in].who_in_room_nicks()[inx]
            rooms[where_the_client_in].who_in_room_nicks().pop(inx)
            socket_list.remove(client)
            nick_list.remove(nic)
            #client.destroy
            logging.info("the client {} drapped out in successfully".format(nic))
            print("{} drap out".format(nic))
        except IndexError:
            logging.error("the client didnt drap fully")
        except ValueError:
            logging.error("the server didnt found the nick name")


# exit from room
def exit_client_from_room(room_num, client, nick, goodbye=0):
    try:
        if goodbye ==0:
            for cl in rooms[int(room_num)].who_in_room():
                if cl == client:
                    rooms[int(room_num)].who_in_room().remove(cl)
                    break
            for cl in rooms[int(room_num)].who_in_room_nicks():
                if cl == nick:
                    rooms[int(room_num)].who_in_room_nicks().remove(cl)
                    break
        elif goodbye == 1:
            drap_the_Client(client)
    except ValueError or TypeError:
        logging.error("the func exit from room didn't get int ")


# find client in rooms
def what_is_client_room(client):
    for room_num in range(len(rooms)):
        for cl in rooms[room_num].who_in_room():
            if cl == client:
                return room_num
    return None


# check the nick isn't exist
def spicel_nick(nick, Nick_ls):
    for n in Nick_ls:
        if n == nick:
            return False
    return True


logapp()
logging.info("the server is working")
print("the server is working")

# server const
Nick_len_byte = 2
Msg_len_byte = 2
room_byte = 1

# protocol send msg
protocol_broadcast = 1
protocol_enter_to_room = 2
protocol_created_room = 3
protocol_broad_list = 4
protocol_disconnect = 8
protocol_connect = 9

# protocol recive msg
inptc_connect = 1
inptc_enter_room = 2
inptc_exit_room = 3
inptc_created_room = 4
inptc_delet_room = 5
inptc_get_msg = 6
inptc_Who_in = 7
inptc_list_rooms = 8
inptc_goodbye = 9

#server local Varint
socket_list = []
client_list = []
nick_list = []
rooms = []
check_test =" "
client_in_room_num = 0


Lobi = Room("lobi")
rooms.append(Lobi)
Lobi.change_room_status()

# open Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 8080))
s.listen(3)
socket_list.append(s)

# ready to get information
while True:
    try:
        read_ready, _, _ = select.select(socket_list, [], [])
        for i in read_ready:
            if i is s:
                client, addr = s.accept()
                client_list.append(client)
                socket_list.append(client)
                Lobi.add_to_room(client)
                print("new connection")  ##
                logging.info('new connection')
            else:
                while True:
                    try:
                        msg_Type = int(i.recv(1).decode())
                        msg_len = int(i.recv(Msg_len_byte).decode())
                        check_test = 0

                        # new connection
                        if msg_Type == inptc_connect:
                            nick_len = int(i.recv(Nick_len_byte).decode())
                            nick_len = one_or_two_chr(nick_len)
                            nick = i.recv(int(nick_len)).decode()
                            check_test = 1
                            if len(socket_list)<=100:
                                room_num = what_is_client_room(i)
                                if spicel_nick(nick, nick_list) is True:
                                    nick_list.append(nick)
                                    rooms[room_num].add_to_room_nick(nick)
                                    msg = f"{nick} join to Lobbi"
                                    # successful connection
                                    note_all(nick, msg, rooms[room_num].who_in_room())
                                    break
                                else:
                                    # disconnection
                                    msg_to_send = "{}{}".format(protocol_disconnect, '01')
                                    i.send(msg_to_send.encode())
                            else:
                                # disconnection
                                msg_to_send = "{}{}".format(protocol_disconnect, '01')
                                i.send(msg_to_send.encode())

                        # enter to room
                        elif msg_Type == inptc_enter_room:
                            try:
                                nick_len = int(i.recv(Nick_len_byte).decode())
                                nick = i.recv(int(nick_len)).decode()
                                room = int(i.recv(room_byte).decode())
                                leave_room_num = what_is_client_room(i)
                                status_enter = go_to_room(i, nick, room)
                                check_test = 2
                                if status_enter == 1:
                                    msg_to_send = "{}{}{}".format(protocol_enter_to_room, "01", "1")
                                    if leave_room_num == None:
                                        logging.warning("problem to find client")
                                    else:
                                        exit_client_from_room(leave_room_num, i, nick)
                                        logging.info("the {} leave room num{}".format(nick, leave_room_num))
                                        logging.info("the {} enter room num{}".format(nick, room))
                                    i.send(msg_to_send.encode())
                                    #if room != 0:
                                    msg = f" join to room num {room}"
                                    broadcastMsg(nick, msg, rooms[room].who_in_room(),i)
                                else:
                                    msg_to_send = "{}{}{}".format(protocol_enter_to_room, "01", "0")
                                    i.send(msg_to_send.encode())
                            except TypeError:
                                logging.error("TypeError, the client send bad msg for enter room")

                        # created room
                        elif msg_Type == inptc_created_room:
                            j = 0
                            try:
                                name_room = i.recv(msg_len - Msg_len_byte).decode()
                                check_test = 3
                                if len(rooms) < 10:
                                    for r in rooms:
                                        while name_room == r.get_name():
                                            j = j + 1
                                            name_room = "random room num: " + str(j)
                                        continue
                                    new_room = Room(name_room)
                                    new_room.change_room_status()
                                    rooms.append(new_room)
                                    room_num = len(rooms)
                                    msg_to_send = "{}{}{}".format(protocol_created_room, "01", "1")
                                    print("the room {} created".format(name_room))
                                    logging.info("the room {} created".format(name_room))
                                else:
                                    msg_to_send = "{}{}{}".format(protocol_created_room, "01", "0")
                                    print("there is 9 room already")
                                    logging.info("there is 9 room already")
                                i.send(msg_to_send.encode())
                            except TypeError:
                                logging.error("TypeError, the client send bad msg for enter room")

                        # exit from room
                        elif msg_Type == inptc_exit_room:
                            try:
                                nick_len = int(i.recv(Nick_len_byte).decode())
                                nick = i.recv(int(nick_len)).decode()
                                leave_room_num = what_is_client_room(i)
                                check_test = 4
                                if leave_room_num != 0:
                                    go_to_room(i, nick, 0)
                                    exit_client_from_room(leave_room_num, i, nick)


                            except Exception as EX:
                                logging.error(EX)

                        # delete room
                        elif msg_Type == inptc_delet_room:
                            try:
                                room = int(i.recv(room_byte).decode())
                                for leaves in rooms[room].who_in_room():
                                    rooms[0].add_to_room(leaves)
                                for leaves_nick in rooms[room].who_in_room_nicks():
                                    rooms[0].add_to_room_nick(leaves_nick)
                                rooms.pop(room)

                            except TypeError as EX:
                                logging.error(EX)
                            except IndexError:
                                msg_to_send = "{}{}{}".format(protocol_broad_list, 27, "the room is not exist yet")
                                i.send(msg_to_send.encode())

                        elif msg_Type == inptc_get_msg:
                            try:
                                nick_len = int(i.recv(Nick_len_byte).decode())
                                nick = i.recv(nick_len).decode()
                                msg = i.recv(msg_len - Nick_len_byte - nick_len).decode()
                                client_in_room_num = what_is_client_room(i)
                                if client_in_room_num is None:
                                    logging.warning("Problem cretic")
                                else:
                                    broadcastMsg(nick, msg, rooms[client_in_room_num].who_in_room(), i)
                            except TypeError as EX:
                                logging.error(EX)

                        # Who in my room
                        elif msg_Type == inptc_Who_in:
                            try:
                                nick_len = int(i.recv(Nick_len_byte).decode())
                                nick = i.recv(nick_len).decode()
                                room_num = what_is_client_room(i)
                                if room_num is not None:
                                    msg = "in {} room:\n".format(rooms[room_num].get_name())
                                    nicks = rooms[room_num].who_in_room_nicks()
                                    for parivt in nicks:
                                        msg += parivt + "\n"
                                    MSG_len = len(msg) + Msg_len_byte
                                    MSG_len = one_or_two_chr(MSG_len)
                                    msg_to_send = "{}{}{}".format(protocol_broad_list, MSG_len, msg)
                                    i.send(msg_to_send.encode())
                            except TypeError as EX:
                                logging.error(EX)

                        # list of all rooms
                        elif msg_Type == inptc_list_rooms:
                            msg = " rooms are opening:\n"
                            for j in range(len(rooms)):
                                msg += "{}. {}\n".format(j, rooms[j].get_name())
                            MSG_len = len(msg) + Msg_len_byte
                            MSG_len = one_or_two_chr(MSG_len)
                            msg_to_send = "{}{}{}".format(protocol_broad_list, MSG_len, msg)
                            i.send(msg_to_send.encode())

                        #client want leave
                        elif msg_Type == inptc_goodbye:
                            try:
                                nick_len = int(i.recv(Nick_len_byte).decode())
                                nick = i.recv(int(nick_len)).decode()
                                leave_room_num = what_is_client_room(i)
                                goodbye = 1
                                exit_client_from_room(leave_room_num, i, nick, goodbye)

                            except TypeError as EX:
                                logging.error(EX)
                        break
                    except ValueError or TypeError:
                        logging.warning("the client {} drapped out, check_test = {}".format(i,check_test))
                        drap_the_Client(i)
                        break
                    except ConnectionError or ConnectionResetError:
                        logging.warning("the client {} drapped out, ".format(i))
                        drap_the_Client(i)
                        break
    except UnicodeDecodeError:
        print("write in English only")  # Todo: send msg to client
        # msg_to_send()
