# AGNEXUSUIO - Landing Page

Una landing page estática, ligera y responsive para la venta de equipos tecnológicos con datos en tiempo real.

## Características

✅ **Diseño Minimalista y Orgánico** - Estética limpia con tonos azulados  
✅ **100% Responsive** - Se adapta perfectamente a móviles, tablets y escritorio  
✅ **Tipografía Lato** - Fuente elegante en toda la página  
✅ **Ligero y Rápido** - HTML/CSS puro sin dependencias externas  
✅ **Carga dinámmica de productos** - Desde archivo JSON  
✅ **30 Productos reales** - 10 laptops pinsoft + 10 laptops digitalpc + 20 celulares mundotek  

## 🚀 Inicio Rápido

### 1. Ver la página localmente (sin ejecutar scraper)
```bash
# Solo abre el archivo index.html en tu navegador
# Usará datos de fallback si productos.json no existe
```

### 2. Actualizar productos desde las tiendas (Opción A: Rápida)
```bash
# Instala dependencias
python -m pip install -r requirements.txt

# Ejecuta el scraper simple
python scraper.py

# Los productos se guardarán en productos.json
# Recarga la página para ver los cambios
```

## 📁 Estructura

```
index.html          - Página principal (HTML + CSS + JavaScript)
scraper.py          - Script para actualizar productos
productos.json      - Base de datos de productos (actualizada por scraper)
requirements.txt    - Dependencias de Python
imagenes/           - Carpeta de imágenes (creada por scraper avanzado)
README.md          - Este archivo
```

## 🎨 Diseño

- **Colores**: Gradiente azulado (#667eea → #764ba2)
- **Tipografía**: Lato (Google Fonts)
- **Layout**: CSS Grid responsive
- **Interactividad**: Hover effects suaves, navegación sticky

## 📱 Secciones

1. **Navegación Sticky** - Logo y menú de navegación
2. **Hero Section** - Título y CTA buttons
3. **Features** - 3 ventajas principales
4. **Laptops** - 20 laptops económicas (10 + 10)
5. **Celulares** - 20 teléfonos móviles
6. **Contacto** - WhatsApp y Email
7. **Footer** - Copyright

## 🔧 Cómo funciona

### Estructura de `productos.json`

El archivo debe ser un array de objetos con la siguiente estructura:

```json
[
  {
    "nombre": "Laptop ASUS VivoBook 15.6\" Intel Core i3",
    "precio": 299.99,
    "precio_original": 299.99,
    "categoria": "Laptop",
    "caracteristicas": ["Intel Core i3", "15.6\"", "RAM 8GB"],
    "descripcion": "Laptop económica para tareas básicas",
    "especificaciones": {"RAM": "8GB", "SSD": "256GB"},
    "disponibilidad": "En stock",
    "imagen": "nombre_imagen.webp",
    "url_origen": "https://..."
  }
]
```

### Cómo funciona el JavaScript

1. Intenta cargar `productos.json` con `fetch()`
2. Separa productos por `categoria` (Laptop vs Celular)
3. Renderiza tarjetas dinámicamente
4. Si hay error, usa datos de fallback

### Datos de Fallback

Si el archivo `productos.json` no existe o hay error:
- Muestra 10 laptops de ejemplo
- Muestra 20 celulares de ejemplo
- Todos con precios e información realista

## 📞 Datos de Contacto

- **Empresa**: AGNEXUSUIO
- **WhatsApp**: +593 99 221 7314
- **Email**: contacto@agnexusuio.com

## 🔗 Fuentes de Productos

- **Pinsoft**: https://pinsoft.ec/laptop-notebook-portatiles/c-67.html
- **DigitalPC**: https://digitalpcecuador.com/categoria-producto/laptops/
- **MundoTek**: https://mundotek.com.ec/product-category/telefonos-al-mejor-precio/

## ⚡ Performance

- Sin dependencias externas (solo Google Fonts CDN)
- Tiempo de carga < 1 segundo
- CSS embebido (no hay requests adicionales)
- JavaScript vanilla y ligero
- Responsive desde 320px

## 🛠️ Personalizaciones

### Cambiar colores

Edita estos valores en la etiqueta `<style>` de `index.html`:

```css
/* Cambiar gradiente principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* A otros colores */
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Cambiar contacto

En `index.html`, busca la sección de contacto:

```html
<a href="https://wa.me/593992217314" target="_blank">+593 99 221 7314</a>
<a href="mailto:contacto@agnexusuio.com">contacto@agnexusuio.com</a>
```

### Agregar más productos manualmente

Edita `productos.json` y agrega nuevos objetos al array. La página se actualizará automáticamente.

## 📋 Checklist de uso

- [ ] Abre `index.html` en navegador
- [ ] Verifica que ves productos (fallback o desde JSON)
- [ ] Prueba en mobile (responsivo)
- [ ] Prueba los botones de contacto (WhatsApp/Email)
- [ ] Ejecuta `scraper.py` para datos reales
- [ ] Recarga la página para ver nuevos productos

## 📝 Notas

- La página es **100% estática** - puede hospedarse en cualquier servidor
- No requiere base de datos ni backend
- Los productos se cargan desde `productos.json` (local)
- Para actualizar productos, ejecuta el scraper o edita el JSON manualmente

## ✨ Ventajas

1. **Carga rápida** - Sin dependencias pesadas
2. **SEO amigable** - HTML semántico
3. **Responsive** - Funciona en todos los dispositivos
4. **Actualizable** - Fácil de modificar productos
5. **Escalable** - Puede crecer el catálogo sin problemas

## 🐛 Solución de problemas

**P: No se ven los productos**  
R: 
- Verifica que exista `productos.json`
- Abre la consola del navegador (F12) para ver errores
- Usa los datos de fallback mientras ejecutas el scraper

**P: El scraper no funciona**  
R:
- Verifica: `pip install -r requirements.txt`
- Algunos sitios pueden bloquear requests
- Intenta ejecutar: `python -u scraper.py` para ver detalles

**P: Los precios están diferentes**  
R:
- Los precios en las tiendas cambian constantemente
- Ejecuta el scraper regularmente para actualizar
- O actualiza manualmente el JSON

---

Creado por Copilot para AGNEXUSUIO ✨
