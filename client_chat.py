import os
import logging
import random
import socket
import threading
# from flask import Flask,render_template
import time
from flask import Flask,render_template

app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug = True)

# app to see log plot
def log_app():
    mypath = os.getcwd()
    FORMAT = '%(asctime)s [ %(levelname)s ]  :  %(message)s'
    logging.basicConfig(filename=mypath + '\\log\client_{}.txt'.format(random.randint(0,1500)), level=logging.INFO, filemode="w", format=FORMAT,
                        datefmt="Date %d/%m/%y Time: %I:%M:%S %p")

#format len chr retrun the len in 2 chr
def one_or_two_chr(my_len):
    ''' get int return str with two byte'''
    if my_len < 10:
        my_len = "0{}".format(my_len)
    else:
        my_len = str(my_len)
    return my_len

#print room
def room_exist():
    msg_to_send = "{}{}".format(prtocol_list_of_room, "00")  # exm:800
    s.send(msg_to_send.encode())
    time.sleep(tsleep)

#len msg less 90 chr
def check_len_msg(msg):
    if len(msg) > 90:
        return False
    else:
        return True


# send msg in currently room
def send_msg(Nick, Sock, protocol_msg=6, not_lobi=1):
    global room_nummber_requst
    while True:
        msg_to_send = ''


        # send the nick to server
        if protocol_msg == prtocol_connect:
            len_nick_name = one_or_two_chr(len(Nick))
            MSG_len = int(len_nick_name) + Nick_len_byte + Msg_len_byte + room_byte
            MSG_len = one_or_two_chr(MSG_len)
            msg_to_send = "{}{}{}{}".format(protocol_msg, MSG_len, len_nick_name, Nick)  # exm:10703Ahi
            Sock.send(msg_to_send.encode())
            break

        # enter to room
        elif protocol_msg == prtocol_enter_to_room:
            try:
                if not_lobi == 1:
                    room_exist()
                    try:
                        room_nummber_requst = int(input("enter the room's number to get in:  "))
                    except TypeError:
                        logging.error("the user didn't write int for room num ")
                        print("you must enter int, you wrote str")
                        room_nummber_requst = 0
                else:
                    room_nummber_requst = 0
                len_message = Msg_len_byte + len(Nick) + Nick_len_byte + room_byte
                MSG_len = one_or_two_chr(len_message)
                Nick_len = one_or_two_chr(len(Nick))
                msg_to_send = "{}{}{}{}{}".format(protocol_msg, MSG_len, Nick_len, Nick,room_nummber_requst)  # exm:20803Ahi1
                Sock.send(msg_to_send.encode())
                break

            except ValueError:
                logging.error("the user enter wrong room")

        # exit from the room
        elif protocol_msg == prtocol_exit_from_room:
            len_message = len(Nick) + Nick_len_byte + room_byte
            MSG_len = one_or_two_chr(len_message)
            Nick_len = one_or_two_chr(len(Nick))
            msg_to_send = "{}{}{}{}".format(protocol_msg, MSG_len, Nick_len, Nick)  # exm:30503Ahi
            Sock.send(msg_to_send.encode())
            break

        # create room
        elif protocol_msg == prtocol_create_room:
            name_room = input("enter the name of the room: ")
            len_name_room = len(name_room) + Msg_len_byte
            len_name_room = one_or_two_chr(len_name_room)
            msg_to_send = "{}{}{}".format(protocol_msg, len_name_room, name_room)  # exm:410nameroom
            Sock.send(msg_to_send.encode())
            break

        # delete the room
        elif protocol_msg == prtocol_delet_room:
            try:
                room_exist()
                room_nummber = int(input("enter the room's number for delete :  "))
                if room_nummber == 0:
                    print("you can't delete the Lobi")
                else:
                    len_message = Msg_len_byte + room_byte
                    MSG_len = one_or_two_chr(len_message)
                    msg_to_send = "{}{}{}".format(protocol_msg, MSG_len, room_nummber)  # exm:5002
                    Sock.send(msg_to_send.encode())
                break
            except ValueError:
                logging.error("the user enter wrong room")

        # send chat msg
        elif protocol_msg == prtocol_send_msg:
            write_msg = input()
            while check_len_msg(write_msg) is False:
                print("it's too long")
                write_msg = input()

            #for menu write menu in board
            if write_msg.lower() == 'menu':
                menu(client_nick_name, s)
                continue

            elif write_msg.lower() == 'exit':
                room_nummber_requst = 0
                len_message = Msg_len_byte + len(Nick) + Nick_len_byte + room_byte
                MSG_len = one_or_two_chr(len_message)
                Nick_len = one_or_two_chr(len(Nick))
                msg_to_send = "{}{}{}{}{}".format(prtocol_enter_to_room, MSG_len, Nick_len, Nick,room_nummber_requst)  # exm:20803Ahi0
                Sock.send(msg_to_send.encode())
                continue
            #TODO: this is only for try bad msg --> it's work ok
            #elif write_msg == "000":
            #   s.send("dsadadaddad".encode())

            #for stop the progrm write goodbye in board
            elif write_msg.lower() == 'goodbye':
                len_message = len(Nick) + Nick_len_byte + room_byte
                MSG_len = one_or_two_chr(len_message)
                Nick_len = one_or_two_chr(len(Nick))
                msg_to_send = "{}{}{}{}".format(prtocol_goodbye, MSG_len, Nick_len, Nick)  # exm:30503Ahi
                Sock.send(msg_to_send.encode())
                break

            #send simpel msg
            else:
                len_message = len(write_msg) + len(Nick) + Nick_len_byte + room_byte
                MSG_len = one_or_two_chr(len_message)
                Nick_len = one_or_two_chr(len(Nick))
                msg_to_send = "{}{}{}{}{}".format(protocol_msg, MSG_len, Nick_len, Nick, write_msg)  # exm:61003Ahihello



        # the clients in my room
        elif protocol_msg == prtocol_Who_in_the_room:
            len_nick = len(client_nick_name)
            len_message = room_byte + Nick_len_byte + Msg_len_byte + len_nick
            MSG_len = one_or_two_chr(len_message)
            len_nick = one_or_two_chr(len_nick)
            msg_to_send = "{}{}{}{}".format(protocol_msg, MSG_len, len_nick, client_nick_name)  # exm:70503Ahi
            Sock.send(msg_to_send.encode())
            break

        # give me all exist rooms
        elif protocol_msg == prtocol_list_of_room:
            room_exist()
            break

        # finally
        logging.info("msg from client to server -" + msg_to_send)
        Sock.send(msg_to_send.encode())

# print msg to client
def printMsg(Nick, MSG, flag=0):
    if flag == 0:
        msg_to_print = "{}: {}".format(Nick, MSG)
        print("{}".format(msg_to_print))

    elif flag == 1:
        msg_to_print = "{}".format(MSG)
        print("{}".format(msg_to_print))

# login with a nick name
def login_nic():
    global check_test
    while True:
        client_nick_name = input("enter your nick name:\n")
        if len(client_nick_name) > 10:
            print("the nick is too long\n")
        elif len(client_nick_name) == 0:
            print("you must choose Nick\n")
        else:
            send_msg(client_nick_name, s, prtocol_connect)
            msg_Type = 0
            msg_len = 0
            try:
                check_test = 0
                msg_Type = int(s.recv(1).decode())
                msg_len = int(s.recv(Msg_len_byte).decode())
            except TypeError:
                logging.error("got wrong msg/ protcol form server, check test = {}".format(check_test))
                break
            finally:
                if msg_Type == inptc_fail_connect:  # fail nick name
                    print("the nick is already exist")
                    logging.info("the user try exist nick")
                    continue
                elif msg_Type == inptc_successful_connect:  # boradcast connect msg from server
                    try:
                        check_test = 1
                        nick_len = int(s.recv(Nick_len_byte).decode())
                        nick = s.recv(nick_len).decode()
                        msg_byte = int(msg_len - Nick_len_byte - nick_len)
                        msg = s.recv(msg_byte).decode()
                        printMsg(nick, msg, 1)
                        logging.info("the user connect with nick:" + nick)
                        return client_nick_name
                    except TypeError:
                        logging.error("got wrong msg/ protcol form server, check test = {}".format(check_test))
                        break

# menu for client
def menu(Nick, SOCK):
    chosen = 0
    logging.info("the menu is open")
    while True:
        flag = 0
        print("welcome to chat! what are you asking? ")
        print(
            "1. Enter to Lobi. \n2. Create new room\n3. Delete room.\n4. Enter to room.\n5. Tell me about all the exist rooms.\n6. Who in the room")
        try:
            chosen = int(input("choose your option:\n"))
        except ValueError as ex:
            print("choose from option")
            flag = 1
            logging.warning("error: " + str(ex))  ##
        except TypeError as exc:
            print("choose from option")
            flag = 1
            logging.warning("error: " + str(exc))  ##
        finally:
            if flag == 0:
                if chosen == 1:  # enter to Lobi
                    send_msg(Nick, SOCK, prtocol_enter_to_room, 0)
                    logging.debug("try to enter to lobi")
                    break
                elif chosen == 2:  # create room
                    send_msg(Nick, SOCK, prtocol_create_room)
                    logging.info("try to create room")
                    break
                elif chosen == 3:  # delete room
                    send_msg(Nick, SOCK, prtocol_delet_room)
                    logging.info("try delet the room ")
                    break
                elif chosen == 4:  # enter to room
                    send_msg(Nick, SOCK, prtocol_enter_to_room)
                    logging.debug("try enter to room ")  #
                    break

                elif chosen == 5:  # print all room
                    send_msg(Nick, SOCK, prtocol_list_of_room)
                    logging.debug("try get all rooms exist")  #
                    break

                elif chosen == 6:  # print all partner in room
                    send_msg(Nick, SOCK, prtocol_Who_in_the_room)
                    logging.debug("try get all nick in room")  #
                    break

# client local const
Nick_len_byte = 2
Msg_len_byte = 2
room_byte = 1
tsleep=0.8

# protocol variant to send
prtocol_connect = 1
prtocol_enter_to_room = 2
prtocol_exit_from_room = 3
prtocol_create_room = 4
prtocol_delet_room = 5
prtocol_send_msg = 6
prtocol_Who_in_the_room = 7
prtocol_list_of_room = 8
prtocol_goodbye = 9

# inbox_protocl variant
intpc_boardcast_msg = 1
inptc_ent_room = 2
inptc_creat_room = 3
intpc_print_status = 4
inptc_fail_connect = 8
inptc_successful_connect = 9

#init client Var
now_room = 0
room_nummber_requst = 0
check_test = " "
msg_Type = 0
msg_len = 0

log_app()

# Socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 8080))

logging.info("connect to server")
client_nick_name = login_nic()

# ready to do mission
thread_send = threading.Thread(target=send_msg, args=(client_nick_name, s, prtocol_send_msg,))
thread_send.start()

# part of get order or answer
while True:
    try:
        check_test = "00"
        msg_Type = int(s.recv(1).decode())
        msg_len = int(s.recv(Msg_len_byte).decode())
        if msg_Type == intpc_boardcast_msg:  # boradcast msg from server
            check_test = "01"
            nick_len = int(s.recv(Nick_len_byte).decode())
            nick = s.recv(nick_len).decode()
            msg_byte = int(msg_len - Nick_len_byte - nick_len)
            msg = s.recv(msg_byte).decode()
            printMsg(nick, msg)
        elif msg_Type == inptc_successful_connect:  # boradcast connect msg from server
            check_test = "02"
            nick_len = int(s.recv(Nick_len_byte).decode())
            nick = s.recv(nick_len).decode()
            msg_byte = int(msg_len - Nick_len_byte - nick_len)
            msg = s.recv(msg_byte).decode()
            printMsg(nick, msg, 1)

        elif msg_Type == inptc_ent_room:
            try:
                check_test = "03"
                wait_for_success_or_fail = int(s.recv(1))
                if wait_for_success_or_fail == 1:
                    now_room = int(room_nummber_requst)
                    printMsg(client_nick_name, "{} join to room num: {}".format(client_nick_name, now_room), 1)
                elif wait_for_success_or_fail == 0:
                    printMsg(client_nick_name,
                             "{} can't join to room num: {}".format(client_nick_name, room_nummber_requst), 1)
            except ValueError:
                print("cant enter to room")
                logging.warning("got wrong msg/ protcol form server, check test = {}".format(check_test))

        elif msg_Type == inptc_creat_room:
            try:
                check_test = "04"
                wait_for_success_or_fail = int(s.recv(1))
                if wait_for_success_or_fail == 1:
                    printMsg(client_nick_name, "{} created new room!".format(client_nick_name), 1)
                elif wait_for_success_or_fail == 0:
                    printMsg(client_nick_name, "{} can't created room ! ".format(client_nick_name), 1)
            except ValueError:
                print("cant enter to room")
                logging.warning("got wrong msg/ protcol form server, check test = {}".format(check_test))

        elif msg_Type == intpc_print_status:
            try:
                check_test = "05"
                msg_byte = int(msg_len - Nick_len_byte)
                msg = s.recv(msg_byte).decode()
                print(msg)
            except ValueError:
                print("something got wrong")
                logging.warning("got wrong msg/ protcol form server, check test = {}".format(check_test))

    except ValueError:
        logging.error("value Error")
    except IndexError:
        logging.error("IndexError")
    except TypeError:
        logging.warning("got wrong msg/ protcol form server")
    except Exception as Ex:
        logging.error(Ex)
        pass

#    ## Flask

#   app = Flask(__name__)

#    @app.route("/")
#   def index():
#        #return "hello world"
#        return render_template("index.html")

#    if __name__ == "__main__":
#        app.run(debug = True, port = 80)
