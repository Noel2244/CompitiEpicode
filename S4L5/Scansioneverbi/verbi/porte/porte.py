import requests
from typing import Dict, Optional
from requests.exceptions import RequestException, Timeout
import time
from datetime import datetime
import threading
import sys
import socket


def mostra_animazione(testo: str, intervallo: float, stop_event: threading.Event):
    lunghezza = len(testo)
    while not stop_event.is_set():
        for i in range(lunghezza):
            if stop_event.is_set():
                break
            animato = "".join(
                char.upper() if j == i else char.lower() for j, char in enumerate(testo)
            )
            sys.stdout.write(f"\r{animato}")
            sys.stdout.flush()
            time.sleep(intervallo)
    sys.stdout.write("\r" + " " * len(testo) + "\r")


class TestHTTP:
    def __init__(self, timeout: int = 2):
        self.timeout = timeout
        self.intestazioni = {
            'User-Agent': 'Tester-Metodi-HTTP/1.0',
            'Accept': 'application/json',
        }

    def prova_metodo(self, metodo: str, url: str, dati: Optional[Dict] = None) -> Dict:
        inizio_tempo = time.time()
        risultato = {
            'metodo': metodo,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'successo': False,
            'codice_stato': None,
            'tempo_risposta_ms': None,
            'intestazioni_risposta': None,
            'errore': None
        }

        try:
            risposta = requests.request(
                method=metodo,
                url=url,
                headers=self.intestazioni,
                json=dati if dati else None,
                timeout=self.timeout
            )
            risultato.update({
                'successo': risposta.status_code < 400,
                'codice_stato': risposta.status_code,
                'tempo_risposta_ms': round((time.time() - inizio_tempo) * 1000, 2),
                'intestazioni_risposta': dict(risposta.headers),
                'lunghezza_contenuto': len(risposta.content),
                'tipo_contenuto': risposta.headers.get('content-type', 'Non specificato')
            })
        except Timeout:
            risultato['errore'] = f"Timeout dopo {self.timeout} secondi"
        except RequestException as e:
            risultato['errore'] = str(e)

        return risultato

    def prova_tutti_metodi(self, url: str) -> Dict:
        urls = []
        if not url.startswith(('http://', 'https://')):
            urls.append(f"http://{url}")
            urls.append(f"https://{url}")
        else:
            urls.append(url)

        risultati = {
            'url_testati': urls,
            'timestamp': datetime.now().isoformat(),
            'test': {}
        }

        for test_url in urls:
            risultati['test'][test_url] = {}
            metodi = {
                'GET': None,
                'POST': {'chiave_test': 'valore_test'},
                'PUT': {'chiave_test': 'valore_test'},
                'DELETE': None,
                'HEAD': None,
                'OPTIONS': None,
                'PATCH': {'chiave_test': 'valore_test'}
            }

            for metodo, dati in metodi.items():
                risultato = self.prova_metodo(metodo=metodo, url=test_url, dati=dati)
                risultati['test'][test_url][metodo] = risultato

        return risultati


def stampa_risultati_http(risultati: Dict):
    print("\n Risultati dei Test HTTP ")
    print(f"URL Testati: {', '.join(risultati['url_testati'])}")
    print(f"Timestamp: {risultati['timestamp']}")
    print("\nRiepilogo:")

    totale_test = 0
    totale_successi = 0
    totale_fallimenti = 0

    for test_url, metodi in risultati['test'].items():
        for metodo, risultato in metodi.items():
            totale_test += 1
            if risultato['successo']:
                totale_successi += 1
            else:
                totale_fallimenti += 1

    print(f"Totale Test Eseguiti: {totale_test}")
    print(f"Test Riusciti: {totale_successi}")
    print(f"Test Falliti: {totale_fallimenti}")
    print("\nDettaglio Test:")

    errori_presenti = False

    for test_url, metodi in risultati['test'].items():
        print(f"\nRisultati per {test_url}:")
        for metodo, risultato in metodi.items():
            print(f"\nTest {metodo}:")
            print(f"  Codice Stato: {risultato['codice_stato']}")
            print(f"  Tempo di Risposta: {risultato['tempo_risposta_ms']}ms")
            if risultato['intestazioni_risposta']:
                print(f"  Tipo Contenuto: {risultato['tipo_contenuto']}")
                print(f"  Lunghezza Contenuto: {risultato['lunghezza_contenuto']} byte")
            if risultato['errore']:
                errori_presenti = True

    if errori_presenti:
        mostra_errori = input("Vuoi visualizzare gli errori? (s/n): ").strip().lower()
        if mostra_errori in ['s', 'si', 'sÃ¬', 'y', 'yes']:
            for test_url, metodi in risultati['test'].items():
                for metodo, risultato in metodi.items():
                    if risultato['errore']:
                        print(f"\nErrore nel test {metodo} su {test_url}: {risultato['errore']}")


def scansiona_porte(target, porta_inizio=1, porta_fine=1024):
    print(f"\nInizio scansione del dispositivo: {target}")
    print(f"Scansione porte da {porta_inizio} a {porta_fine}")
    print(f"Tempo di inizio: {datetime.now()}")
    print("-" * 50)
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Errore: Nome host non valido.")
        return
    print(f"Indirizzo IP del target: {target_ip}\n")
    for porta in range(porta_inizio, porta_fine + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        risultato = s.connect_ex((target_ip, porta))
        if risultato == 0:
            print(f"Porta {porta}: APERTA")
        s.close()
    print("\nScansione completata.")
    print(f"Tempo di fine: {datetime.now()}")
    print("-" * 50)


def main():
    while True:
        print("\nCosa vuoi fare?")
        print("1: Test verbi HTTP")
        print("2: Scansione porte")
        print("Scrivi 'esci' per terminare il programma.")
        scelta = input("(1/2): ").strip()
        if scelta.lower() == 'esci':
            print("Uscita dal programma.")
            break

        if scelta == '1':
            print("\nTester Metodi HTTP")
            print("-" * 50)
            url = input("\nInserisci l'URL da testare (es. esempio.com o http://esempio.com): \n").strip()
            print("\n")

            stop_event = threading.Event()
            animazione_thread = threading.Thread(
                target=mostra_animazione, args=("Theta", 0.5, stop_event)
            )
            animazione_thread.start()
            tester = TestHTTP(timeout=2)
            try:
                risultati = tester.prova_tutti_metodi(url)
            finally:
                stop_event.set()
                animazione_thread.join()
            stampa_risultati_http(risultati)
        elif scelta == '2':
            print("\nScanner di Porte")
            print("-" * 50)
            target = input("Inserisci il nome host o l'indirizzo IP del dispositivo da scansionare: ").strip()
            try:
                porta_inizio = int(input("Inserisci la porta di inizio (default: 1): ") or "1")
                porta_fine = int(input("Inserisci la porta di fine (default: 1024): ") or "1024")
            except ValueError:
                print("Errore: Inserire numeri validi per le porte.")
                continue
            if porta_inizio < 1 or porta_fine > 65535 or porta_inizio > porta_fine:
                print("Errore: Range di porte non valido. (1-65535)")
                continue
            scansiona_porte(target, porta_inizio, porta_fine)
        else:
            print("Scelta non valida. Riprova.")


if __name__ == "__main__":
    main()