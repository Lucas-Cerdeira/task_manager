from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.auth import UserAuth, UserRegister, Token
from app.schemas.user import UserResponse
from app.models.user import User
from app.security.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.
    
    Args:
        user_data: Dados do usuário a ser registrado
        db: Sessão do banco de dados
    
    Returns:
        UserResponse: Dados do usuário criado
    
    Raises:
        HTTPException: Se o email já estiver em uso
    """
    # Verifica se o email já existe
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Cria o usuário com a senha hasheada
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        senha_hash=hashed_password,
        nome=user_data.nome,
        sobrenome=user_data.sobrenome
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login(user_data: UserAuth, db: Session = Depends(get_db)):
    """
    Autentica um usuário e retorna um token JWT.
    
    Args:
        user_data: Credenciais do usuário
        db: Sessão do banco de dados
    
    Returns:
        Token: Token de acesso JWT
    
    Raises:
        HTTPException: Se as credenciais forem inválidas
    """
    # Busca o usuário pelo email
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

@router.post("/logout")
async def logout():
    """
    Realiza o logout do usuário (cliente deve descartar o token).
    
    Returns:
        dict: Mensagem de sucesso
    """
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado.
    
    Args:
        current_user: Usuário atual (injetado pela dependência)
    
    Returns:
        UserResponse: Dados do usuário autenticado
    """
    return current_user
