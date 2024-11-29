import scapy.all as scapy
from scapy.all import sniff, wrpcap, get_if_list
from termcolor import colored
import os

# Lista per salvare i pacchetti
captured_packets = []

# Funzione per filtro avanzato, per monitorare un socket specifico
def advanced_filter(packet, ip_src=None, ip_dst=None, port=None, packet_type=None):
    if packet.haslayer(scapy.IP):
        # Filtro IP di origine e destinazione
        if ip_src and packet[scapy.IP].src != ip_src:
            return False
        if ip_dst and packet[scapy.IP].dst != ip_dst:
            return False
        # Filtro per il traffico su una porta specifica (TCP o UDP)
        if port:
            if packet.haslayer(scapy.TCP) and packet[scapy.TCP].sport != port and packet[scapy.TCP].dport != port:
                return False
            if packet.haslayer(scapy.UDP) and packet[scapy.UDP].sport != port and packet[scapy.UDP].dport != port:
                return False
    if packet_type:
        if packet_type == 'TCP' and not packet.haslayer(scapy.TCP):
            return False
        elif packet_type == 'UDP' and not packet.haslayer(scapy.UDP):
            return False
        elif packet_type == 'IP' and not packet.haslayer(scapy.IP):
            return False
    return True

# Funzione di callback per l'analisi dei pacchetti
def packet_callback(packet, ip_src=None, ip_dst=None, port=None, packet_type=None):
    """Cattura i pacchetti e filtra quelli relativi al socket specificato."""
    if advanced_filter(packet, ip_src, ip_dst, port, packet_type):
        print(colored(f"[INFO] Pacchetto catturato: {packet.summary()}", 'blue'))
        captured_packets.append(packet)  # Aggiungi il pacchetto alla lista

# Funzione di cattura dei pacchetti
def capture_packets(iface="eth0", timeout=60, ip_src=None, ip_dst=None, port=None, packet_type=None, save_file=None):
    """Inizia a catturare pacchetti sulla rete."""
    print(colored(f"[INFO] Inizio cattura pacchetti su {iface}...", 'magenta'))
    sniff(prn=lambda pkt: packet_callback(pkt, ip_src, ip_dst, port, packet_type), store=0, timeout=timeout, iface=iface)

    # Salvataggio dei pacchetti in un file PCAP se richiesto
    if save_file:
        print(colored(f"[INFO] Salvataggio pacchetti nel file: {save_file}.pcap", 'green'))
        wrpcap(save_file, captured_packets)

# Funzione per scegliere l'interfaccia di rete
def choose_interface():
    """Permette all'utente di scegliere l'interfaccia di rete per la cattura."""
    interfaces = get_if_list()  # Ottiene tutte le interfacce di rete disponibili
    print(colored("\n[INFO] Scegli l'interfaccia di rete:", 'yellow'))
    for i, iface in enumerate(interfaces, 1):
        print(colored(f"{i}. {iface}", 'cyan'))
    choice = int(input(colored("\nInserisci il numero della tua scelta: ", 'yellow')))
    if 1 <= choice <= len(interfaces):
        return interfaces[choice - 1]
    else:
        print(colored("[ERRORE] Scelta non valida. Verrà utilizzata l'interfaccia di default eth0.", 'red'))
        return "eth0"

# Menu di scelta del tipo di pacchetto
def get_packet_type_choice():
    """Fai scegliere all'utente il tipo di pacchetto da catturare."""
    print(colored("\n[INFO] Scegli il tipo di pacchetto da catturare:", 'yellow'))
    print(colored("1. TCP", 'cyan'))
    print(colored("2. UDP", 'cyan'))
    print(colored("3. IP", 'cyan'))
    print(colored("4. Tutti i pacchetti (TCP, UDP, IP)", 'cyan'))
    choice = input(colored("\nInserisci il numero della tua scelta (1/2/3/4): ", 'yellow'))

    if choice == '1':
        return 'TCP'
    elif choice == '2':
        return 'UDP'
    elif choice == '3':
        return 'IP'
    elif choice == '4':
        return None 
    else:
        print(colored("[ERRORE] Scelta non valida. Verranno catturati tutti i pacchetti.", 'red'))
        return None

# Main
if __name__ == "__main__":
    iface = choose_interface()  
    timeout = 60  # Tempo di cattura
    
    # Chiedi all'utente IP di origine, IP di destinazione e porta
    ip_src = input(colored("Inserisci l'IP di origine (lascia vuoto per tutti): ", 'yellow')) or None
    ip_dst = input(colored("Inserisci l'IP di destinazione (lascia vuoto per tutti): ", 'yellow')) or None
    port = input(colored("Inserisci la porta (lascia vuoto per tutte): ", 'yellow')) or None
    port = int(port) if port else None
    
    # Scelta del tipo di pacchetto
    packet_type = get_packet_type_choice()
    
    # Chiede all'utente se salvare i pacchetti in un file
    save_choice = input(colored("\nVuoi salvare i pacchetti catturati in un file PCAP? (sì/no): ", 'yellow'))
    if save_choice.lower() == 'sì':
        save_file = input(colored("Inserisci il nome del file (senza estensione): ", 'yellow')) + ".pcap"
    else:
        save_file = None

    # Inizia la cattura dei pacchetti
    capture_packets(iface, timeout, ip_src, ip_dst, port, packet_type, save_file)