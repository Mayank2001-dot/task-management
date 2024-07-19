from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from enum import Enum

app = FastAPI()

@app.get('/')
async def check():
    return 'hello'

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic Schemas
class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class ManagementBase(BaseModel):
    title: str
    description: str
    status: StatusEnum

class ManagementCreate(ManagementBase):
    pass

class ManagementUpdate(ManagementBase):
    pass

class Management(ManagementBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

# CRUD Operations
@app.get("/managements/", response_model=List[Management])
async def read_managements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    managements = db.query(models.Management).offset(skip).limit(limit).all()
    return managements

@app.get("/managements/{management_id}", response_model=Management)
async def read_management(management_id: int, db: Session = Depends(get_db)):
    management = db.query(models.Management).filter(models.Management.id == management_id).first()
    if management is None:
        raise HTTPException(status_code=404, detail="Management not found")
    return management

@app.post("/managements/", response_model=Management)
async def create_management(management: ManagementCreate, db: Session = Depends(get_db)):
    db_management = models.Management(**management.dict())
    db.add(db_management)
    db.commit()
    db.refresh(db_management)
    return db_management

@app.put("/managements/{management_id}", response_model=Management)
async def update_management(management_id: int, management: ManagementUpdate, db: Session = Depends(get_db)):
    db_management = db.query(models.Management).filter(models.Management.id == management_id).first()
    if db_management is None:
        raise HTTPException(status_code=404, detail="Management not found")
    for key, value in management.dict().items():
        setattr(db_management, key, value)
    db.commit()
    db.refresh(db_management)
    return db_management

@app.delete("/managements/{management_id}", response_model=Management)
async def delete_management(management_id: int, db: Session = Depends(get_db)):
    db_management = db.query(models.Management).filter(models.Management.id == management_id).first()
    if db_management is None:
        raise HTTPException(status_code=404, detail="Management not found")
    db.delete(db_management)
    db.commit()
    return db_management
