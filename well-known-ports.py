import requests
from bs4 import BeautifulSoup
import re

def scrape_port_services():
    print("Scraping port services from Wikipedia...")

    url = "https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    port_service_map = {}

    # Pega as tabelas da página
    tables = soup.find_all("table", {"class": "wikitable"})
    
    # Apenas as tabelas 1 e 2 contém as informações que queremos
    for table in tables[1:3]:
        rows = table.find_all("tr")
        for row in rows[1:]:  # Pula o cabecalho
            cols = row.find_all("td")
            # Se é uma linha válida
            if len(cols) >= 2:
                try:
                    # Apenas salvamos as portas que possuem um serviço associado
                    if "Yes" in cols[1].text or "Reserved" in cols[1].text:
                        port_range = cols[0].text.strip()
                        service_name = cols[-1].text.strip()
                        
                        # Remove as referências da wiki
                        cleaned_text = re.sub(r'\[.*?\]', '', service_name)
                        
                        # Salvamos a porta e o serviço associado
                        port_service_map[int(port_range)] = cleaned_text
                except:
                    continue

    return port_service_map



if __name__ == "__main__":
    port_service_map = scrape_port_services()

    for port, service in list(port_service_map.items())[:20]: 
        print(f"Port {port}: {service}")
    
    # Salve eme um arquivo JSON
    import json
    with open("main_ports.json", "w") as f:
        json.dump(port_service_map, f)
