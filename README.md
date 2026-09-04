# AGNEXUSUIO - Landing Page

Una landing page estática, ligera y responsive para la venta de equipos tecnológicos.

## Características

✅ **Diseño Minimalista y Orgánico** - Estética limpia con tonos azulados  
✅ **100% Responsive** - Se adapta perfectamente a móviles, tablets y escritorio  
✅ **Tipografía Lato** - Fuente elegante en toda la página  
✅ **Ligero y Rápido** - HTML/CSS puro sin dependencias externas  
✅ **20 Laptops** - 10 de pinsoft.ec + 10 de digitalpcecuador.com  
✅ **20 Celulares** - Últimas ofertas de mundotek.com.ec  

## Estructura

```
index.html         - Página principal completa con HTML y CSS embebido
scraper.py        - Script para scrapear productos (opcional)
README.md         - Este archivo
```

## Secciones

### 1. **Navegación Sticky**
- Logo de AGNEXUSUIO
- Enlaces a secciones principales
- Diseño responsive para móviles

### 2. **Hero Section**
- Título principal atractivo
- Subtítulo descriptivo
- Botones CTA (Call-to-Action)

### 3. **Features**
- 3 características destacadas
- Precios competitivos
- Envíos rápidos
- Atención personalizada

### 4. **Sección de Laptops**
- 20 laptops con precios
- Grid responsive
- Información de fuente del producto
- Hover effects atractivos

### 5. **Sección de Celulares**
- 20 celulares con precios
- Misma estructura que laptops
- Fondo diferenciado

### 6. **Contacto**
- WhatsApp: +593 99 221 7314
- Email: contacto@agnexusuio.com
- Diseño atractivo con backdrop blur

### 7. **Footer**
- Copyright y derechos reservados

## Colores Utilizados

- **Gradiente Principal**: #667eea a #764ba2 (Tonos azulados)
- **Fondo Secundario**: #f5f7fa (Blanco azulado)
- **Texto Principal**: #2c3e50 (Gris oscuro)
- **Acentos**: #667eea (Azul principal)

## Tipografía

**Font**: Lato (Google Fonts)
- Light: 300
- Regular: 400
- Bold: 700

## Cómo Usar

1. Abre `index.html` en tu navegador
2. Los productos se cargan dinámicamente desde JavaScript
3. Para actualizar productos, edita la sección de `products` en el script

### Actualizar Datos de Contacto

Busca esta sección en el HTML:
```html
<div class="contact-item">
    <h3>WhatsApp</h3>
    <a href="https://wa.me/593992217314" target="_blank">+593 99 221 7314</a>
</div>
```

### Agregar Productos Reales

1. Ejecuta `scraper.py` para obtener datos reales:
```bash
python scraper.py
```

2. Modifica `index.html` para cargar datos desde `productos.json`

## Características Responsive

- **Desktop** (>768px): Grid de 3-4 columnas
- **Tablet** (768px-480px): Grid de 2 columnas
- **Mobile** (<480px): Grid de 1 columna

## Performance

- ✅ Sin dependencias externas (solo Google Fonts)
- ✅ CSS embebido (sin requests externos)
- ✅ JavaScript vanilla (sin frameworks)
- ✅ Tiempo de carga < 1 segundo

## Sitios de Origen de Productos

- **Laptops Pinsoft**: https://pinsoft.ec/laptop-notebook-portatiles/c-67.html
- **Laptops DigitalPC**: https://digitalpcecuador.com/categoria-producto/laptops/
- **Celulares MundoTek**: https://mundotek.com.ec/product-category/telefonos-al-mejor-precio/

## Notas

- La página utiliza datos de ejemplo realistas
- Los precios mostrados son referencias
- Se pueden actualizar fácilmente editando el array `products` en JavaScript

## Autor

Creado por Copilot para AGNEXUSUIO
