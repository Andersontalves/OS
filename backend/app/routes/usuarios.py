from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..services.auth_service import hash_password, require_role

router = APIRouter(prefix="/usuarios", tags=["Gestão de Usuários"])

@router.get("", response_model=List[UserResponse])
def list_usuarios(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """List all users (Admin only)"""
    return db.query(User).all()

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """Create a new user (Admin only)"""
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de usuário já existe"
        )
    
    new_user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
        nome=user_data.nome,
        telegram_id=user_data.telegram_id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.patch("/{user_id}", response_model=UserResponse)
def update_usuario(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """Update a user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user_data.nome is not None:
        user.nome = user_data.nome
    
    if user_data.password:
        user.password_hash = hash_password(user_data.password)
        
    # Extra fields for admin management
    if hasattr(user_data, 'role') and user_data.role:
        user.role = user_data.role
        
    if hasattr(user_data, 'username') and user_data.username:
        # Check if new username is taken
        existing = db.query(User).filter(User.username == user_data.username).first()
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Nome de usuário já está em uso")
        user.username = user_data.username

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """Delete a user (Admin only)"""
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="Você não pode excluir a si mesmo")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    db.delete(user)
    db.commit()
    return None
