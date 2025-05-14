from fastapi import FastAPI
import pymongo
import json
from fastapi.responses import JSONResponse
from datetime import datetime
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from bson import ObjectId

app = FastAPI()

client = pymongo.MongoClient("mongodb+srv://emmanuel2d28:omlydwtwu9RhJWTo@sheincluster.oddfa1j.mongodb.net/shein?retryWrites=true&w=majority")
db = client["MERCADOLIBRE"]
clientes = db["clientes"]
productos = db["productos"]
tipo = db["tipo"]
app.add_middleware(
    CORSMiddleware,
    allow_origins =["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def serialize_document(doc):
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key]= value.isoformat()
        elif isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc

@app.get("/clientes/getClientes")
def get_productos():
    documents =list(clientes.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)

@app.delete("clientes/deleteClientes/{id})
def delete_clientes(id:str):
    try:
        result = clientes.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return JSONResponse(content={"mensaje": "Cliente eliminado correctamente"})
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        

@app.get("/getProductos")
def get_clientes():
    documents =list(productos.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)

@app.get("/getTipos")
def get_clientes():
    documents =list(tipo.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)

@app.get("/buscar")
def search_productos(nombre: str = None):
    query = {}
    if nombre:
        query["nombre"] = {"$regex": nombre, "$options": "i"}  # Búsqueda insensible a mayúsculas/minúsculas
    documents = list(collection.find(query))
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)
