import select
import socket
import time

from mycroft.util.log import LOG

clients = []


def playAudio(audio):
    LOG.info('Trying to play UDP audio')
    LOG.info(str(clients))
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # LOG.info(str(audio))
    try:
        LOG.info("Connection Status" + str(udp_socket.connect_ex(("192.168.1.5", 50006))))
        udp_socket.setblocking(0)
        send = True

        retries = 0
        while send and retries < 10:
            readable, writable, exceptional = select.select(
                [udp_socket], [udp_socket], [udp_socket])
            for s in writable:
                s.send("START{SR: " + str(audio.samplerate) + ",CH: " + str(audio.channels) + "}")
            for s in readable:
                data = s.recv(4096)
                if data:
                    if "STARTING" in str(data):
                        send = False
            time.sleep(.1)
            retries += 1
        if retries == 10:
            return
        udp_socket.setblocking(1)
        for buf in audio:
            udp_socket.sendall(buf)
        udp_socket.setblocking(0)
        send = True
        retries = 0
        # while send and retries < 10:
        #     readable, writable, exceptional = select.select(
        #         [udp_socket], [udp_socket], [udp_socket])
        #     for s in writable:
        #         s.send("END")
        #     for s in readable:
        #         data = s.recv(4096)
        #         if data:
        #             if "ENDING" in str(data):
        #                 send = False
        #     time.sleep(.3)
        #     retries += 1

        udp_socket.close()
    except socket.error as msg:
        udp_socket.close()
        LOG.error(msg)

