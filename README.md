
# Port Scanner

Este scanner de portas TCP em Python permite que você escaneie um intervalo de portas ou as "Well-Known Ports" em um host especificado. Ele retorna se a porta está aberta ou fechada e fornece uma breve descrição do serviço associado à porta (para as conhecidas).

## Funcionalidades

- Escanear uma única porta ou um intervalo de portas (tanto para um IP de host/rede quanto para uma URL).
- Exibir o status de cada porta (aberta/fechada).
- Identificar o serviço associado a uma porta se ela for conhecida.

## Pré-requisitos

- Python 3.x
- As dependências estão listadas no `requirements.txt`.

## Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/JoaoLucasMBC/port-scanner.git
   cd port-scanner
   ```

2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

## Como Utilizar

### Executando o Port Scan

Para executar o scanner, use o seguinte comando:

```bash
python scan.py <host> <flags>
```

### Opções

- **Escanear Portas Conhecidas**: Escaneie as portas mais conhecidas de um host.
- **Escanear Intervalo de Portas**: Escaneie um intervalo de portas em um host.

### Exemplos de Comandos

- **Escanear as portas conhecidas**:

  ```bash
  python scan.py -h <nome_do_host_ou_ip>
  ```

- **Escanear um intervalo de portas**:

  ```bash
  python scan.py -h <nome_do_host_ou_ip> -p <porta_inicial> <porta_final>
  ```

### Script de Portas Bem Conhecidas

Além do serviço, você pode encontrar o script `well-known-ports.py`, que gera uma lista de portas bem conhecidas e os serviços relacionados, como fonte na Wikipedia. Ele pode ser usado para criar o `main_ports.json`, que contém a relação entre as portas mais conhecidas e os seus serviços usuais.

## Fontes

* [Base de como Scannear Portas](https://www.geeksforgeeks.org/port-scanner-using-python/)  
* [Base de como criar um programa com argumentos para a tarefa](https://github.com/filipe1417/python-portscan-rapido)  
* [Lista das portas mais conhecidas e seus serviços](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers)