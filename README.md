# Burger Home - Sistema Automatizado de Gestión de Pedidos

Trabajo Práctico Integrador de la materia **Organización Empresarial**.

**Alumno:** Rodrigo Moyano

## Descripción

Burger Home es una hamburguesería ficticia utilizada como caso de estudio para analizar y mejorar su proceso de gestión de pedidos.

El proceso original se realiza principalmente de forma manual mediante WhatsApp. Como propuesta de mejora se desarrolló una simulación de chatbot en **Python**, modelada previamente mediante **BPMN 2.0**.

El chatbot utiliza una **Máquina de Estados Finitos (FSM)** para controlar las diferentes etapas de la conversación y un archivo **JSON** como mecanismo de persistencia simulado para almacenar productos, stock, zonas de cobertura y pedidos registrados.

El objetivo principal del proyecto es mantener coherencia entre:

- El proceso de negocio modelado mediante BPMN.
- Las decisiones y caminos alternativos del proceso.
- La Máquina de Estados.
- La lógica implementada en Python.

---

## Tecnologías utilizadas

- Python 3.10+
- JSON
- BPMN 2.0
- Git y GitHub

No se requieren librerías externas de Python.

---

## Estructura del proyecto

```text
TPI1_OE/
│
├── chatbot_simulado.py
├── base_datos.json
├── README.md
│
└── doc/
    ├── TPI_Organizacion_Empresarial_Rodrigo_Moyano.pdf
    └── TPI_Organizacion_Empresarial_Rodrigo_Moyano.docx
```

### Archivos principales

**`chatbot_simulado.py`**

Contiene la lógica principal del chatbot, las validaciones y la Máquina de Estados que controla el avance del pedido.

**`base_datos.json`**

Archivo utilizado como mecanismo de persistencia. Contiene:

- Catálogo de productos.
- Precios.
- Stock.
- Zonas de cobertura.
- Pedidos registrados.

**`doc/`**

Contiene la documentación correspondiente al Trabajo Práctico Integrador, incluyendo los diagramas BPMN AS-IS y TO-BE.

---

## Ejecución

### Requisitos

Tener instalado **Python 3.10 o superior**.

El archivo `base_datos.json` debe encontrarse en el mismo directorio que `chatbot_simulado.py`.

### Clonar el repositorio

```bash
git clone https://github.com/ElRodriCAT/TPI1_OE.git
cd TPI1_OE
```

### Ejecutar el chatbot

```bash
python chatbot_simulado.py
```

En sistemas donde Python se ejecuta mediante `python3`:

```bash
python3 chatbot_simulado.py
```

Para iniciar la simulación se debe ingresar un mensaje, por ejemplo:

```text
Hola
```

La palabra:

```text
salir
```

permite finalizar la simulación de manera controlada.

---

## Funcionamiento general

El chatbot guía al usuario durante el proceso de realización de un pedido.

El flujo principal es:

```text
Inicio
  ↓
Mostrar productos
  ↓
Seleccionar producto
  ↓
Validar producto y stock
  ↓
Elegir modalidad
  ↓
Delivery / Retiro
  ↓
Seleccionar medio de pago
  ↓
Confirmar pedido
  ↓
Preparación
  ↓
Retiro / Reparto
  ↓
Pedido entregado
```

Además del flujo principal, se contemplan caminos alternativos y entradas inválidas.

---

## Máquina de Estados Finitos

El chatbot utiliza una **Máquina de Estados Finitos (FSM)** para determinar en qué etapa se encuentra cada pedido y qué entradas son válidas en ese momento.

Los principales estados son:

| Estado | Función |
|---|---|
| `IDLE` | Espera el inicio de una nueva conversación. |
| `ESPERANDO_PRODUCTO` | Espera y valida la selección de un producto. |
| `ESPERANDO_MODALIDAD` | Espera la elección entre Delivery y Retiro. |
| `ESPERANDO_DIRECCION` | Solicita y valida la dirección para Delivery. |
| `ESPERANDO_CONFIRMACION_RETIRO` | Ofrece Retiro cuando la dirección está fuera de cobertura. |
| `ESPERANDO_PAGO` | Espera la selección del medio de pago. |
| `ESPERANDO_COMPROBANTE` | Espera y valida el comprobante de transferencia. |
| `PEDIDO_CONFIRMADO` | El pedido fue validado y registrado. |
| `EN_PRODUCCION` | Cocina se encuentra preparando el pedido. |
| `LISTO` | El pedido está preparado. |
| `EN_REPARTO` | El pedido se encuentra en proceso de entrega. |
| `ENTREGADO` | El pedido fue entregado o retirado. |

Una vez finalizado el pedido, el sistema vuelve al estado `IDLE` y queda disponible para iniciar una nueva operación.

---

## Caminos alternativos y validaciones

El sistema contempla situaciones que pueden ocurrir durante un pedido.

### Producto inválido

Si el usuario selecciona una opción inexistente, el sistema informa el error y permanece en `ESPERANDO_PRODUCTO`.

El usuario puede realizar una nueva selección sin reiniciar el proceso.

### Producto sin stock

Si el producto existe pero no posee stock disponible, el sistema informa la situación y permite seleccionar otro producto.

### Delivery fuera de cobertura

Si el cliente selecciona Delivery pero la dirección ingresada se encuentra fuera de la zona de cobertura, el chatbot ofrece la posibilidad de **Retiro en local**.

Si el cliente acepta, el pedido continúa hacia el pago.

Si rechaza la alternativa, el pedido se cancela.

### Método de pago inválido

Una opción de pago incorrecta no finaliza el pedido. El sistema informa el error y vuelve a solicitar el medio de pago.

### Comprobante inválido

Si se selecciona Transferencia y el comprobante ingresado no cumple con la validación, el chatbot informa el error y permite volver a ingresarlo.

El pedido permanece en `ESPERANDO_COMPROBANTE` hasta recibir una entrada válida o hasta que el usuario decida finalizar la simulación.

---

## Flujo posterior a la confirmación

Cuando el pedido es confirmado:

1. Se registra el pedido.
2. Se actualiza el stock.
3. Se notifica a Cocina.
4. El pedido pasa a `EN_PRODUCCION`.
5. Cocina informa cuando está `LISTO`.

A partir de allí, el flujo depende de la modalidad seleccionada.

### Retiro en local

El cliente es informado de que el pedido está listo.

Cuando se confirma el retiro, el pedido pasa a `ENTREGADO`.

### Delivery

El pedido pasa a `EN_REPARTO`.

El repartidor confirma la entrega y el pedido pasa a `ENTREGADO`.

Finalmente, el sistema limpia los datos temporales y vuelve a `IDLE`.

---

## Persistencia de datos

El proyecto utiliza el archivo:

```text
base_datos.json
```

como mecanismo de persistencia simulado.

El archivo contiene tres estructuras principales:

### `productos`

Almacena el catálogo de productos.

Ejemplo:

```json
{
    "nombre": "Combo Burger Simple",
    "precio": 4500,
    "stock": 5
}
```

El stock se consulta antes de permitir avanzar con el pedido y se actualiza cuando el pedido es confirmado.

### `zonas_cobertura`

Contiene las zonas habilitadas para Delivery.

El chatbot compara la dirección ingresada con esta lista para determinar si el pedido puede enviarse a domicilio.

### `pedidos_registrados`

Mantiene el historial de pedidos confirmados.

Cada pedido puede almacenar información como:

```json
{
    "producto": "Combo Burger Simple",
    "modalidad": "Delivery",
    "pago": "Transferencia",
    "direccion": "macrocentro",
    "estado": "PEDIDO_CONFIRMADO"
}
```

El estado del pedido se actualiza posteriormente a medida que avanza por producción y entrega.

---

## Modelado BPMN

El proyecto incluye dos modelos principales:

### AS-IS

Representa el proceso original de Burger Home, donde la atención y gestión del pedido depende principalmente de la intervención manual de un empleado.

### TO-BE

Representa el proceso mejorado mediante la incorporación del chatbot.

El modelo contempla:

- Tareas realizadas por el cliente.
- Tareas automatizadas por el sistema.
- Intervención de Cocina.
- Intervención del Repartidor.
- Decisiones mediante gateways exclusivos.
- Validación de producto y stock.
- Cobertura de Delivery.
- Alternativa de Retiro.
- Validación del medio de pago.
- Confirmación y preparación.
- Retiro o entrega del pedido.

La lógica implementada en Python busca mantener coherencia con este proceso.

---

## Pruebas

El sistema fue probado tanto sobre el flujo principal como sobre diferentes caminos alternativos.

Entre las situaciones verificadas se encuentran:

- Opciones de producto inválidas.
- Productos sin stock.
- Modalidades inválidas.
- Direcciones fuera de cobertura.
- Métodos de pago inválidos.
- Comprobantes inválidos.
- Retiro en local.
- Delivery.
- Preparación y entrega completa del pedido.

Estas pruebas permiten comprobar que una entrada incorrecta no finalice innecesariamente el proceso cuando existe una alternativa válida.

---

## Uso de Inteligencia Artificial

Durante el desarrollo del proyecto se utilizaron herramientas de Inteligencia Artificial como apoyo.

### Claude CLI

Utilizado principalmente para:

- Revisión del código.
- Detección de posibles inconsistencias.
- Apoyo en la documentación.
- Generación y revisión del manual de usuario.

### Gemini

Utilizado como herramienta de consulta y apoyo durante:

- Planificación del proyecto.
- Revisión del modelado BPMN.
- Análisis de aspectos técnicos del proceso.

Las respuestas generadas por las herramientas fueron revisadas y contrastadas con la consigna, el modelo BPMN y el funcionamiento real del programa antes de aplicar modificaciones.

---

## Documentación

La documentación completa del Trabajo Práctico Integrador se encuentra en la carpeta:

```text
/doc
```

Allí se incluye el informe del proyecto con:

- Análisis de la organización.
- Enfoque sistémico.
- Proceso AS-IS.
- Propuesta TO-BE.
- Diagramas BPMN 2.0.
- Arquitectura de la solución.
- Máquina de Estados.
- Diccionario de datos.
- Pruebas.
- Evidencias de utilización de Inteligencia Artificial.

---

## Autor

**Rodrigo Moyano**

Tecnicatura Universitaria en Programación  
Universidad Tecnológica Nacional