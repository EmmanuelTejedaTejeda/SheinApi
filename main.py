from fastapi import FastAPI
import pymongo
import json
from fastapi.responses import JSONResponse
from datetime import datetime
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = pymongo.MongoClient("mongodb+srv://emmanuel2d28:omlydwtwu9RhJWTo@sheincluster.oddfa1j.mongodb.net/shein?retryWrites=true&w=majority")
db = client["shein"]
collection = db["shein_db"]
clientes = db["clientes"]

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

@app.get("/getProductos")
def get_productos():
    documents =list(collection.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)

@app.get("/getClientes")
def get_clientes():
    documents =list(clientes.find())
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
