import json
import os


# --- FUNCIONES DE PERSISTENCIA (BASE DE DATOS SIMULADA) ---

def cargar_bd():
    """Lee el archivo JSON utilizado como persistencia del simulador."""
    if os.path.exists("base_datos.json"):
        try:
            with open("base_datos.json", "r", encoding="utf-8") as f:
                datos = json.load(f)

            claves_requeridas = {"productos", "zonas_cobertura", "pedidos_registrados"}

            if not claves_requeridas.issubset(datos.keys()):
                print("Error: base_datos.json tiene estructura incorrecta. Faltan claves requeridas.")
                return {}

            return datos

        except json.JSONDecodeError:
            print("Error: base_datos.json está corrupto o tiene formato inválido.")
            return {}

        except OSError as e:
            print(f"Error al leer base_datos.json: {e}")
            return {}

    return {}


def guardar_bd(data):
    """Guarda las modificaciones en el archivo JSON."""
    try:
        with open("base_datos.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except OSError as e:
        print(f"\nAdvertencia: no se pudo guardar la información: {e}")


def registrar_pedido(bd, carrito, modalidad, pago, direccion):
    """
    Confirma el pedido, descuenta una unidad del stock y lo registra en el JSON.
    Devuelve el pedido creado para poder actualizar su estado posteriormente.
    """
    try:
        bd["productos"][carrito["id"]]["stock"] -= 1
    except (KeyError, TypeError) as e:
        print(f"\nAdvertencia: no se pudo actualizar el stock: {e}")

    nuevo_pedido = {
        "producto": carrito["nombre"],
        "modalidad": modalidad,
        "pago": pago,
        "direccion": direccion,
        "estado": "PEDIDO_CONFIRMADO"
    }

    bd["pedidos_registrados"].append(nuevo_pedido)
    guardar_bd(bd)

    return nuevo_pedido


def actualizar_estado_pedido(bd, pedido, nuevo_estado):
    """Actualiza el estado del pedido actual y persiste el cambio."""
    pedido["estado"] = nuevo_estado
    guardar_bd(bd)


# --- SIMULADOR DEL CHATBOT ---

def ejecutar_bot():

    bd = cargar_bd()

    if not bd:
        print("Error crítico: no se pudo cargar la base de datos. Verificá el archivo base_datos.json.")
        return

    # Variables que representan la memoria del bot.
    estado_actual = "IDLE"
    carrito = {}
    modalidad = None
    direccion = None
    pedido_actual = None

    print("=== SIMULADOR DE CHATBOT AUTOMATIZADO - BURGER HOME ===")
    print("Para iniciar el flujo, enviá un mensaje (Ej: 'Hola').")
    print("Para salir de la simulación, escribí 'salir'.\n")

    while True:

        # ---------------------------------------------------------
        # ESTADOS AUTOMÁTICOS
        # No esperan una entrada del usuario para avanzar.
        # ---------------------------------------------------------

        if estado_actual == "PEDIDO_CONFIRMADO":
            print("\n--- ALERTA A COCINA 🍳 ---")
            print("Pedido confirmado y enviado a producción.")

            actualizar_estado_pedido(bd, pedido_actual, "EN_PRODUCCION")
            estado_actual = "EN_PRODUCCION"
            continue

        if estado_actual == "ENTREGADO":
            print("\nSistema: proceso finalizado correctamente.")
            print("El bot vuelve al estado inicial para permitir un nuevo pedido.\n")

            carrito = {}
            modalidad = None
            direccion = None
            pedido_actual = None

            estado_actual = "IDLE"
            continue

        if estado_actual == "LISTO" and modalidad == "Delivery":
            print("\nSistema: pedido asignado al repartidor.")

            actualizar_estado_pedido(bd, pedido_actual, "EN_REPARTO")
            estado_actual = "EN_REPARTO"
            continue

        # ---------------------------------------------------------
        # ESTADOS QUE ESPERAN UNA ENTRADA
        # ---------------------------------------------------------

        if estado_actual == "EN_PRODUCCION":
            entrada_usuario = input(
                "Cocina 🍳 (escribí 'listo' cuando termine el pedido): "
            ).strip()

        elif estado_actual == "EN_REPARTO":
            entrada_usuario = input(
                "Repartidor 🛵 (escribí 'entregado' cuando entregue el pedido): "
            ).strip()

        elif estado_actual == "LISTO" and modalidad == "Retiro":
            entrada_usuario = input(
                "Cliente 👤 (escribí 'retirado' cuando retires el pedido): "
            ).strip()

        else:
            entrada_usuario = input("Cliente 👤: ").strip()

        # Permite interrumpir la simulación desde cualquier estado interactivo.
        if entrada_usuario.lower() == "salir":
            print("\nSimulación finalizada.")
            break

        # --- MÁQUINA DE ESTADOS ---

        if estado_actual == "IDLE":
            # Cualquier mensaje inicia la conversación y muestra el menú disponible.
            print("\nBot 🤖: ¡Hola! Bienvenido a Burger Home.")
            print("Este es nuestro menú disponible:")

            for id_prod, info in bd["productos"].items():
                print(
                    f" [{id_prod}] {info['nombre']} - "
                    f"${info['precio']} (Stock: {info['stock']})"
                )

            print("Por favor, ingresá el número del combo que querés pedir.")
            estado_actual = "ESPERANDO_PRODUCTO"

        elif estado_actual == "ESPERANDO_PRODUCTO":

            if entrada_usuario not in bd["productos"]:
                print("\nBot 🤖: Opción inválida.")
                print("Por favor, ingresá una opción válida del menú.")
                continue

            producto_seleccionado = bd["productos"][entrada_usuario]

            if producto_seleccionado["stock"] <= 0:
                print(
                    f"\nBot 🤖: Disculpame, nos quedamos sin stock de "
                    f"{producto_seleccionado['nombre']}."
                )
                print("Por favor, seleccioná otro producto disponible.")
                continue

            carrito = {
                "id": entrada_usuario,
                "nombre": producto_seleccionado["nombre"],
                "precio": producto_seleccionado["precio"]
            }

            print(f"\nBot 🤖: Seleccionaste {carrito['nombre']}.")
            print("¿Cómo preferís tu pedido?")
            print(" [1] Delivery")
            print(" [2] Retiro en Local")

            estado_actual = "ESPERANDO_MODALIDAD"

        elif estado_actual == "ESPERANDO_MODALIDAD":

            if entrada_usuario == "1":
                modalidad = "Delivery"

                print("\nBot 🤖: Por favor, ingresá tu barrio para verificar si tenemos cobertura:")
                estado_actual = "ESPERANDO_DIRECCION"

            elif entrada_usuario == "2":
                modalidad = "Retiro"
                direccion = None

                print(f"\nBot 🤖: Perfecto. El total a abonar es: ${carrito['precio']}.")
                print("¿Cómo vas a pagar?")
                print(" [1] Efectivo")
                print(" [2] Transferencia Bancaria")

                estado_actual = "ESPERANDO_PAGO"

            else:
                print("\nBot 🤖: Opción inválida.")
                print("Ingresá 1 para Delivery o 2 para Retiro.")

        elif estado_actual == "ESPERANDO_DIRECCION":

            barrio = entrada_usuario.lower()

            if barrio in bd["zonas_cobertura"]:
                direccion = entrada_usuario

                print(f"\nBot 🤖: ¡Genial! {entrada_usuario} está en nuestra zona de cobertura.")
                print(f"El total a abonar es: ${carrito['precio']}.")
                print("¿Cómo vas a pagar?")
                print(" [1] Efectivo")
                print(" [2] Transferencia Bancaria")

                estado_actual = "ESPERANDO_PAGO"

            else:
                print(f"\nBot 🤖: Lo lamento, no tenemos delivery hasta {entrada_usuario}.")
                print("¿Querés retirar el pedido por el local?")
                print(" [1] Sí")
                print(" [2] No")

                estado_actual = "ESPERANDO_CONFIRMACION_RETIRO"

        elif estado_actual == "ESPERANDO_CONFIRMACION_RETIRO":

            if entrada_usuario == "1":
                modalidad = "Retiro"
                direccion = None

                print("\nBot 🤖: Perfecto. Cambiamos el pedido a Retiro en Local.")
                print(f"El total a abonar es: ${carrito['precio']}.")
                print("¿Cómo vas a pagar?")
                print(" [1] Efectivo")
                print(" [2] Transferencia Bancaria")

                estado_actual = "ESPERANDO_PAGO"

            elif entrada_usuario == "2":
                print("\nBot 🤖: Entendido. El pedido fue cancelado.")
                print("Podés iniciar un nuevo pedido cuando quieras.")

                carrito = {}
                modalidad = None
                direccion = None
                pedido_actual = None
                estado_actual = "IDLE"

            else:
                print("\nBot 🤖: Opción inválida.")
                print("Ingresá 1 para retirar por el local o 2 para cancelar el pedido.")

        elif estado_actual == "ESPERANDO_PAGO":

            if entrada_usuario == "1":
                print("\nBot 🤖: ¡Pedido confirmado! Abonás al recibir o retirar.")

                pedido_actual = registrar_pedido(
                    bd,
                    carrito,
                    modalidad,
                    "Efectivo",
                    direccion
                )

                estado_actual = "PEDIDO_CONFIRMADO"
                continue

            elif entrada_usuario == "2":
                print("\nBot 🤖: Por favor, adjuntá tu comprobante.")
                print("Simulá escribiendo el nombre del archivo, por ejemplo: comprobante.jpg")

                estado_actual = "ESPERANDO_COMPROBANTE"

            else:
                print("\nBot 🤖: Método de pago inválido.")
                print("Seleccioná 1 para Efectivo o 2 para Transferencia.")

        elif estado_actual == "ESPERANDO_COMPROBANTE":

            extension_valida = (
                "." in entrada_usuario
                and entrada_usuario.split(".")[-1].lower() in ["jpg", "jpeg", "png", "pdf"]
            )

            if len(entrada_usuario) < 3 or not extension_valida:
                print("\nBot 🤖: Comprobante inválido.")
                print("El archivo debe tener extensión jpg, jpeg, png o pdf.")
                print("Por favor, enviá otro comprobante.")
                continue

            print("\nBot 🤖: Comprobante validado con éxito.")
            print("¡Pedido confirmado!")

            pedido_actual = registrar_pedido(
                bd,
                carrito,
                modalidad,
                "Transferencia",
                direccion
            )

            estado_actual = "PEDIDO_CONFIRMADO"
            continue

        elif estado_actual == "EN_PRODUCCION":

            if entrada_usuario.lower() == "listo":
                print("\nSistema: cocina informó que el pedido está listo.")

                actualizar_estado_pedido(bd, pedido_actual, "LISTO")
                estado_actual = "LISTO"

                if modalidad == "Retiro":
                    print("Bot 🤖: ¡Tu pedido está listo! Podés retirarlo por el local.")
                else:
                    print("Sistema: el pedido será asignado al repartidor.")

            else:
                print("\nSistema: el pedido continúa EN_PRODUCCION.")
                print("Cocina debe escribir 'listo' cuando termine.")

        elif estado_actual == "LISTO":

            if entrada_usuario.lower() == "retirado":
                print("\nBot 🤖: Pedido entregado. ¡Gracias por elegir Burger Home!")

                actualizar_estado_pedido(bd, pedido_actual, "ENTREGADO")
                estado_actual = "ENTREGADO"
                continue

            else:
                print("\nBot 🤖: Tu pedido sigue listo para retirar.")
                print("Escribí 'retirado' cuando lo recibas.")

        elif estado_actual == "EN_REPARTO":

            if entrada_usuario.lower() == "entregado":
                print("\nSistema: el repartidor confirmó la entrega.")
                print("Bot 🤖: ¡Pedido entregado! Gracias por elegir Burger Home.")

                actualizar_estado_pedido(bd, pedido_actual, "ENTREGADO")
                estado_actual = "ENTREGADO"
                continue

            else:
                print("\nSistema: el pedido continúa EN_REPARTO.")
                print("El repartidor debe escribir 'entregado' al finalizar.")

        else:
            print("\nError: estado desconocido. Se reinicia la conversación.")
            estado_actual = "IDLE"


if __name__ == "__main__":
    ejecutar_bot()
