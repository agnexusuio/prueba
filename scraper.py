import os
import re
import json
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# ============================================================
# CONFIGURACIÓN
# ============================================================

OUTPUT_JSON = "productos.json"
IMAGE_DIR = "imagenes"

os.makedirs(IMAGE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
}

# ============================================================
# UTILIDADES
# ============================================================

def limpiar_texto(texto):
    if not texto:
        return ""
    texto = BeautifulSoup(texto, "html.parser").get_text(" ", strip=True)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def extraer_precio(texto):
    if not texto:
        return None
    
    texto = str(texto).replace(",", "").replace("$", "").strip()
    patrones = [
        r"(\d+(?:\.\d{1,2})?)",
    ]
    
    for patron in patrones:
        encontrados = re.findall(patron, texto, re.I)
        for valor in encontrados:
            try:
                numero = float(valor)
                if numero > 0:
                    return numero
            except:
                pass
    return None

# ============================================================
# EXTRACCIÓN POR FUENTE
# ============================================================

def scrape_pinsoft_laptops():
    """Scrape 10 laptops económicas de pinsoft.ec"""
    print("\n[PINSOFT] Iniciando extracción...")
    url = "https://pinsoft.ec/laptop-notebook-portatiles/c-67.html"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        laptops = []
        
        # Buscar productos con diferentes selectores
        productos = soup.find_all('div', class_=re.compile(r'product|item', re.I))
        
        print(f"[PINSOFT] Encontrados {len(productos)} items en HTML")
        
        for product in productos[:15]:
            try:
                # Obtener nombre
                nombre_elem = (
                    product.find('h2') or 
                    product.find('h3') or 
                    product.find('a', class_=re.compile(r'product|link', re.I))
                )
                
                # Obtener precio
                precio_elem = product.find('span', class_=re.compile(r'price', re.I))
                
                # Obtener URL
                url_elem = product.find('a', href=True)
                
                if nombre_elem and precio_elem:
                    nombre = limpiar_texto(nombre_elem.get_text())
                    precio_str = limpiar_texto(precio_elem.get_text())
                    precio = extraer_precio(precio_str)
                    url_producto = urljoin("https://pinsoft.ec", url_elem['href']) if url_elem else url
                    
                    if nombre and precio:
                        laptops.append({
                            "nombre": nombre,
                            "precio_original": precio,
                            "categoria": "Laptop",
                            "url_origen": url_producto,
                            "imagen": None
                        })
                        print(f"  ✓ {nombre[:50]}... - ${precio:.2f}")
            except Exception as e:
                pass
        
        print(f"[PINSOFT] Productos extraídos: {len(laptops)}")
        return laptops[:10]
        
    except Exception as e:
        print(f"[PINSOFT] Error: {e}")
        return []

def scrape_digitalpc_laptops():
    """Scrape 10 laptops económicas de digitalpcecuador.com (WordPress)"""
    print("\n[DIGITALPC] Iniciando extracción...")
    url = "https://digitalpcecuador.com/categoria-producto/laptops/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        laptops = []
        
        # Selectores típicos de WooCommerce/WordPress
        productos = soup.find_all('div', class_=re.compile(r'product|woo', re.I))
        
        print(f"[DIGITALPC] Encontrados {len(productos)} items en HTML")
        
        for product in productos[:15]:
            try:
                # WooCommerce típico
                nombre_elem = (
                    product.find('h2', class_='woocommerce-loop-product__title') or
                    product.find('h3') or
                    product.find('a', class_=re.compile(r'product', re.I))
                )
                
                precio_elem = (
                    product.find('span', class_='woocommerce-Price-amount') or
                    product.find('span', class_=re.compile(r'price', re.I))
                )
                
                url_elem = product.find('a', href=re.compile(r'product', re.I))
                
                if nombre_elem and precio_elem:
                    nombre = limpiar_texto(nombre_elem.get_text())
                    precio_str = limpiar_texto(precio_elem.get_text())
                    precio = extraer_precio(precio_str)
                    url_producto = url_elem['href'] if url_elem else url
                    
                    if nombre and precio:
                        laptops.append({
                            "nombre": nombre,
                            "precio_original": precio,
                            "categoria": "Laptop",
                            "url_origen": url_producto,
                            "imagen": None
                        })
                        print(f"  ✓ {nombre[:50]}... - ${precio:.2f}")
            except Exception as e:
                pass
        
        print(f"[DIGITALPC] Productos extraídos: {len(laptops)}")
        return laptops[:10]
        
    except Exception as e:
        print(f"[DIGITALPC] Error: {e}")
        return []

def scrape_mundotek_phones():
    """Scrape 20 celulares económicos de mundotek.com.ec (WordPress)"""
    print("\n[MUNDOTEK] Iniciando extracción...")
    url = "https://mundotek.com.ec/product-category/telefonos-al-mejor-precio/"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        phones = []
        
        # Selectores típicos de WooCommerce
        productos = soup.find_all('div', class_=re.compile(r'product|woo', re.I))
        
        print(f"[MUNDOTEK] Encontrados {len(productos)} items en HTML")
        
        for product in productos[:25]:
            try:
                # WooCommerce típico
                nombre_elem = (
                    product.find('h2', class_='woocommerce-loop-product__title') or
                    product.find('h3') or
                    product.find('a', class_=re.compile(r'product', re.I))
                )
                
                precio_elem = (
                    product.find('span', class_='woocommerce-Price-amount') or
                    product.find('span', class_=re.compile(r'price', re.I))
                )
                
                url_elem = product.find('a', href=re.compile(r'product', re.I))
                
                if nombre_elem and precio_elem:
                    nombre = limpiar_texto(nombre_elem.get_text())
                    precio_str = limpiar_texto(precio_elem.get_text())
                    precio = extraer_precio(precio_str)
                    url_producto = url_elem['href'] if url_elem else url
                    
                    if nombre and precio:
                        phones.append({
                            "nombre": nombre,
                            "precio_original": precio,
                            "categoria": "Celular",
                            "url_origen": url_producto,
                            "imagen": None
                        })
                        print(f"  ✓ {nombre[:50]}... - ${precio:.2f}")
            except Exception as e:
                pass
        
        print(f"[MUNDOTEK] Productos extraídos: {len(phones)}")
        return phones[:20]
        
    except Exception as e:
        print(f"[MUNDOTEK] Error: {e}")
        return []

# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

def main():
    print("=" * 70)
    print("AGNEXUSUIO - SCRAPER DE PRODUCTOS")
    print("=" * 70)
    
    todos = []
    
    # Scraping Pinsoft Laptops
    pinsoft = scrape_pinsoft_laptops()
    todos.extend(pinsoft)
    
    time.sleep(1)
    
    # Scraping DigitalPC Laptops
    digitalpc = scrape_digitalpc_laptops()
    todos.extend(digitalpc)
    
    time.sleep(1)
    
    # Scraping MundoTek Phones
    mundotek = scrape_mundotek_phones()
    todos.extend(mundotek)
    
    # Ordenar por categoría y precio
    todos = sorted(
        todos,
        key=lambda x: (x.get("categoria", ""), x.get("precio_original", 999999))
    )
    
    # Guardar en JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETADO")
    print("=" * 70)
    print(f"✓ Total de productos: {len(todos)}")
    print(f"✓ Laptops: {len([p for p in todos if p.get('categoria') == 'Laptop'])}")
    print(f"✓ Celulares: {len([p for p in todos if p.get('categoria') == 'Celular'])}")
    print(f"✓ Archivo guardado: {OUTPUT_JSON}")
    print("=" * 70)

if __name__ == "__main__":
    main()
