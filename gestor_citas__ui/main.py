import flet as ft
import requests
from datetime import datetime

api_base_url = "http://127.0.0.1:8000"  # Ajusta si tu API está en otro puerto o IP

def main(page: ft.Page):
    page.title = "Gestión de Pacientes y Citas"

    # Contenedor con barra de desplazamiento
    container = ft.Container(
        content=ft.Column(
            controls=[],
            scroll=ft.ScrollMode.AUTO  # Permite el desplazamiento vertical
        ),
        expand=True
    )

    # Listas para mostrar pacientes y citas
    pacientes_list = ft.Column()
    citas_list = ft.Column()

    # Funciones para gestionar pacientes
    def crear_paciente(e):
        def guardar_paciente(e):
            paciente_data = {
                "id": int(paciente_id.value),
                "nombre": nombre.value,
                "edad": int(edad.value),
                "telefono": telefono.value
            }
            response = requests.post(f"{api_base_url}/pacientes/", json=paciente_data)
            if response.status_code == 200:
                listar_pacientes(None)
                dlg.open = False
                page.update()
        
        paciente_id = ft.TextField(label="ID del Paciente")
        nombre = ft.TextField(label="Nombre")
        edad = ft.TextField(label="Edad")
        telefono = ft.TextField(label="Teléfono")
        
        dlg = ft.AlertDialog(
            title=ft.Text("Crear Paciente"),
            content=ft.Column([paciente_id, nombre, edad, telefono]),
            actions=[ft.TextButton("Guardar", on_click=guardar_paciente)],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def listar_pacientes(e):
        response = requests.get(f"{api_base_url}/pacientes/")
        pacientes = response.json()
        pacientes_list.controls.clear()
        for paciente in pacientes:
            pacientes_list.controls.append(
                ft.Text(f"ID: {paciente['id']}, Nombre: {paciente['nombre']}, Edad: {paciente['edad']}, Teléfono: {paciente['telefono']}")
            )
        page.update()

    def actualizar_paciente(e):
        def guardar_cambios(e):
            paciente_data = {
                "id": int(paciente_id.value),
                "nombre": nombre.value,
                "edad": int(edad.value),
                "telefono": telefono.value
            }
            response = requests.put(f"{api_base_url}/pacientes/{paciente_id.value}", json=paciente_data)
            if response.status_code == 200:
                listar_pacientes(None)
                dlg.open = False
                page.update()

        paciente_id = ft.TextField(label="ID del Paciente")
        nombre = ft.TextField(label="Nombre")
        edad = ft.TextField(label="Edad")
        telefono = ft.TextField(label="Teléfono")

        dlg = ft.AlertDialog(
            title=ft.Text("Actualizar Paciente"),
            content=ft.Column([paciente_id, nombre, edad, telefono]),
            actions=[ft.TextButton("Guardar Cambios", on_click=guardar_cambios)],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Funciones para gestionar citas
    def crear_cita(e):
        def guardar_cita(e):
            cita_data = {
                "id": int(cita_id.value),
                "paciente_id": int(paciente_id.value),
                "fecha_hora": fecha_hora.value,
                "motivo": motivo.value
            }
            response = requests.post(f"{api_base_url}/citas/", json=cita_data)
            if response.status_code == 200:
                listar_citas(None)
                dlg.open = False
                page.update()

        cita_id = ft.TextField(label="ID de la Cita")
        paciente_id = ft.TextField(label="ID del Paciente")
        fecha_hora = ft.TextField(label="Fecha y Hora (YYYY-MM-DDTHH:MM:SS)")
        motivo = ft.TextField(label="Motivo")

        dlg = ft.AlertDialog(
            title=ft.Text("Crear Cita"),
            content=ft.Column([cita_id, paciente_id, fecha_hora, motivo]),
            actions=[ft.TextButton("Guardar", on_click=guardar_cita)],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def listar_citas(e):
        response = requests.get(f"{api_base_url}/citas/")
        citas = response.json()
        citas_list.controls.clear()
        for cita in citas:
            citas_list.controls.append(
                ft.Text(f"ID: {cita['id']}, Paciente ID: {cita['paciente_id']}, Fecha/Hora: {cita['fecha_hora']}, Motivo: {cita['motivo']}")
            )
        page.update()

    def actualizar_cita(e):
        def guardar_cambios(e):
            cita_data = {
                "id": int(cita_id.value),
                "paciente_id": int(paciente_id.value),
                "fecha_hora": fecha_hora.value,
                "motivo": motivo.value
            }
            response = requests.put(f"{api_base_url}/citas/{cita_id.value}", json=cita_data)
            if response.status_code == 200:
                listar_citas(None)
                dlg.open = False
                page.update()

        cita_id = ft.TextField(label="ID de la Cita")
        paciente_id = ft.TextField(label="ID del Paciente")
        fecha_hora = ft.TextField(label="Fecha y Hora (YYYY-MM-DDTHH:MM:SS)")
        motivo = ft.TextField(label="Motivo")

        dlg = ft.AlertDialog(
            title=ft.Text("Actualizar Cita"),
            content=ft.Column([cita_id, paciente_id, fecha_hora, motivo]),
            actions=[ft.TextButton("Guardar Cambios", on_click=guardar_cambios)],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Agregar botones y listas a la interfaz
    container.content.controls.extend([
        ft.Text("Pacientes"),
        ft.ElevatedButton("Crear Paciente", on_click=crear_paciente),
        ft.ElevatedButton("Listar Pacientes", on_click=listar_pacientes),
        ft.ElevatedButton("Actualizar Paciente", on_click=actualizar_paciente),
        pacientes_list,
        ft.Text("Citas"),
        ft.ElevatedButton("Crear Cita", on_click=crear_cita),
        ft.ElevatedButton("Listar Citas", on_click=listar_citas),
        ft.ElevatedButton("Actualizar Cita", on_click=actualizar_cita),
        citas_list,
    ])

    page.add(container)

ft.app(target=main)
