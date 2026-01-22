from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class OrdemServicoBase(BaseModel):
    """Base schema for OrdemServico"""
    tecnico_campo_id: Optional[int] = None
    status: Optional[str] = "aguardando"
    observacoes: Optional[str] = None


class OrdemServicoCreate(BaseModel):
    """Schema for creating an OrdemServico"""
    tecnico_campo_id: int
    foto_power_meter: str  # URL
    foto_caixa: str  # URL
    localizacao_lat: Optional[Decimal] = None
    localizacao_lng: Optional[Decimal] = None
    localizacao_precisao: Optional[Decimal] = None
    print_os_cliente: str  # URL
    pppoe_cliente: str = Field(..., max_length=100)
    motivo_abertura: Optional[str] = None
    telegram_nick: Optional[str] = None
    telegram_phone: Optional[str] = None
    cidade: Optional[str] = None


class OrdemServicoUpdate(BaseModel):
    """Schema for updating an OrdemServico (Admin only)"""
    status: Optional[str] = Field(None, pattern="^(aguardando|em_andamento|concluido)$")
    observacoes: Optional[str] = None
    tecnico_executor_id: Optional[int] = None


class UserSimple(BaseModel):
    """Simplified technician schema"""
    id: int
    nome: Optional[str] = None
    username: str

    class Config:
        from_attributes = True


class OrdemServicoResponse(BaseModel):
    """Schema for returning OrdemServico details"""
    id: int
    numero_os: str
    status: str
    tecnico_campo_id: int
    tecnico_executor_id: Optional[int] = None
    
    # Photos and location
    foto_power_meter: str
    foto_caixa: str
    localizacao_lat: Optional[Decimal] = None
    localizacao_lng: Optional[Decimal] = None
    localizacao_precisao: Optional[Decimal] = None
    print_os_cliente: str
    pppoe_cliente: str
    motivo_abertura: Optional[str] = None
    telegram_nick: Optional[str] = None
    telegram_phone: Optional[str] = None
    cidade: Optional[str] = None
    
    # Timestamps
    criado_em: datetime
    iniciado_em: Optional[datetime] = None
    concluido_em: Optional[datetime] = None
    observacoes: Optional[str] = None
    
    # Nested info
    tecnico_campo: Optional[UserSimple] = None
    tecnico_executor: Optional[UserSimple] = None

    class Config:
        from_attributes = True


class OrdemServicoListItem(BaseModel):
    """Schema for a simplified OS in a list"""
    id: int
    numero_os: str
    status: str
    tecnico_campo_nome: Optional[str] = None
    tecnico_executor_nome: Optional[str] = None
    pppoe_cliente: str
    motivo_abertura: Optional[str] = None
    cidade: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
