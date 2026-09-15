# Burger Home - Sistema Automatizado de Gestión de Pedidos

Trabajo Práctico Integrador de la materia **Organización Empresarial**.

**Alumno:** Rodrigo Moyano

## Descripción

Burger Home es una hamburguesería ficticia utilizada como caso de estudio para analizar y mejorar su proceso de gestión de pedidos.

El proceso original se realiza principalmente de forma manual mediante WhatsApp. Como propuesta de mejora se desarrolló una simulación de chatbot en **Python**, modelada mediante **BPMN 2.0**.

El chatbot utiliza una **Máquina de Estados Finitos (FSM)** para controlar las diferentes etapas del proceso y un archivo **JSON** como mecanismo de persistencia simulado para almacenar productos, stock, zonas de cobertura y pedidos registrados.

El objetivo principal del proyecto es mantener coherencia entre el proceso de negocio modelado mediante BPMN, las decisiones del proceso, la Máquina de Estados y la lógica implementada en Python.

---

## Tecnologías utilizadas

- Python 3
- JSON
- BPMN 2.0
- Git
- GitHub

El programa no requiere librerías externas de Python.

---

## Estructura del proyecto

```text
TPI1_OE/
│
├── README.md
├── chatbot_simulado.py
├── base_datos.json
│
└── doc/
    ├── MANUAL_USUARIO.md
    ├── diagrama_proceso.bpmn
    ├── diagrama_proceso_bpmn.svg
    ├── TPI_Organizacion_Empresarial_Rodrigo_Moyano.docx
    └── TPI_Organizacion_Empresarial_Rodrigo_Moyano.pdf
```

> Los archivos DOCX y PDF corresponden a la documentación final del Trabajo Práctico Integrador.

---

## Archivos principales

### `chatbot_simulado.py`

Contiene la lógica principal del chatbot, las validaciones y la Máquina de Estados que controla el avance del pedido.

### `base_datos.json`

Archivo utilizado como mecanismo de persistencia simulado. Contiene:

- Productos.
- Precios.
- Stock.
- Zonas de cobertura.
- Pedidos registrados.

### `doc/MANUAL_USUARIO.md`

Contiene las instrucciones necesarias para ejecutar y utilizar el chatbot.

### `doc/diagrama_proceso.bpmn`

Archivo editable correspondiente al modelado BPMN del proceso.

### `doc/diagrama_proceso_bpmn.svg`

Versión gráfica del diagrama BPMN.

### Documentación del TPI

Los archivos DOCX y PDF contienen el informe final del Trabajo Práctico Integrador.

---

## Instalación y ejecución

### Requisitos

Tener instalado **Python 3**.

El archivo `base_datos.json` debe encontrarse en el mismo directorio que `chatbot_simulado.py`.

### Clonar el repositorio

```bash
git clone https://github.com/ElRodriCAT/TPI1_OE.git
cd TPI1_OE
```

### Ejecutar

```bash
python chatbot_simulado.py
```

En sistemas donde Python se ejecuta mediante `python3`:

```bash
python3 chatbot_simulado.py
```

Para comenzar la simulación se puede ingresar un mensaje como:

```text
Hola
```

La palabra:

```text
salir
```

permite finalizar la simulación.

---

## Funcionamiento general

El chatbot guía al usuario durante la realización de un pedido.

El flujo general es:

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

Además del flujo principal, el sistema contempla entradas inválidas y caminos alternativos.

---

## Máquina de Estados Finitos

El chatbot utiliza una **Máquina de Estados Finitos (FSM)** para determinar en qué etapa se encuentra el proceso y qué acciones son válidas en cada momento.

Los estados utilizados son:

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

### Producto inválido

Si el usuario selecciona una opción inexistente, el sistema informa el error y permanece en `ESPERANDO_PRODUCTO`, permitiendo realizar una nueva selección.

### Producto sin stock

Si el producto seleccionado no posee stock disponible, el sistema informa la situación y permite seleccionar otro producto.

### Delivery fuera de cobertura

Si la dirección ingresada no se encuentra dentro de las zonas de cobertura, el chatbot ofrece **Retiro en local** como alternativa.

Si el cliente acepta, el proceso continúa hacia el pago. Si rechaza la alternativa, el pedido se cancela.

### Método de pago inválido

Una opción de pago incorrecta no finaliza el pedido. El sistema informa el error y solicita nuevamente el medio de pago.

### Comprobante inválido

Si el comprobante ingresado no cumple con la validación, el sistema informa el error y permite ingresarlo nuevamente.

---

## Flujo posterior a la confirmación

Cuando el pedido es confirmado:

1. Se registra el pedido.
2. Se actualiza el stock.
3. Se notifica a Cocina.
4. El pedido pasa a `EN_PRODUCCION`.
5. Cocina informa cuando está `LISTO`.

Si la modalidad es **Retiro**, el cliente es notificado y posteriormente confirma el retiro.

Si la modalidad es **Delivery**, el pedido pasa a `EN_REPARTO` y el repartidor confirma la entrega.

En ambos casos el pedido finalmente pasa a `ENTREGADO`.

---

## Persistencia

El proyecto utiliza:

```text
base_datos.json
```

como mecanismo de persistencia simulado.

El archivo contiene:

### `productos`

Catálogo con nombre, precio y stock de cada producto.

### `zonas_cobertura`

Zonas habilitadas para realizar entregas mediante Delivery.

### `pedidos_registrados`

Historial de pedidos confirmados y sus respectivos estados.

El stock se consulta durante la selección y se actualiza cuando se registra un pedido.

Los cambios realizados sobre los pedidos también se almacenan en el archivo JSON.

---

## Modelado BPMN

El proyecto analiza dos situaciones:

### AS-IS

Representa el proceso original de Burger Home, donde la gestión del pedido se realiza principalmente de manera manual.

### TO-BE

Representa el proceso mejorado mediante la incorporación del chatbot.

El modelo TO-BE contempla:

- Cliente.
- Chatbot / Sistema.
- Cocina.
- Repartidor.
- Validación de producto.
- Validación de stock.
- Selección de Delivery o Retiro.
- Validación de cobertura.
- Alternativa de Retiro.
- Selección y validación del pago.
- Registro del pedido.
- Preparación.
- Retiro o reparto.
- Finalización del pedido.

La implementación en Python busca mantener coherencia con el proceso representado mediante BPMN.

---

## Pruebas

Se realizaron pruebas sobre el flujo principal y sobre caminos alternativos.

Entre las situaciones verificadas se encuentran:

- Producto inválido.
- Producto sin stock.
- Modalidad inválida.
- Dirección fuera de cobertura.
- Método de pago inválido.
- Comprobante inválido.
- Retiro en local.
- Delivery.
- Preparación y entrega completa.

El objetivo de estas pruebas es comprobar que el sistema pueda responder ante entradas incorrectas y continuar el proceso cuando exista una alternativa válida.

---

## Uso de Inteligencia Artificial

Durante el desarrollo se utilizaron herramientas de Inteligencia Artificial como apoyo.

### Claude CLI

Utilizado principalmente para:

- Revisión del código.
- Detección de posibles inconsistencias.
- Apoyo en la documentación.
- Revisión del manual de usuario.

### Gemini

Utilizado como herramienta de consulta y apoyo para:

- Planificación del proyecto.
- Revisión del modelado BPMN.
- Análisis de aspectos del proceso.

Las respuestas generadas por las herramientas fueron revisadas antes de incorporar modificaciones al proyecto.

---

## Documentación

La documentación complementaria se encuentra en:

```text
/doc
```

Esta carpeta contiene el manual de usuario, los archivos correspondientes al modelado BPMN y la documentación final del Trabajo Práctico Integrador.

---

## Autor

**Rodrigo Moyano**

Tecnicatura Universitaria en Programación  
Universidad Tecnológica Nacional