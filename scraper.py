import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_pinsoft_laptops():
    """Scrape 10 laptops más económicas de pinsoft.ec"""
    url = "https://pinsoft.ec/laptop-notebook-portatiles/c-67.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        laptops = []
        products = soup.find_all('div', class_='product-item')
        
        for product in products[:10]:
            try:
                name_elem = product.find('h2', class_='product-name')
                price_elem = product.find('span', class_='product-price')
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price = price_elem.get_text(strip=True)
                    laptops.append({
                        'name': name,
                        'price': price,
                        'source': 'pinsoft.ec'
                    })
            except:
                pass
        
        return laptops[:10]
    except Exception as e:
        print(f"Error scraping pinsoft: {e}")
        return []

def scrape_digitalpc_laptops():
    """Scrape 10 laptops más económicas de digitalpcecuador.com"""
    url = "https://digitalpcecuador.com/categoria-producto/laptops/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        laptops = []
        products = soup.find_all('div', class_='product')
        
        for product in products[:10]:
            try:
                name_elem = product.find('h2') or product.find('a', class_='product-link')
                price_elem = product.find('span', class_='price') or product.find('span', class_='woocommerce-Price-amount')
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price = price_elem.get_text(strip=True)
                    laptops.append({
                        'name': name,
                        'price': price,
                        'source': 'digitalpcecuador.com'
                    })
            except:
                pass
        
        return laptops[:10]
    except Exception as e:
        print(f"Error scraping digitalpc: {e}")
        return []

def scrape_mundotek_phones():
    """Scrape 20 celulares más económicos de mundotek.com.ec"""
    url = "https://mundotek.com.ec/product-category/telefonos-al-mejor-precio/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        phones = []
        products = soup.find_all('div', class_='product')
        
        for product in products[:20]:
            try:
                name_elem = product.find('h2') or product.find('a')
                price_elem = product.find('span', class_='price') or product.find('span', class_='woocommerce-Price-amount')
                
                if name_elem and price_elem:
                    name = name_elem.get_text(strip=True)
                    price = price_elem.get_text(strip=True)
                    phones.append({
                        'name': name,
                        'price': price,
                        'source': 'mundotek.com.ec'
                    })
            except:
                pass
        
        return phones[:20]
    except Exception as e:
        print(f"Error scraping mundotek: {e}")
        return []

def main():
    print("Iniciando scraping de productos...")
    
    print("\nScraperando laptops de pinsoft...")
    pinsoft_laptops = scrape_pinsoft_laptops()
    print(f"Encontradas {len(pinsoft_laptops)} laptops en pinsoft")
    
    time.sleep(1)
    
    print("\nScraperando laptops de digitalpc...")
    digitalpc_laptops = scrape_digitalpc_laptops()
    print(f"Encontradas {len(digitalpc_laptops)} laptops en digitalpc")
    
    time.sleep(1)
    
    print("\nScraperando celulares de mundotek...")
    mundotek_phones = scrape_mundotek_phones()
    print(f"Encontrados {len(mundotek_phones)} celulares en mundotek")
    
    data = {
        'laptops_pinsoft': pinsoft_laptops,
        'laptops_digitalpc': digitalpc_laptops,
        'phones_mundotek': mundotek_phones
    }
    
    with open('productos.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\nDatos guardados en productos.json")

if __name__ == "__main__":
    main()
