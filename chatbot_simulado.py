import json
import os

# --- FUNCIONES DE PERSISTENCIA (BASE DE DATOS SIMULADA) ---
def cargar_bd():
    """Lee el archivo JSON para simular consultas en tiempo real"""
    if os.path.exists("base_datos.json"):
        with open("base_datos.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_bd(data):
    """Guarda las modificaciones en el JSON para persistir los datos"""
    with open("base_datos.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- SIMULADOR DEL CHATBOT ---
def ejecutar_bot():
    bd = cargar_bd()
    
    # Variables de estado conversacional (Memoria del Bot)
    estado_actual = "IDLE" 
    carrito = {}
    modalidad = None
    direccion = None

    print("=== SIMULADOR DE CHATBOT AUTOMATIZADO - BURGER HOME ===")
    print("Para iniciar el flujo, simula enviar un mensaje (Ej: 'Hola'). Para salir, escribe 'salir'.\n")

    while True:
        # Tarea de Usuario: Captura de entrada por consola
        entrada_usuario = input("Cliente 👤: ").strip()
        
        # En caso de querer salir de la simulación de consola
        if entrada_usuario.lower() == "salir":
            break

        # --- MÁQUINA DE ESTADOS (Mapeo de Compuertas y Tareas de Servicio) ---
        
        if estado_actual == "IDLE":
            # Tarea de Servicio: Saludo y Despliegue de Menú Dinámico
            print("\nBot ⚙️: ¡Hola! Bienvenido a Burger Home. Este es nuestro menú disponible:")
            for id_prod, info in bd["productos"].items():
                print(f"  [{id_prod}] {info['nombre']} - ${info['precio']} (Stock: {info['stock']})")
            print("Por favor, ingresá el número del combo que querés pedir.")
            estado_actual = "ESPERANDO_PRODUCTO"

        elif estado_actual == "ESPERANDO_PRODUCTO":
            # ROBUSTEZ (Camino Infeliz): Validar si ingresó una opción válida
            if entrada_usuario not in bd["productos"]:
                print("\nBot ⚙️: Opción inválida. Por favor, ingresá una opcion válida del menú.")
                continue # Mantiene el flujo atrapado en el mismo estado

            producto_seleccionado = bd["productos"][entrada_usuario]
            
            # COMPUERTA COMPLEJA: ¿Hay stock disponible?
            if producto_seleccionado["stock"] <= 0:
                print(f"\nBot ⚙️: Disculpame, nos quedamos sin stock de {producto_seleccionado['nombre']}.")
                print("Fin de la simulación: Pedido Cancelado.")
                estado_actual = "IDLE"
                break
            
            # Camino Feliz: Guardar en carrito temporal
            carrito = {
                "id": entrada_usuario,
                "nombre": producto_seleccionado["nombre"],
                "precio": producto_seleccionado["precio"]
            }
            
            print(f"\nBot ⚙️: Seleccionaste {carrito['nombre']}.")
            print("¿Cómo preferís tu pedido? Ingresá:\n [1] Delivery\n [2] Retiro en Local")
            estado_actual = "ESPERANDO_MODALIDAD"

        elif estado_actual == "ESPERANDO_MODALIDAD":
            # COMPUERTA EXCLUSIVA: ¿Es Delivery?
            if entrada_usuario == "1":
                modalidad = "Delivery"
                print("\nBot ⚙️: Por favor, ingresá tu barrio para verificar si tenemos cobertura:")
                estado_actual = "ESPERANDO_DIRECCION"
            elif entrada_usuario == "2":
                modalidad = "Retiro"
                # Salta directo a calcular importe (Igual que en el BPMN)
                print(f"\nBot ⚙️: Perfecto. El total a abonar es: ${carrito['precio']}.")
                print("¿Cómo vas a pagar?\n [1] Efectivo\n [2] Transferencia Bancaria")
                estado_actual = "ESPERANDO_PAGO"
            else:
                print("\nBot ⚙️: Opción inválida. Ingresá 1 para Delivery o 2 para Retiro.")

        elif estado_actual == "ESPERANDO_DIRECCION":
            # Tarea de Servicio: Validar Zona de Cobertura
            barrio = entrada_usuario.lower()
            
            # COMPUERTA EXCLUSIVA: ¿Zona en cobertura?
            if barrio in bd["zonas_cobertura"]:
                direccion = entrada_usuario
                print(f"\nBot ⚙️: ¡Genial! {entrada_usuario} está en nuestra zona de cobertura.")
                print(f"El total a abonar es: ${carrito['precio']}.")
                print("¿Cómo vas a pagar?\n [1] Efectivo\n [2] Transferencia Bancaria")
                estado_actual = "ESPERANDO_PAGO"
            else:
                print(f"\nBot ⚙️: Lo lamento, no llegamos hasta {entrada_usuario} con nuestros repartidores.")
                print("Fin de la simulación: Pedido Cancelado por falta de cobertura.")
                estado_actual = "IDLE"
                break

        elif estado_actual == "ESPERANDO_PAGO":
            if entrada_usuario == "1":
                print("\nBot ⚙️: ¡Pedido confirmado! Abonás al recibir/retirar.")
                # TAREA DE SERVICIO: Confirmar pedido, descontar stock y guardar en DB
                bd["productos"][carrito["id"]]["stock"] -= 1
                
                nuevo_pedido = {"producto": carrito["nombre"], "modalidad": modalidad, "pago": "Efectivo", "direccion": direccion}
                bd["pedidos_registrados"].append(nuevo_pedido)
                guardar_bd(bd) # Persistencia real en el JSON
                
                print("--- ALERTA A COCINA 🍳 ---: Pedido enviado a producción de forma automática.")
                print("Fin de la simulación del sistema automatizado.")
                break
            elif entrada_usuario == "2":
                print("\nBot ⚙️: Por favor, simula adjuntar tu comprobante (Escribí cualquier palabra para simular la carga del archivo):")
                estado_actual = "ESPERANDO_COMPROBANTE"
            else:
                print("\nBot ⚙️: Opción inválida. Seleccioná 1 para Efectivo o 2 para Transferencia.")

        elif estado_actual == "ESPERANDO_COMPROBANTE":
            # ROBUSTEZ (Camino Infeliz): Validación simulada de archivo
            if len(entrada_usuario) < 3:
                print("\nBot ⚙️: Error: El comprobante parece inválido o ilegible. Por favor, cargalo de nuevo:")
                continue # Bucle de reintento del comprobante
            
            print("\nBot ⚙️: Comprobante validado con éxito.")
            # TAREA DE SERVICIO: Confirmar pedido, descontar stock y guardar en DB
            bd["productos"][carrito["id"]]["stock"] -= 1
            
            nuevo_pedido = {"producto": carrito["nombre"], "modalidad": modalidad, "pago": "Transferencia", "direccion": direccion}
            bd["pedidos_registrados"].append(nuevo_pedido)
            guardar_bd(bd) # Persistencia real en el JSON
            
            print("--- ALERTA A COCINA 🍳 ---: Comprobante verificado. Pedido enviado a producción.")
            print("Fin de la simulación del sistema automatizado.")
            break

if __name__ == "__main__":
    ejecutar_bot()