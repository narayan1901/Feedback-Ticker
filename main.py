from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
import json

# Database setup
DATABASE_URL = "mysql+mysqlconnector://root:mysql@localhost/feedback_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Feedback model
class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    comment = Column(Text)
    sentiment = Column(String(50))

Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/feedback")
async def submit_feedback(name: str, comment: str, db: Session = Depends(get_db)):
    new_feedback = Feedback(name=name, comment=comment, sentiment="neutral")
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    await manager.broadcast(json.dumps({"name": name, "comment": comment, "sentiment": "neutral"}))
    return {"message": "Feedback submitted successfully"}

@app.get("/feedback")
async def get_feedback(db: Session = Depends(get_db)):
    feedback_list = db.query(Feedback).all()
    return feedback_list
