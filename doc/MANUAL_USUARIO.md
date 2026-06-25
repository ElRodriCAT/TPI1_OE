# Manual de Usuario — Chatbot Simulado Burger Home

## ¿Qué es este sistema?

Es un simulador de chatbot por consola que reproduce el flujo de toma de pedidos de una hamburguesería (Burger Home). Está diseñado para demostrar una máquina de estados conversacional con persistencia en archivo JSON.

---

## Requisitos previos

- Python 3.10+ instalado
- Archivo `base_datos.json` presente en el directorio raíz, junto a `chatbot_simulado.py`

---

## Cómo ejecutar

```bash
python chatbot_simulado.py
```

---

## Flujo de conversación

El bot guía al cliente por los siguientes pasos en orden:

### 1. Saludo — Ver el menú

Al escribir cualquier mensaje (por ejemplo `Hola`), el bot muestra los productos disponibles con su precio y stock actual.

```
Cliente 👤: Hola
Bot ⚙️: ¡Hola! Bienvenido a Burger Home. Este es nuestro menú disponible:
  [1] Combo Burger Simple - $4500 (Stock: 5)
  [2] Combo Burger Doble - $5800 (Stock: 10)
  ...
```

### 2. Seleccionar producto

Ingresá el número del combo que querés pedir (1 al 7).

- Si el número no existe en el menú, el bot te vuelve a pedir una opción válida.
- Si el producto no tiene stock, el pedido se cancela automáticamente.

### 3. Elegir modalidad de entrega

```
[1] Delivery
[2] Retiro en Local
```

- **Delivery:** el bot te pedirá tu barrio para verificar cobertura.
- **Retiro:** pasa directo al paso de pago.

### 4. Verificación de zona (solo Delivery)

Ingresá el nombre de tu barrio. Las zonas con cobertura disponibles son:

| Barrio        |
|---------------|
| Centro        |
| Macrocentro   |
| Barrio Norte  |
| Barrio Sur    |
| Barrio Oeste  |

Si el barrio no tiene cobertura, el pedido se cancela.

### 5. Método de pago

```
[1] Efectivo
[2] Transferencia Bancaria
```

- **Efectivo:** el pedido se confirma de inmediato.
- **Transferencia:** el bot te pedirá que adjuntes el comprobante. En la simulación, escribí un nombre de archivo válido (mínimo 3 caracteres y extensión `jpg`, `jpeg`, `png` o `pdf`, por ejemplo `comprobante.jpg`). Tenés hasta **3 intentos**; si los superás, el pedido se cancela.

### 6. Confirmación del pedido

Una vez confirmado, el bot:
- Descuenta una unidad del stock del producto seleccionado.
- Registra el pedido en `base_datos.json`.
- Muestra una alerta de envío a cocina.

---

## Salir del simulador

En cualquier momento, escribí `salir` para terminar la sesión sin completar el pedido.

```
Cliente 👤: salir
```

---

## Archivo de base de datos (`base_datos.json`)

El sistema lee y escribe sobre este archivo JSON. Contiene tres secciones:

| Sección              | Descripción                                         |
|----------------------|-----------------------------------------------------|
| `productos`          | Catálogo con nombre, precio y stock de cada combo   |
| `zonas_cobertura`    | Lista de barrios que reciben delivery               |
| `pedidos_registrados`| Historial de pedidos confirmados                    |

> Para modificar el stock, agregar productos o ampliar zonas de cobertura, editá directamente el archivo `base_datos.json`.

---

## Tabla de estados internos

| Estado               | Qué espera el bot              |
|----------------------|-------------------------------|
| `IDLE`               | Cualquier mensaje del cliente  |
| `ESPERANDO_PRODUCTO` | Número de combo del menú       |
| `ESPERANDO_MODALIDAD`| `1` (Delivery) o `2` (Retiro)  |
| `ESPERANDO_DIRECCION`| Nombre del barrio              |
| `ESPERANDO_PAGO`     | `1` (Efectivo) o `2` (Transf.) |
| `ESPERANDO_COMPROBANTE` | Texto que simule el archivo  |

---

## Casos de error y cómo se manejan

| Situación                        | Comportamiento del bot                        |
|----------------------------------|-----------------------------------------------|
| Opción de menú inválida          | Vuelve a pedir sin avanzar                    |
| Producto sin stock               | Cancela el pedido y termina la simulación     |
| Barrio sin cobertura             | Cancela el pedido y termina la simulación     |
| Opción de modalidad inválida     | Vuelve a pedir sin avanzar                    |
| Comprobante inválido (corto o sin extensión válida) | Vuelve a pedir el comprobante; tras 3 intentos cancela el pedido |
