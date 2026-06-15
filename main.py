from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models import Document, FinanceMovement, User
from schemas import (
    DocumentCreate,
    DocumentResponse,
    FinanceMovementCreate,
    FinanceMovementResponse,
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Home Finance API", lifespan=lifespan)


# ── Auth endpoints ──────────────────────────────────────────────


@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(409, "Username already taken")
    user = User(username=data.username, password_hash=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid username or password")
    if user.disabled:
        raise HTTPException(403, "User is disabled")
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)


@app.get("/auth/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


# ── Document endpoints ──────────────────────────────────────────


@app.get("/documents", response_model=list[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


@app.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    return doc


@app.post("/documents", response_model=DocumentResponse, status_code=201)
def create_document(
    data: DocumentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    doc = Document(**data.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@app.delete("/documents/{document_id}", status_code=204)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    doc = db.get(Document, document_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    db.delete(doc)
    db.commit()


# ── Movement endpoints ──────────────────────────────────────────


@app.get("/movements", response_model=list[FinanceMovementResponse])
def list_movements(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(FinanceMovement).order_by(FinanceMovement.movement_date.desc()).all()


@app.get("/movements/{movement_id}", response_model=FinanceMovementResponse)
def get_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    mov = db.get(FinanceMovement, movement_id)
    if not mov:
        raise HTTPException(404, "Movement not found")
    return mov


@app.post("/movements", response_model=FinanceMovementResponse, status_code=201)
def create_movement(
    data: FinanceMovementCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    mov = FinanceMovement(**data.model_dump())
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return mov


@app.delete("/movements/{movement_id}", status_code=204)
def delete_movement(
    movement_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    mov = db.get(FinanceMovement, movement_id)
    if not mov:
        raise HTTPException(404, "Movement not found")
    db.delete(mov)
    db.commit()
