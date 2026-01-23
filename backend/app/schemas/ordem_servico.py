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
    tipo_os: Optional[str] = "normal"  # "normal", "rompimento", "manutencao"
    prazo_horas: Optional[int] = None  # Apenas para rompimento/manutenção
    prazo_fim: Optional[datetime] = None  # Calculado no backend se não fornecido
    porta_placa_olt: Optional[str] = None  # Para rompimento e manutenções


class OrdemServicoUpdate(BaseModel):
    """Schema for updating an OrdemServico (Admin only)"""
    status: Optional[str] = Field(None, pattern="^(aguardando|em_andamento|concluido)$")
    observacoes: Optional[str] = None
    tecnico_executor_id: Optional[int] = None


class OrdemServicoAssumirRequest(BaseModel):
    """Schema for assuming an OS"""
    tecnico_executor_id: int


class OrdemServicoFinalizarRequest(BaseModel):
    """Schema for finalizing an OS"""
    foto_comprovacao: str
    observacoes: Optional[str] = None


class TecnicoInfo(BaseModel):
    """Simplified technician schema for responses"""
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
    
    # Execution data
    foto_comprovacao: Optional[str] = None
    observacoes: Optional[str] = None
    
    # Timestamps
    criado_em: datetime
    iniciado_em: Optional[datetime] = None
    concluido_em: Optional[datetime] = None
    
    # Tipo e prazo
    tipo_os: str
    prazo_horas: Optional[int] = None
    prazo_fim: Optional[datetime] = None
    porta_placa_olt: Optional[str] = None
    tempo_restante_min: Optional[int] = None
    prazo_vencido: bool = False
    
    # Computed metrics
    tempo_espera_min: Optional[int] = None
    tempo_execucao_min: Optional[int] = None
    tempo_total_min: Optional[int] = None
    
    # Nested info
    tecnico_campo: Optional[TecnicoInfo] = None
    tecnico_executor: Optional[TecnicoInfo] = None

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
    tipo_os: str
    prazo_horas: Optional[int] = None
    prazo_fim: Optional[datetime] = None
    porta_placa_olt: Optional[str] = None
    criado_em: datetime

    class Config:
        from_attributes = True
