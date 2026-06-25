# Burger Home — Sistema Automatizado de Gestión de Pedidos

Burger Home es un sistema de toma automatizada de pedidos modelado como una **Máquina de Estados Finita (FSM)** que gobierna un **canal conversacional simulado** por consola. El orquestador (`chatbot_simulado.py`) actúa como motor de transición: mantiene el estado conversacional en memoria, evalúa la entrada del usuario contra **compuertas de decisión (gateways)** derivadas del modelo **BPMN 2.0** y delega la mutación del dominio a **tareas de servicio (Service Tasks)**. La persistencia se resuelve mediante un esquema de **persistencia documental indexada** sobre `base_datos.json`, sin dependencias externas de motor de base de datos.

La arquitectura desacopla tres responsabilidades:

- **Capa de persistencia** — funciones `cargar_bd()` / `guardar_bd()`, que serializan y deserializan el documento JSON con validación estructural de claves requeridas.
- **Motor de estados (FSM)** — el bucle principal en `ejecutar_bot()`, que despacha la lógica según `estado_actual`.
- **Interfaz conversacional** — captura de entrada por consola (`input()`), modelada como **tarea de usuario (User Task)**.

---

## 🚀 Instrucciones de Ejecución

### Requisitos previos

- **Python 3.10+** (no requiere dependencias de terceros; utiliza únicamente la biblioteca estándar: `json`, `os`).
- El archivo `base_datos.json` debe residir en el mismo directorio que el orquestador.

### Clonado del repositorio

```bash
git clone https://github.com/<organizacion>/TPI1_OE.git
cd TPI1_OE
```

### Ejecución del orquestador principal

```bash
python chatbot_simulado.py
```

> En sistemas con coexistencia de intérpretes, invocar explícitamente `python3 chatbot_simulado.py`.

Para iniciar el flujo, simule el envío de un mensaje (por ejemplo, `Hola`). Para abortar la sesión en cualquier estado, ingrese `salir`.

---

## 📁 Estructura de Archivos

```
TPI1_OE/
├── chatbot_simulado.py          # Orquestador principal: motor FSM + capa de persistencia
├── base_datos.json              # Persistencia documental indexada (productos, cobertura, pedidos)
├── README.md                    # Documentación técnica y de arquitectura (este archivo)
└── doc/                         # Informes técnicos y modelo conceptual del proceso
    ├── MANUAL_USUARIO.md        # Guía funcional de operación del simulador
    ├── diagrama_proceso.bpmn    # Modelo de proceso ejecutable (BPMN 2.0)
    └── diagrama_proceso_bpmn.svg # Render vectorial del diagrama BPMN
```

---

## ⚙️ Funcionamiento del Bot (Máquina de Estados)

El motor conversacional implementa una FSM cuyo ciclo de vida del pedido transita por seis estados discretos. Cada iteración del bucle principal captura una entrada (User Task), evalúa las compuertas asociadas al estado vigente y, según el resultado, ejecuta una transición de estado o invoca una tarea de servicio.

### Estados del ciclo de vida del pedido

| Estado | Responsabilidad | Tipo de tarea BPMN |
|---|---|---|
| `IDLE` | Estado inicial. Despliega el menú dinámico desde `productos`. | Service Task (saludo + render de catálogo) |
| `ESPERANDO_PRODUCTO` | Valida la selección de combo y verifica disponibilidad de stock. | User Task + Gateway |
| `ESPERANDO_MODALIDAD` | Bifurca el flujo según modalidad de entrega. | Exclusive Gateway |
| `ESPERANDO_DIRECCION` | Valida la zona de cobertura del barrio (solo Delivery). | Service Task + Gateway |
| `ESPERANDO_PAGO` | Selecciona el medio de pago y bifurca según método. | Exclusive Gateway |
| `ESPERANDO_COMPROBANTE` | Valida el comprobante de transferencia con loop de reintentos. | User Task + Gateway con convergencia |

> **Nota de trazabilidad con BPMN 2.0:** el estado `ESPERANDO_DIRECCION` materializa la actividad conceptual de **validación de cobertura**, mientras que la actividad conceptual de **procesamiento del pedido** no es un estado conversacional sino una **tarea de servicio terminal** embebida en los estados `ESPERANDO_PAGO` (rama Efectivo) y `ESPERANDO_COMPROBANTE` (rama Transferencia): decremento atómico de inventario, registro de la transacción y alerta a cocina.

### Caminos alternativos: Retiro en local vs. Delivery

En `ESPERANDO_MODALIDAD` una **compuerta exclusiva (XOR)** divide el proceso:

- **Delivery (`1`):** transiciona a `ESPERANDO_DIRECCION`, donde una segunda compuerta evalúa si el barrio normalizado pertenece a la colección `zonas_cobertura`. Si pertenece, avanza a `ESPERANDO_PAGO`; en caso contrario, cancela el pedido por falta de cobertura.
- **Retiro en local (`2`):** **cortocircuita la validación de cobertura** y transiciona directamente a `ESPERANDO_PAGO`, calculando el importe a abonar. La dirección permanece `null` en el registro persistido.

### Manejo de excepciones

1. **Falta de stock (camino infeliz):** en `ESPERANDO_PRODUCTO`, si el campo `stock` del producto seleccionado es `<= 0`, el flujo notifica la indisponibilidad, retorna a `IDLE` y termina la simulación (pedido cancelado).
2. **Loop de convergencia por comprobante inválido:** en `ESPERANDO_COMPROBANTE`, el comprobante se valida por longitud mínima y extensión permitida (`jpg`, `jpeg`, `png`, `pdf`). Ante un comprobante inválido, el contador `intentos_comprobante` se incrementa y el flujo **reintenta sobre el mismo estado (loop de convergencia)**. Al alcanzar el **umbral de tres reintentos**, la compuerta deriva a cancelación definitiva del pedido.
3. **Entradas inválidas no terminales:** selecciones de menú, modalidad o pago inválidas mantienen el flujo atrapado en el estado vigente (`continue` / re-prompt) sin avanzar la transición, garantizando robustez del autómata.

---

## 🗄️ Arquitectura de la Base de Datos

El sistema adopta un modelo de **persistencia documental indexada** sobre el archivo `base_datos.json`, leído íntegramente en memoria al inicio (`cargar_bd()`) y reescrito de forma completa tras cada confirmación (`guardar_bd()`). La carga aplica **validación estructural**: rechaza el documento si no contiene las tres claves de primer nivel requeridas o si el JSON está corrupto.

El documento expone tres colecciones principales:

### Colección `productos` (catálogo de inventario)

Diccionario **indexado por identificador de producto** (clave string `"1"`–`"7"`). Cada entrada describe un combo y contiene el campo crítico `stock`, sujeto a **decremento atómico** ante cada compra exitosa (`bd["productos"][carrito["id"]]["stock"] -= 1`), encapsulado en manejo de excepciones para preservar la integridad ante claves o tipos inválidos.

```json
"productos": {
    "1": { "nombre": "Combo Burger Simple", "precio": 4500, "stock": 5 }
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | `string` | Denominación comercial del combo. |
| `precio` | `int` | Importe a abonar, en moneda local. |
| `stock` | `int` | **Campo crítico.** Unidades disponibles; decrementado atómicamente al confirmar el pedido. Valor `0` inhabilita la selección. |

### Colección `zonas_cobertura`

Arreglo de cadenas que enumera los barrios habilitados para Delivery. Funciona como **conjunto de pertenencia** consultado durante la validación de cobertura (comparación sobre el barrio normalizado a minúsculas).

### Colección `pedidos_registrados` (registro histórico de transacciones)

Arreglo append-only que constituye el **registro histórico de transacciones confirmadas**. Cada nuevo pedido se anexa (`append`) y se persiste atómicamente junto con el decremento de stock, garantizando que producción y registro queden sincronizados.

```json
"pedidos_registrados": [
    { "producto": "Combo Pollo Crispy", "modalidad": "Delivery", "pago": "Transferencia", "direccion": "macrocentro" }
]
```

| Campo | Tipo | Descripción |
|---|---|---|
| `producto` | `string` | Nombre del combo confirmado. |
| `modalidad` | `string` | `Delivery` o `Retiro`. |
| `pago` | `string` | `Efectivo` o `Transferencia`. |
| `direccion` | `string \| null` | Barrio de entrega; `null` en modalidad Retiro. |
