from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


readings = []


@app.post("/devices", status_code=201)
def create_device(device: Device):
    new_device = device.model_dump()
    readings.append(new_device)
    return new_device


@app.get("/devices")
def all_devices():
    return readings


@app.get("/devices/{name}")
def one_device(name: str):
    for device in readings:
        if device["name"] == name:
            return device
    raise HTTPException(status_code=404, detail="Device not found")


@app.put("/devices/{name}")
def update_device(name: str, device: Device):
    for i, existing in enumerate(readings):
        if existing["name"] == name:
            readings[i] = device.model_dump()
            return readings[i]
    raise HTTPException(status_code=404, detail=f"No device called {name}")



@app.delete("/devices/{name}")
def delete_device(name: str):
    for i, existing in enumerate(readings):
        if existing["name"] == name:
            readings.pop(i)
            return {"deleted": name}
    raise HTTPException(status_code=404, detail=f"No device called {name}")