from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Document, FinanceMovement
from schemas import (
    DocumentCreate,
    DocumentResponse,
    FinanceMovementCreate,
    FinanceMovementResponse,
)

app = FastAPI(title="Home Finance API")


@app.get("/documents", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


@app.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc


@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(data: DocumentCreate, db: Session = Depends(get_db)):
    doc = Document(**data.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@app.delete("/documents/{document_id}", status_code=204)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    db.delete(doc)
    db.commit()


@app.get("/movements", response_model=list[FinanceMovementResponse])
def list_movements(db: Session = Depends(get_db)):
    return db.query(FinanceMovement).order_by(FinanceMovement.movement_date.desc()).all()


@app.get("/movements/{movement_id}", response_model=FinanceMovementResponse)
def get_movement(movement_id: int, db: Session = Depends(get_db)):
    mov = db.get(FinanceMovement, movement_id)
    if not mov:
        raise HTTPException(404, "Movement not found")
    return mov


@app.post("/movements", response_model=FinanceMovementResponse, status_code=201)
def create_movement(data: FinanceMovementCreate, db: Session = Depends(get_db)):
    mov = FinanceMovement(**data.model_dump())
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov


@app.delete("/movements/{movement_id}", status_code=204)
def delete_movement(movement_id: int, db: Session = Depends(get_db)):
    mov = db.get(FinanceMovement, movement_id)
    if not mov:
        raise HTTPException(404, "Movement not found")
    db.delete(mov)
    db.commit()
