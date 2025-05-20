import pymongo
import json
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from bson import ObjectId

app = FastAPI()

client = pymongo.MongoClient("mongodb+srv://emmanuel2d28:omlydwtwu9RhJWTo@sheincluster.oddfa1j.mongodb.net/shein?retryWrites=true&w=majority")
db = client["MERCADOLIBRE"]
clientes = db["clientes"]
productos = db["productos"]
tipo = db["tipo"]
compras = db["compras"]

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
def get_clientes():
    documents =list(clientes.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)

@app.delete("/clientes/deleteClientes/{id}")
def delete_clientes(id:str):
    try:
        result = clientes.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return JSONResponse(content={"mensaje": "Cliente eliminado correctamente"})
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/clientes/createCliente")
async def create_clientes(request:Request):
    data = await request.json()
    result = clientes.insert_one(data)
    return JSONResponse(content={"mensaje": "Cliente creado", "id": str(result.inserted_id)})

@app.post("/clientes/updateClientes/{id}")
async def update_clientes(id: str, request: Request):
    try:
        data = await request.json()
        if "_id" in data:
            del data["_id"]
        result = clientes.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if result.matched_count == 1:
            return JSONResponse(content={"mensaje": "Cliente actualizado correctamente"})
        else:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        

@app.get("/productos/getProductos")
def get_productos():
    documents =list(productos.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)
    
@app.delete("/productos/deleteProductos/{id}")
def delete_productos(id:str):
    try:
        result = productos.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return JSONResponse(content={"mensaje": "Producto eliminado correctamente"})
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/productos/createProductos")
async def create_productos(request:Request):
    data =await request.json()
    result = productos.insert_one(data)
    return JSONResponse(content={"mensaje":"Producto creado", "id": str(result.inserted_id)})


@app.post("/productos/updateProductos/{id}")
async def update_producto(id: str, request: Request):
    try:
        data = await request.json()
        if "_id" in data:
            del data["_id"]
        result = productos.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if result.matched_count == 1:
            return JSONResponse(content={"mensaje": "Producto actualizado correctamente"})
        else:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/getTipos")
def get_tipos():
    documents =list(tipo.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)

@app.get("/compras/getCompras")
def get_compras():
    documents =list(compras.find())
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)

@app.post("/compras/createCompras")
async def create_compras(request:Request):
    data = await request.json()
    result = compras.insert_one(data)
    return JSONResponse(content={"mensaje": "Compra creada", "id": str(result.inserted_id)})

@app.get("/buscar")
def search_productos(nombre: str = None):
    query = {}
    if nombre:
        query["nombre"] = {"$regex": nombre, "$options": "i"}  # Búsqueda insensible a mayúsculas/minúsculas
    documents = list(productos.find(query))
    serialized_documents = [serialize_document(doc) for doc in documents]
    return JSONResponse(content=serialized_documents)
