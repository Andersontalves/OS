from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


# OrdemServico Schemas
class OrdemServicoBase(BaseModel):
    """Base schema for OrdemServico"""
    pppoe_cliente: str = Field(..., max_length=100)
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


class OrdemServicoUpdate(BaseModel):
    """Schema for updating an OrdemServico (Admin only)"""
    status: Optional[str] = Field(None, pattern="^(aguardando|em_andamento|concluido)$")
    observacoes: Optional[str] = None
    tecnico_executor_id: Optional[int] = None


class OrdemServicoAssumirRequest(BaseModel):
    """Schema for assuming an OrdemServico"""
    tecnico_executor_id: int


class OrdemServicoFinalizarRequest(BaseModel):
    """Schema for finalizing an OrdemServico"""
    foto_comprovacao: str  # URL
    observacoes: Optional[str] = None


class TecnicoInfo(BaseModel):
    """Schema for technician basic info"""
    id: int
    nome: Optional[str]
    username: str
    
    class Config:
        from_attributes = True


class OrdemServicoResponse(BaseModel):
    """Schema for OrdemServico response"""
    id: int
    numero_os: str
    status: str
    
    # Técnicos
    tecnico_campo: TecnicoInfo
    tecnico_executor: Optional[TecnicoInfo] = None
    
    # Dados
    foto_power_meter: str
    foto_caixa: str
    localizacao_lat: Optional[Decimal]
    localizacao_lng: Optional[Decimal]
    localizacao_precisao: Optional[Decimal]
    print_os_cliente: str
    pppoe_cliente: str
    motivo_abertura: Optional[str] = None
    telegram_nick: Optional[str] = None
    telegram_phone: Optional[str] = None
    cidade: Optional[str] = None
    foto_comprovacao: Optional[str] = None
    observacoes: Optional[str] = None
    
    # Timestamps
    criado_em: datetime
    iniciado_em: Optional[datetime] = None
    concluido_em: Optional[datetime] = None
    
    # Computed times
    tempo_espera_min: Optional[float] = None
    tempo_execucao_min: Optional[float] = None
    tempo_total_min: Optional[float] = None
    
    class Config:
        from_attributes = True


class OrdemServicoListItem(BaseModel):
    """Simplified schema for list views"""
    id: int
    numero_os: str
    status: str
    tecnico_campo_nome: Optional[str]
    tecnico_executor_nome: Optional[str]
    criado_em: datetime
    pppoe_cliente: str
    cidade: Optional[str] = None
    
    class Config:
        from_attributes = True
