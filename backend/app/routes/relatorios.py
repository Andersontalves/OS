from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.ordem_servico import OrdemServico
from ..schemas.relatorios import (
    DashboardResponse,
    DashboardTotais,
    DashboardMetricas,
    TecnicoStats
)
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard statistics and metrics
    
    Returns:
    - Total counts by status
    - Average times (espera, execução, total)
    - Statistics per technician
    """
    # Total counts by status
    totais_query = (
        db.query(
            OrdemServico.status,
            func.count(OrdemServico.id).label("count")
        )
        .group_by(OrdemServico.status)
        .all()
    )
    
    totais_dict = {row.status: row.count for row in totais_query}
    total_geral = sum(totais_dict.values())
    
    totais = DashboardTotais(
        aguardando=totais_dict.get("aguardando", 0),
        em_andamento=totais_dict.get("em_andamento", 0),
        concluido=totais_dict.get("concluido", 0),
        total=total_geral
    )
    
    # Average times (only for completed OS)
    avg_times = (
        db.query(
            func.avg(
                func.extract('epoch', OrdemServico.iniciado_em - OrdemServico.criado_em) / 60
            ).label("tempo_espera"),
            func.avg(
                func.extract('epoch', OrdemServico.concluido_em - OrdemServico.iniciado_em) / 60
            ).label("tempo_execucao"),
            func.avg(
                func.extract('epoch', OrdemServico.concluido_em - OrdemServico.criado_em) / 60
            ).label("tempo_total")
        )
        .filter(OrdemServico.status == "concluido")
        .first()
    )
    
    metricas = DashboardMetricas(
        tempo_medio_espera_min=float(avg_times.tempo_espera) if avg_times.tempo_espera else None,
        tempo_medio_execucao_min=float(avg_times.tempo_execucao) if avg_times.tempo_execucao else None,
        tempo_medio_total_min=float(avg_times.tempo_total) if avg_times.tempo_total else None
    )
    
    # Stats per technician
    tecnico_stats = (
        db.query(
            User.nome,
            func.count(OrdemServico.id).label("total"),
            func.avg(
                func.extract('epoch', OrdemServico.concluido_em - OrdemServico.iniciado_em) / 60
            ).label("tempo_medio")
        )
        .join(OrdemServico, OrdemServico.tecnico_executor_id == User.id)
        .filter(OrdemServico.status == "concluido")
        .group_by(User.id, User.nome)
        .all()
    )
    
    por_tecnico = [
        TecnicoStats(
            tecnico_nome=row.nome or "Sem nome",
            total_concluidas=row.total,
            tempo_medio_execucao_min=float(row.tempo_medio) if row.tempo_medio else None
        )
        for row in tecnico_stats
    ]
    
    return DashboardResponse(
        totais=totais,
        metricas=metricas,
        por_tecnico=por_tecnico
    )
