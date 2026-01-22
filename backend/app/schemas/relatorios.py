from pydantic import BaseModel
from typing import List, Optional


# Dashboard Schemas
class DashboardTotais(BaseModel):
    """Total counts by status"""
    aguardando: int = 0
    em_andamento: int = 0
    concluido: int = 0
    total: int = 0
    # Motivo stats
    motivo_sem_sinal: int = 0
    motivo_ampliacao: int = 0
    motivo_sinal_alto: int = 0


class DashboardMetricas(BaseModel):
    """Average time metrics"""
    tempo_medio_espera_min: Optional[float] = None
    tempo_medio_execucao_min: Optional[float] = None
    tempo_medio_total_min: Optional[float] = None


class TecnicoStats(BaseModel):
    """Statistics per technician"""
    tecnico_nome: str
    total_concluidas: int
    tempo_medio_execucao_min: Optional[float] = None


class CidadeStats(BaseModel):
    """Statistics per city"""
    cidade: str
    total: int


class DashboardResponse(BaseModel):
    """Complete dashboard response"""
    totais: DashboardTotais
    metricas: DashboardMetricas
    por_tecnico: List[TecnicoStats]
    por_cidade: List[CidadeStats] = []
