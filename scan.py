import pyfiglet
import sys
import socket
import multiprocessing
import json
import argparse

def main():
    # Printa os banners
    ascii_banner = pyfiglet.figlet_format("JOHNNY'S")
    print(ascii_banner)
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)

    # Configura o argparse para gerenciar os argumentos de linha de comando
    parser = argparse.ArgumentParser(description="A simple port scanner")
    parser.add_argument('--host', type=str, required=True, help='IP or hostname to scan')
    parser.add_argument('--port', type=int, nargs=2, metavar=('start_port', 'end_port'), 
                        help='Range of ports to scan. If not provided, the scanner will scan the main ports')
    args = parser.parse_args()

    target = args.host

    # Se não for um IP, tenta resolver o hostname
    if not target.isnumeric():
        try:
            target = socket.gethostbyname(target)    
        except socket.gaierror:
            print("\n Hostname could not be resolved. Exiting")
            sys.exit()
    
    print("Scanning Target: " + target)
    print("-=" * 10 + '\n')
    
    if args.port:
        start_port, end_port = args.port
    else:
        start_port, end_port = None, None

    try:
        # Usando o máximo de núcleos disponíveis para acelerar o processo
        with multiprocessing.Manager() as manager:
            closed_ports = manager.list()  # Guarda uma lista das portas fechadas
            
            num_processos = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=num_processos)

            # Checa as portas principais ou não dependendo do argumento do usuário
            if start_port is None:
                for port in MAIN_PORTS:
                    pool.apply_async(scan_port, args=(target, int(port), closed_ports))
            else:
                for port in range(start_port, end_port + 1):
                    pool.apply_async(scan_port, args=(target, port, closed_ports))

            # Fecha e espera os resultados
            pool.close()
            pool.join()

            # Printa tudo
            if closed_ports:
                print("\nClosed Ports:")
                print(", ".join(str(port) for port in closed_ports))
            else:
                print("No closed ports found.")

    except KeyboardInterrupt:
        print("\n Exiting Program")
        sys.exit()


def read_main_ports():
    with open("main_ports.json", "r") as f:
        return json.load(f)


def scan_port(target, port, closed_ports):
    try:
        # Cria a conexão com timeout
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        # Tenta conectar e analisa o resultado
        result = s.connect_ex((target, port))
        if result == 0:
            service = MAIN_PORTS.get(str(port), "Unknown Service")
            print(f"Port {port} is open. Service: {service}")
        else:
            closed_ports.append(port)  # Coloca na lista de portas fechadas
        s.close()
    except socket.timeout:
        print(f"Timeout occurred for port: {port}")
    except socket.error:
        print(f"\n Server not responding for port: {port}")
    finally:
        s.close()

if __name__ == "__main__":
    MAIN_PORTS = read_main_ports()
    main()
