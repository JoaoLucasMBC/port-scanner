import pyfiglet
import sys
import socket
import multiprocessing
import json

def main():
    ascii_banner = pyfiglet.figlet_format("JOHNNY'S")
    print(ascii_banner)
    ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
    print(ascii_banner)

    if len(sys.argv) > 4 or len(sys.argv) < 2:
        print("Invalid arguments")
        print("Usage: python3 scan.py <ip/host> <start_port> <end_port>")
        sys.exit()
    
    target = sys.argv[1]

    if not target.isnumeric():
        try:
            target = socket.gethostbyname(target)    
        except socket.gaierror:
            print("\n Hostname couldn't be resolved. Check the target or try again later.")
            sys.exit()
    
    print("Scanning Target: " + target)

    print("-=" * 10 + '\n')
    
    if len(sys.argv) == 2:
        start_port = None
        end_port = None
    else:
        start_port = int(sys.argv[2])
        end_port = int(sys.argv[3])

    try:
        # Create a multiprocessing manager to share data between processes
        with multiprocessing.Manager() as manager:
            closed_ports = manager.list()  # Shared list to store closed ports
            
            num_processos = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes=num_processos)

            # Check if the user provided a port range
            if start_port is None:
                for port in MAIN_PORTS:
                    pool.apply_async(scan_port, args=(target, int(port), closed_ports))
            else:
                for port in range(start_port, end_port+1):
                    pool.apply_async(scan_port, args=(target, port, closed_ports))

            pool.close()
            pool.join()

            # Print all closed ports at once
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            service = MAIN_PORTS.get(str(port), "Unknown Service")
            print(f"Port {port} is open. Service: {service}")
        else:
            closed_ports.append(port)  # Append closed port to the shared list
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
