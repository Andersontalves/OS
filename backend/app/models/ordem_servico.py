from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class OrdemServico(Base):
    """Service Order model with status tracking and timestamps"""
    
    __tablename__ = "ordens_servico"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Identificação
    numero_os = Column(String(50), unique=True, nullable=False, index=True)
    
    # Técnico que abriu (campo)
    tecnico_campo_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Dados coletados
    foto_power_meter = Column(Text, nullable=False)  # URL Cloudinary
    foto_caixa = Column(Text, nullable=False)  # URL Cloudinary
    localizacao_lat = Column(Numeric(10, 8), nullable=True)
    localizacao_lng = Column(Numeric(11, 8), nullable=True)
    localizacao_precisao = Column(Numeric(6, 2), nullable=True)  # Em metros
    print_os_cliente = Column(Text, nullable=False)  # URL Cloudinary
    pppoe_cliente = Column(String(100), nullable=False)
    
    # Novos campos solicitados
    motivo_abertura = Column(String(50), nullable=True) # Caixa sem sinal, Ampliação, etc
    telegram_nick = Column(String(100), nullable=True)
    telegram_phone = Column(String(20), nullable=True)
    cidade = Column(String(100), nullable=True)
    
    # Status e controle
    status = Column(
        String(20),
        nullable=False,
        default="aguardando",
        index=True
    )
    
    # Técnico executor
    tecnico_executor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Tempos
    criado_em = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    iniciado_em = Column(DateTime, nullable=True)
    concluido_em = Column(DateTime, nullable=True)
    
    # Comprovação de conclusão
    foto_comprovacao = Column(Text, nullable=True)  # URL Cloudinary
    
    # Observações
    observacoes = Column(Text, nullable=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('aguardando', 'em_andamento', 'concluido')",
            name="check_status_valido"
        ),
    )
    
    # Relationships
    tecnico_campo = relationship(
        "User",
        foreign_keys=[tecnico_campo_id],
        back_populates="ordens_abertas"
    )
    tecnico_executor = relationship(
        "User",
        foreign_keys=[tecnico_executor_id],
        back_populates="ordens_executadas"
    )
    
    def __repr__(self):
        return f"<OrdemServico(numero='{self.numero_os}', status='{self.status}')>"
    
    @property
    def tempo_espera_minutos(self) -> Optional[int]:
        """Calculate waiting time in minutes (criado -> iniciado)"""
        if not self.iniciado_em or not self.criado_em:
            return None
        delta = self.iniciado_em - self.criado_em
        return int(delta.total_seconds() / 60)
    
    @property
    def tempo_execucao_minutos(self) -> Optional[int]:
        """Calculate execution time in minutes (iniciado -> concluido)"""
        if not self.concluido_em or not self.iniciado_em:
            return None
        delta = self.concluido_em - self.iniciado_em
        return int(delta.total_seconds() / 60)
    
    @property
    def tempo_total_minutos(self) -> Optional[int]:
        """Calculate total time in minutes (criado -> concluido)"""
        if not self.concluido_em or not self.criado_em:
            return None
        delta = self.concluido_em - self.criado_em
        return int(delta.total_seconds() / 60)
