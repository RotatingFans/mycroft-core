import socket
from mycroft.util.log import LOG

clients = []


def playAudio(audio):
    LOG.info('Trying to play UDP audio')
    LOG.info(str(clients))
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # LOG.info(str(audio))
    try:
        udp.setblocking(0)
        LOG.info("Connection Status" + str(udp.connect_ex(("192.168.1.5", 50005))))
        totalsent = 0
        udp.send("START")
        udp.send(str(audio.samplerate))
        udp.send(str(audio.channels))
        for buf in audio:
            udp.send(buf)
        udp.send("END")
        udp.close()
    except socket.error as msg:
        udp.close()
        LOG.error(msg)

