from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
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
    foto_power_meter = Column(Text, nullable=True)  # URL Cloudinary (opcional para rompimento/manutenção)
    foto_caixa = Column(Text, nullable=False)  # URL Cloudinary
    localizacao_lat = Column(Numeric(10, 8), nullable=True)
    localizacao_lng = Column(Numeric(11, 8), nullable=True)
    localizacao_precisao = Column(Numeric(6, 2), nullable=True)  # Em metros
    print_os_cliente = Column(Text, nullable=True)  # URL Cloudinary (opcional para rompimento/manutenção)
    pppoe_cliente = Column(String(100), nullable=True)  # Opcional para rompimento
    
    # Novos campos solicitados
    motivo_abertura = Column(String(50), nullable=True) # Caixa sem sinal, Ampliação, etc
    telegram_nick = Column(String(100), nullable=True)
    telegram_phone = Column(String(20), nullable=True)
    cidade = Column(String(100), nullable=True)
    
    # Tipo de O.S e prazo (para rompimento e manutenções)
    tipo_os = Column(
        String(20),
        nullable=False,
        default="normal",
        index=True
    )  # Valores: "normal", "rompimento", "manutencao"
    prazo_horas = Column(Integer, nullable=True)  # Prazo em horas
    prazo_fim = Column(DateTime, nullable=True)  # Data/hora limite calculada
    porta_placa_olt = Column(String(50), nullable=True)  # Porta da placa/Porta da OLT
    
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
        CheckConstraint(
            "tipo_os IN ('normal', 'rompimento', 'manutencao')",
            name="check_tipo_os_valido"
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
    
    @property
    def tempo_restante_minutos(self) -> Optional[int]:
        """Tempo restante até o prazo (apenas para rompimento/manutenção)"""
        if not self.prazo_fim or self.tipo_os == "normal":
            return None
        agora = datetime.utcnow()
        if agora > self.prazo_fim:
            return 0  # Prazo vencido
        delta = self.prazo_fim - agora
        return int(delta.total_seconds() / 60)
    
    @property
    def prazo_vencido(self) -> bool:
        """Verifica se o prazo foi vencido"""
        if not self.prazo_fim or self.tipo_os == "normal":
            return False
        return datetime.utcnow() > self.prazo_fim
