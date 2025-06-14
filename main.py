from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from database import ServerDatabase
import json

app = FastAPI()
@app.get("/")
def root():
    return {"status": "Backend is running!"}

@app.post("/update")
async def update_object(data: dict):
    obj_id = data["id"]
    state = json.dumps(data["state"])
    db.update_object_state(obj_id, state)
    return {"status": "updated", "id": obj_id}

@app.get("/objects")
def get_all_objects():
    try:
        objects = db.get_all_objects()
        return {"objects": objects}
    except Exception as e:
        print(e)

@app.post("/insert")
async def insert_object(data: dict):
    db.insert_object(
        id=data["id"],
        type=data["type"],
        position_x=data["position_x"],
        position_y=data["position_y"],
        state=json.dumps(data["state"])
    )
    return {"status": "inserted", "id": data["id"]}

@app.post("/insert")
async def insert_object(data: dict):
    db.insert_object(
        id=data["id"],
        type=data["type"],
        position_x=data["position_x"],
        position_y=data["position_y"],
        state=json.dumps(data["state"])
    )
    return {"status": "inserted", "id": data["id"]}

db = ServerDatabase()

# Allow Unity or other clients to talk cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Client connected!")

    try:
        while True:
            raw = await websocket.receive_text()
            data = json.loads(raw)

            if data["action"] == "get_all":
                objects = db.get_all_objects()
                await websocket.send_text(json.dumps({"objects": objects}))
                continue

            elif data["action"] == "update":
                obj_id = data["id"]
                state = json.dumps(data["state"])  # assuming state is dict
                db.update_object_state(obj_id, state)
                await websocket.send_text(json.dumps({"status": "updated", "id": obj_id}))

            elif data["action"] == "insert":
                db.insert_object(data["id"], data["type"], json.dumps(data["state"]))
                await websocket.send_text(json.dumps({"status": "inserted", "id": data["id"]}))

    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()