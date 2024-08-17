from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Modelos de datos
class Paciente(BaseModel):
    id: int
    nombre: str
    edad: int
    telefono: str

class Cita(BaseModel):
    id: int
    paciente_id: int
    fecha_hora: datetime
    motivo: str

# Base de datos simulada
pacientes_db: List[Paciente] = []
citas_db: List[Cita] = []

# Rutas para gestión de pacientes
@app.post("/pacientes/", response_model=Paciente)
def crear_paciente(paciente: Paciente):
    if any(p.id == paciente.id for p in pacientes_db):
        raise HTTPException(status_code=400, detail="El paciente con este ID ya existe.")
    pacientes_db.append(paciente)
    return paciente

@app.get("/pacientes/", response_model=List[Paciente])
def listar_pacientes():
    return pacientes_db

@app.get("/pacientes/{paciente_id}", response_model=Paciente)
def obtener_paciente(paciente_id: int):
    for paciente in pacientes_db:
        if paciente.id == paciente_id:
            return paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrado.")

@app.put("/pacientes/{paciente_id}", response_model=Paciente)
def actualizar_paciente(paciente_id: int, datos_actualizados: Paciente):
    for paciente in pacientes_db:
        if paciente.id == paciente_id:
            paciente.nombre = datos_actualizados.nombre
            paciente.edad = datos_actualizados.edad
            paciente.telefono = datos_actualizados.telefono
            return paciente
    raise HTTPException(status_code=404, detail="Paciente no encontrado.")

# Rutas para gestión de citas
@app.post("/citas/", response_model=Cita)
def crear_cita(cita: Cita):
    if any(c.id == cita.id for c in citas_db):
        raise HTTPException(status_code=400, detail="La cita con este ID ya existe.")
    if not any(p.id == cita.paciente_id for p in pacientes_db):
        raise HTTPException(status_code=404, detail="Paciente no encontrado.")
    citas_db.append(cita)
    return cita

@app.get("/citas/", response_model=List[Cita])
def listar_citas():
    return citas_db

@app.get("/citas/{cita_id}", response_model=Cita)
def obtener_cita(cita_id: int):
    for cita in citas_db:
        if cita.id == cita_id:
            return cita
    raise HTTPException(status_code=404, detail="Cita no encontrada.")

@app.put("/citas/{cita_id}", response_model=Cita)
def actualizar_cita(cita_id: int, datos_actualizados: Cita):
    for cita in citas_db:
        if cita.id == cita_id:
            cita.paciente_id = datos_actualizados.paciente_id
            cita.fecha_hora = datos_actualizados.fecha_hora
            cita.motivo = datos_actualizados.motivo
            return cita
    raise HTTPException(status_code=404, detail="Cita no encontrada.")

@app.delete("/citas/{cita_id}", response_model=Cita)
def cancelar_cita(cita_id: int):
    for cita in citas_db:
        if cita.id == cita_id:
            citas_db.remove(cita)
            return cita
    raise HTTPException(status_code=404, detail="Cita no encontrada.")
