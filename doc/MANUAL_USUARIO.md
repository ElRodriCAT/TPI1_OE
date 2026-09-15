# Manual de Usuario - Burger Home

## 1. Introducción

Burger Home es una simulación de un sistema automatizado de gestión de pedidos desarrollada en Python.

El usuario interactúa con un chatbot desde la consola. El sistema permite seleccionar productos, verificar disponibilidad, elegir entre Delivery o Retiro, seleccionar un medio de pago y completar el proceso hasta la entrega del pedido.

El sistema utiliza una Máquina de Estados Finitos (FSM) para controlar las diferentes etapas de la interacción.

---

## 2. Requisitos

Para ejecutar el sistema se necesita:

- Python 3.
- `chatbot_simulado.py`.
- `base_datos.json`.

Ambos archivos deben encontrarse en el mismo directorio.

No es necesario instalar librerías externas.

---

## 3. Ejecución

Desde una terminal ubicada en la carpeta del proyecto ejecutar:

```bash
python chatbot_simulado.py
```

También puede utilizarse:

```bash
python3 chatbot_simulado.py
```

dependiendo de la instalación de Python.

---

## 4. Inicio

Al ejecutar el programa, el chatbot queda esperando el inicio de una conversación.

Por ejemplo:

```text
Hola
```

El sistema responde mostrando el menú de productos disponibles.

---

## 5. Selección de producto

El chatbot muestra los productos disponibles junto con su precio y stock.

El usuario debe ingresar la opción correspondiente al producto que desea comprar.

### Producto inválido

Si se ingresa una opción inexistente, el chatbot informa el error y permite realizar una nueva selección.

El proceso no se cancela.

### Producto sin stock

Si el producto seleccionado no tiene stock disponible, el chatbot informa la situación y vuelve a permitir la selección de otro producto.

---

## 6. Modalidad de entrega

Después de seleccionar un producto válido, el sistema solicita elegir una modalidad:

```text
1. Delivery
2. Retiro
```

### Retiro

Si se selecciona Retiro, no es necesario ingresar una dirección y el proceso continúa hacia la selección del medio de pago.

### Delivery

Si se selecciona Delivery, el chatbot solicita una dirección o zona.

El sistema compara la información ingresada con las zonas de cobertura almacenadas en `base_datos.json`.

---

## 7. Dirección fuera de cobertura

Si la dirección ingresada no se encuentra dentro de la zona de cobertura, el pedido no se cancela inmediatamente.

El chatbot ofrece continuar mediante **Retiro en local**.

### Si el cliente acepta

La modalidad cambia a Retiro y el proceso continúa hacia el pago.

### Si el cliente rechaza

El pedido se cancela.

---

## 8. Medio de pago

El sistema permite seleccionar el medio de pago correspondiente.

Las opciones disponibles son:

- Efectivo.
- Transferencia.

Si se ingresa una opción inválida, el chatbot informa el error y solicita nuevamente el medio de pago.

---

## 9. Pago en efectivo

Si el cliente selecciona Efectivo, el pedido puede ser confirmado sin necesidad de ingresar un comprobante.

El sistema registra el pedido y actualiza el stock.

---

## 10. Pago mediante transferencia

Si se selecciona Transferencia, el chatbot solicita ingresar un comprobante.

### Comprobante válido

Si el comprobante cumple con la validación, el pedido continúa y es confirmado.

### Comprobante inválido

Si el comprobante no es válido, el sistema informa el error y permite ingresarlo nuevamente.

El pedido permanece en la etapa de comprobante hasta recibir una entrada válida o finalizar la simulación.

---

## 11. Confirmación del pedido

Una vez completadas las validaciones necesarias:

1. El pedido se confirma.
2. Se registra en `base_datos.json`.
3. Se actualiza el stock del producto.
4. Se notifica el pedido a Cocina.
5. El pedido pasa al estado `EN_PRODUCCION`.

---

## 12. Preparación

Cuando el pedido se encuentra en producción, la simulación representa la intervención de Cocina.

Cocina debe indicar:

```text
listo
```

cuando finaliza la preparación.

El pedido pasa entonces al estado:

```text
LISTO
```

---

## 13. Pedido con Retiro

Si la modalidad seleccionada es Retiro, una vez preparado el pedido el sistema informa al cliente que se encuentra listo.

Para representar la entrega al cliente se ingresa:

```text
retirado
```

El pedido pasa al estado:

```text
ENTREGADO
```

---

## 14. Pedido con Delivery

Si la modalidad seleccionada es Delivery, cuando Cocina finaliza la preparación el pedido pasa al proceso de reparto.

El sistema actualiza el pedido al estado:

```text
EN_REPARTO
```

Para representar la confirmación realizada por el repartidor se ingresa:

```text
entregado
```

El pedido pasa al estado:

```text
ENTREGADO
```

---

## 15. Finalización

Una vez que el pedido llega a `ENTREGADO`, el chatbot finaliza el proceso actual, limpia los datos temporales de la operación y vuelve al estado:

```text
IDLE
```

El sistema queda preparado para iniciar un nuevo pedido.

---

## 16. Estados del sistema

| Estado | Descripción |
|---|---|
| `IDLE` | Espera el inicio de una conversación. |
| `ESPERANDO_PRODUCTO` | Espera la selección de un producto. |
| `ESPERANDO_MODALIDAD` | Espera la elección entre Delivery y Retiro. |
| `ESPERANDO_DIRECCION` | Espera la dirección para un pedido con Delivery. |
| `ESPERANDO_CONFIRMACION_RETIRO` | Espera la respuesta ante la alternativa de Retiro. |
| `ESPERANDO_PAGO` | Espera la selección del medio de pago. |
| `ESPERANDO_COMPROBANTE` | Espera un comprobante válido. |
| `PEDIDO_CONFIRMADO` | El pedido fue confirmado y registrado. |
| `EN_PRODUCCION` | Cocina está preparando el pedido. |
| `LISTO` | El pedido está preparado. |
| `EN_REPARTO` | El pedido se encuentra en proceso de entrega. |
| `ENTREGADO` | El pedido fue entregado o retirado. |

---

## 17. Persistencia

El sistema utiliza:

```text
base_datos.json
```

como mecanismo de persistencia simulado.

El archivo almacena:

- Productos.
- Precios.
- Stock.
- Zonas de cobertura.
- Pedidos registrados.

Cuando se confirma un pedido, el stock correspondiente se modifica y el pedido queda registrado.

Los cambios posteriores de estado también se almacenan.

---

## 18. Manejo de errores y caminos alternativos

El chatbot contempla diferentes situaciones que pueden ocurrir durante el proceso:

| Situación | Respuesta del sistema |
|---|---|
| Producto inválido | Informa el error y permite elegir nuevamente. |
| Producto sin stock | Informa la falta de stock y permite elegir otro. |
| Modalidad inválida | Solicita nuevamente la modalidad. |
| Dirección fuera de cobertura | Ofrece Retiro en local. |
| Retiro alternativo rechazado | Cancela el pedido. |
| Medio de pago inválido | Solicita nuevamente el medio de pago. |
| Comprobante inválido | Solicita nuevamente el comprobante. |

Estas validaciones permiten continuar el proceso cuando el error puede ser corregido sin necesidad de reiniciar toda la operación.

---

## 19. Salir del programa

Durante la simulación puede utilizarse:

```text
salir
```

para finalizar la ejecución de manera controlada.

---

## 20. Ejemplo de flujo completo

Un ejemplo de pedido mediante Delivery y Transferencia es:

```text
Inicio de conversación
        ↓
Selección de producto
        ↓
Validación de stock
        ↓
Delivery
        ↓
Ingreso de dirección
        ↓
Validación de cobertura
        ↓
Transferencia
        ↓
Ingreso de comprobante
        ↓
Confirmación del pedido
        ↓
EN_PRODUCCION
        ↓
LISTO
        ↓
EN_REPARTO
        ↓
ENTREGADO
```

Un pedido mediante Retiro sigue el mismo proceso inicial, pero después de la preparación no pasa por `EN_REPARTO`.

---

## 21. Archivos relacionados

La documentación complementaria del proyecto se encuentra en la carpeta `doc/`.

Allí se incluyen:

- Manual de usuario.
- Archivo editable del diagrama BPMN.
- Diagrama BPMN en formato SVG.
- Informe del Trabajo Práctico Integrador.

El código fuente y el archivo JSON se encuentran en la raíz del repositorio.