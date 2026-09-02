import os
import re
import json
import math
import hashlib
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

OUTPUT_JSON = "productos.json"
IMAGE_DIR = "imagenes"
os.makedirs(IMAGE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
}

# Configuración con parámetros de menor precio garantizado
FUENTES = [
    {
        "nombre": "Pinsoft",
        "base": "https://www.pinsoft.ec",
        "categoria": "Laptops",
        "url_base": "https://www.pinsoft.ec/laptop-notebook-portatiles/c-67.html",
        "cantidad": 10,
        "tipo": "pinsoft"
    },
    {
        "nombre": "DigitalPC",
        "base": "https://digitalpcecuador.com",
        "categoria": "Laptops",
        "url_base": "https://digitalpcecuador.com/categoria-producto/laptops/",
        "cantidad": 10,
        "tipo": "wordpress"
    },
    {
        "nombre": "MundoTek",
        "base": "https://mundotek.com.ec",
        "categoria": "Celulares",
        "url_base": "https://mundotek.com.ec/product-category/telefonos-al-mejor-precio/",
        "cantidad": 20,
        "tipo": "wordpress"
    }
]

def limpiar_texto(texto):
    if not texto:
        return ""
    texto = BeautifulSoup(texto, "html.parser").get_text(" ", strip=True)
    return re.sub(r"\s+", " ", texto).strip()

def extraer_precio(texto):
    if not texto:
        return None
    texto = texto.replace(",", "")
    patrones = [r"\$\s*(\d+(?:\.\d{1,2})?)", r"(\d+(?:\.\d{1,2})?)\s*(?:USD|US\$)"]
    valores = []
    for patron in patrones:
        encontrados = re.findall(patron, texto, re.I)
        for valor in encontrados:
            try:
                num = float(valor)
                if num > 0:
                    valores.append(num)
            except Exception:
                pass
    return min(valores) if valores else None

def precio_final(precio):
    if precio is None:
        return None
    # Regla: < $200 aumenta 60% | >= $200 aumenta 40% y redondea a la decena superior
    if precio < 200:
        resultado = precio * 1.60
    else:
        resultado = precio * 1.40
    return int(math.ceil(resultado / 10) * 10)

def nombre_archivo_seguro(texto):
    texto = re.sub(r'[<>:"/\\|?*]', "", texto)
    return re.sub(r"\s+", "_", texto)[:45].strip("_")

def resolver_url(url, base):
    if not url:
        return None
    url = url.strip()
    if url.startswith("//"):
        return "https:" + url
    return urljoin(base, url)

def es_imagen_valida(url):
    if not url or url.lower().startswith("data:"):
        return False
    url_lower = url.lower()
    basura = ["logo", "whatsapp", "icon", "payment", "placeholder", "avatar", "blank.gif", "loader"]
    if any(b in url_lower for b in basura):
        return False
    return any(ext in url_lower for ext in [".jpg", ".jpeg", ".png", ".webp", ".avif"]) or "wp-content/uploads" in url_lower or "getimage/" in url_lower

def extraer_imagen_desde_tag(img, base_url):
    if not img:
        return None
    srcset = img.get("data-srcset") or img.get("srcset") or img.get("data-lazy-srcset")
    if srcset:
        partes = [p.strip() for p in srcset.split(",") if p.strip()]
        if partes:
            url = resolver_url(partes[-1].split(" ")[0], base_url)
            if es_imagen_valida(url):
                return url
    for attr in ["data-large_image", "data-zoom-image", "data-high-res-img", "data-lazy-src", "data-src", "data-original", "src"]:
        val = img.get(attr)
        if val:
            url = resolver_url(val, base_url)
            if es_imagen_valida(url):
                return url
    return None

def obtener_imagen_ficha_producto(html, base):
    soup = BeautifulSoup(html, "html.parser")
    selectores = [
        ".woocommerce-product-gallery__image img",
        ".product-images img.wp-post-image",
        ".product-info .image img",
        "#default-image img",
        "#main-image",
        ".main-image img",
        ".product-detail-image img"
    ]
    for selector in selectores:
        img = soup.select_one(selector)
        if img:
            url = extraer_imagen_desde_tag(img, base)
            if url:
                return url
    for meta in soup.find_all("meta"):
        prop = (meta.get("property") or meta.get("name") or "").lower()
        if prop in ["og:image", "og:image:secure_url", "twitter:image"]:
            val = meta.get("content")
            if val:
                url = resolver_url(val, base)
                if es_imagen_valida(url):
                    return url
    return None

def descargar_imagen(url, referer, ruta_base):
    headers = HEADERS.copy()
    headers["Referer"] = referer
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200 and len(res.content) > 1000:
            from PIL import Image
            from io import BytesIO
            img = Image.open(BytesIO(res.content)).convert("RGB")
            ruta = ruta_base + ".webp"
            img.save(ruta, "WEBP", quality=88, method=6)
            return ruta.replace("\\", "/")
    except Exception:
        pass
    return None

def recolectar_pinsoft(page, fuente):
    print("\n[Pinsoft] Buscando laptops más económicas...")
    productos = []
    for pagina in range(1, 10):
        url = f"{fuente['url_base']}?sort=p.price&order=ASC" if pagina == 1 else f"{fuente['url_base']}/{pagina}/?sort=p.price&order=ASC"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=35000)
            page.wait_for_timeout(1500)
            soup = BeautifulSoup(page.content(), "html.parser")
            items = soup.select(".product-layout, .product-thumb, .product-grid .product, div[class*='product-']")
            if not items:
                enlaces = soup.find_all("a", href=True)
                items = [a.parent for a in enlaces if "/p-" in a.get("href") or "/p/" in a.get("href")]

            encontrados_pag = 0
            for item in items:
                link = item.select_one("a[href*='/p-'], a[href*='/p/']") or item.select_one("a[href]")
                if not link:
                    continue
                href = resolver_url(link.get("href"), fuente["base"])
                if any(x in href.lower() for x in ["/brands", "/cart", "/login", "/account"]):
                    continue

                texto = limpiar_texto(item.get_text(" ", strip=True))
                precio = extraer_precio(texto)
                if not precio or precio < 120:  # Filtra cables o repuestos
                    continue

                nombre_el = item.select_one(".name a, .caption h4 a, h4, h3, h2") or link
                nombre = limpiar_texto(nombre_el.get_text(" ", strip=True))
                if len(nombre) < 15:
                    nombre = texto.split("$")[0].strip()
                if len(nombre) < 15:
                    continue

                if not any(p["url_origen"] == href for p in productos):
                    productos.append({
                        "nombre": nombre,
                        "precio_original": precio,
                        "url_origen": href,
                        "fuente": fuente["nombre"],
                        "categoria": fuente["categoria"]
                    })
                    encontrados_pag += 1

            if encontrados_pag == 0 and pagina > 1:
                break
        except Exception as e:
            print(f"Fin en página {pagina}: {e}")
            break
    return productos

def recolectar_wordpress(page, fuente):
    print(f"\n[{fuente['nombre']}] Buscando productos más económicos...")
    productos = []
    for pagina in range(1, 15):
        url = f"{fuente['url_base']}?orderby=price" if pagina == 1 else f"{fuente['url_base']}page/{pagina}/?orderby=price"
        try:
            page.goto(url, wait_until="networkidle", timeout=35000)
            page.wait_for_timeout(1500)
            soup = BeautifulSoup(page.content(), "html.parser")
            tarjetas = soup.select("li.product, article.product, div.product-small, .product")
            encontrados_pag = 0

            for tarjeta in tarjetas:
                nombre_el = tarjeta.select_one(".woocommerce-loop-product__title, .product-title, h2, h3")
                if not nombre_el:
                    continue
                nombre = limpiar_texto(nombre_el.get_text(" ", strip=True))
                if len(nombre) < 3:
                    continue

                precio_el = tarjeta.select_one(".price")
                if not precio_el:
                    continue
                precio = extraer_precio(precio_el.get_text(" ", strip=True))
                if precio is None or precio < 40:  # Filtra accesorios o micas
                    continue

                enlace = tarjeta.select_one("a.woocommerce-LoopProduct-link, a.woocommerce-loop-product__link, .product-title a, a[href*='/producto/'], a[href*='/product/'], a[href]")
                if not enlace:
                    continue
                href = resolver_url(enlace.get("href"), fuente["base"])

                if not any(p["url_origen"] == href for p in productos):
                    productos.append({
                        "nombre": nombre,
                        "precio_original": precio,
                        "url_origen": href,
                        "fuente": fuente["nombre"],
                        "categoria": fuente["categoria"]
                    })
                    encontrados_pag += 1

            if encontrados_pag == 0 or len(productos) >= fuente["cantidad"] * 3:
                break
        except Exception as e:
            print(f"Fin en página {pagina}: {e}")
            break
    return productos

def extraer_caracteristicas(nombre):
    partes = re.split(r"\s*/\s*|\s*-\s*", nombre)
    caracteristicas = [limpiar_texto(p) for p in partes if len(limpiar_texto(p)) >= 3 and limpiar_texto(p).lower() != nombre.lower()]
    if len(caracteristicas) < 4:
        tokens = re.split(r"\s+(?=Intel|AMD|Ryzen|Core|RAM|GB|SSD|NVMe|RTX|Windows|Android|5G|4G|Wi-Fi|\d{2,3}[\"”])", nombre, flags=re.I)
        for t in tokens:
            t = limpiar_texto(t)
            if len(t) >= 3 and t not in caracteristicas:
                caracteristicas.append(t)
            if len(caracteristicas) >= 4:
                break
    return caracteristicas[:4] if caracteristicas else ["Garantía técnica local", "Disponibilidad inmediata", "Envío a nivel nacional", "Equipo homologado"]

def main():
    todos_seleccionados = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"])
        context = browser.new_context(user_agent=HEADERS["User-Agent"], viewport={"width": 1440, "height": 900}, locale="es-EC")
        page = context.new_page()

        for fuente in FUENTES:
            if fuente["tipo"] == "pinsoft":
                recolectados = recolectar_pinsoft(page, fuente)
            else:
                recolectados = recolectar_wordpress(page, fuente)

            # Ordenar estrictamente de menor a mayor precio
            recolectados = sorted(recolectados, key=lambda x: x["precio_original"])
            seleccionados = recolectados[:fuente["cantidad"]]
            print(f"\n>> {fuente['nombre']}: {len(seleccionados)} productos más económicos listos.")

            for idx, prod in enumerate(seleccionados, 1):
                print(f"  [{idx:02d}] {prod['nombre']} | Base: ${prod['precio_original']:.2f}")
                try:
                    page.goto(prod["url_origen"], wait_until="domcontentloaded", timeout=25000)
                    page.wait_for_timeout(1000)
                    img_url = obtener_imagen_ficha_producto(page.content(), fuente["base"])
                except Exception:
                    img_url = None

                ruta_relativa = None
                if img_url:
                    slug = nombre_archivo_seguro(prod["nombre"])
                    hash_id = hashlib.md5(prod["url_origen"].encode()).hexdigest()[:6]
                    base_name = os.path.join(IMAGE_DIR, f"{fuente['nombre']}_{idx:02d}_{hash_id}_{slug}")
                    ruta_relativa = descargar_imagen(img_url, prod["url_origen"], base_name)

                prod["imagen"] = ruta_relativa
                prod["precio_final"] = precio_final(prod["precio_original"])
                prod["caracteristicas"] = extraer_caracteristicas(prod["nombre"])
                todos_seleccionados.append(prod)

        browser.close()

    # Formateo estricto del JSON: No expone nombres de origen
    salida = [
        {
            "nombre": p["nombre"],
            "precio": p["precio_final"],
            "categoria": p["categoria"],
            "caracteristicas": p["caracteristicas"],
            "imagen": p["imagen"]
        }
        for p in todos_seleccionados
    ]

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"✓ Catálogo generado: {len(salida)} productos.")
    print(f"✓ Archivo guardado: {OUTPUT_JSON}")
    print("=" * 60)

if __name__ == "__main__":
    main()
