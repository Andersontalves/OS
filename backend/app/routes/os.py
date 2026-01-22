from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models.user import User
from ..models.ordem_servico import OrdemServico
from ..schemas.ordem_servico import (
    OrdemServicoCreate,
    OrdemServicoResponse,
    OrdemServicoListItem,
    OrdemServicoUpdate,
    OrdemServicoAssumirRequest,
    OrdemServicoFinalizarRequest,
    TecnicoInfo
)
from ..services.auth_service import get_current_user, require_role
from ..services.cloudinary_service import upload_image

router = APIRouter(prefix="/os", tags=["Ordens de Serviço"])


def _generate_numero_os(db: Session) -> str:
    """Generate next OS number (OS-YYYY-NNN)"""
    today = datetime.now()
    year = today.year
    
    # Get last OS number for this year
    last_os = (
        db.query(OrdemServico)
        .filter(OrdemServico.numero_os.like(f"OS-{year}-%"))
        .order_by(desc(OrdemServico.numero_os))
        .first()
    )
    
    if last_os:
        # Extract number from OS-YYYY-NNN
        last_number = int(last_os.numero_os.split("-")[-1])
        next_number = last_number + 1
    else:
        next_number = 1
    
    return f"OS-{year}-{next_number:03d}"


@router.post("", response_model=OrdemServicoResponse, status_code=status.HTTP_201_CREATED)
def create_os(
    os_data: OrdemServicoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new Ordem de Serviço (Service Order)
    
    This endpoint is typically called by the Telegram bot when a field technician submits a new OS.
    """
    # Verify that the tecnico_campo exists
    tecnico = db.query(User).filter(User.id == os_data.tecnico_campo_id).first()
    if not tecnico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Técnico de campo não encontrado"
        )
    
    # Generate OS number
    numero_os = _generate_numero_os(db)
    
    # Create OS
    new_os = OrdemServico(
        numero_os=numero_os,
        tecnico_campo_id=os_data.tecnico_campo_id,
        foto_power_meter=os_data.foto_power_meter,
        foto_caixa=os_data.foto_caixa,
        localizacao_lat=os_data.localizacao_lat,
        localizacao_lng=os_data.localizacao_lng,
        localizacao_precisao=os_data.localizacao_precisao,
        print_os_cliente=os_data.print_os_cliente,
        pppoe_cliente=os_data.pppoe_cliente,
        motivo_abertura=os_data.motivo_abertura,
        telegram_nick=os_data.telegram_nick,
        telegram_phone=os_data.telegram_phone,
        cidade=os_data.cidade,
        status="aguardando"
    )
    
    db.add(new_os)
    db.commit()
    db.refresh(new_os)
    
    return _format_os_response(new_os)


@router.get("", response_model=List[OrdemServicoListItem])
def list_os(
    status_filter: Optional[str] = Query(None, description="Filtrar por status"),
    tecnico_executor_id: Optional[int] = Query(None, description="Filtrar por técnico executor"),
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List Ordens de Serviço with optional filters
    
    - **status_filter**: Filter by status (aguardando, em_andamento, concluido)
    - **tecnico_executor_id**: Filter by executor technician
    - **limit**: Maximum number of results (max 200)
    - **offset**: Pagination offset
    """
    query = db.query(OrdemServico)
    
    # Apply filters
    if status_filter:
        query = query.filter(OrdemServico.status == status_filter)
    
    if tecnico_executor_id:
        query = query.filter(OrdemServico.tecnico_executor_id == tecnico_executor_id)
    
    # Role-based filtering
    if current_user.role == "execucao":
        # Execution role can only see:
        # - OS with status "aguardando"
        # - Their own OS (em_andamento or concluido)
        query = query.filter(
            (OrdemServico.status == "aguardando") |
            (OrdemServico.tecnico_executor_id == current_user.id)
        )
    
    # Order by creation date (newest first)
    query = query.order_by(desc(OrdemServico.criado_em))
    
    # Pagination
    results = query.offset(offset).limit(limit).all()
    
    # Format response
    return [
        OrdemServicoListItem(
            id=os.id,
            numero_os=os.numero_os,
            status=os.status,
            tecnico_campo_nome=(os.tecnico_campo.nome or os.tecnico_campo.username) if os.tecnico_campo else None,
            tecnico_executor_nome=(os.tecnico_executor.nome or os.tecnico_executor.username) if os.tecnico_executor else None,
            criado_em=os.criado_em,
            pppoe_cliente=os.pppoe_cliente,
            cidade=os.cidade
        )
        for os in results
    ]


@router.get("/{os_id}", response_model=OrdemServicoResponse)
def get_os(
    os_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get details of a specific Ordem de Serviço
    """
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    
    if not os:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada"
        )
    
    # Check permissions
    if current_user.role == "execucao":
        # Execution can only view aguardando or their own OS
        if os.status != "aguardando" and os.tecnico_executor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para visualizar esta O.S"
            )
    
    return _format_os_response(os)


@router.patch("/{os_id}/assumir", response_model=OrdemServicoResponse)
def assumir_os(
    os_id: int,
    request: OrdemServicoAssumirRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "execucao"))
):
    """
    Assume an Ordem de Serviço (change status to em_andamento)
    
    Only allowed for users with role 'execucao' or 'admin'.
    The OS must be in 'aguardando' status.
    """
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    
    if not os:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada"
        )
    
    # Check if OS is available
    if os.status != "aguardando":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esta O.S não pode ser assumida. Status atual: {os.status}"
        )
    
    # Verify that tecnico_executor exists
    tecnico = db.query(User).filter(User.id == request.tecnico_executor_id).first()
    if not tecnico or tecnico.role not in ["execucao", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Técnico executor inválido"
        )
    
    # Update OS
    os.status = "em_andamento"
    os.tecnico_executor_id = request.tecnico_executor_id
    os.iniciado_em = datetime.utcnow()
    
    db.commit()
    db.refresh(os)
    
    return _format_os_response(os)


@router.patch("/{os_id}/finalizar", response_model=OrdemServicoResponse)
def finalizar_os(
    os_id: int,
    request: OrdemServicoFinalizarRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "execucao"))
):
    """
    Finalize an Ordem de Serviço (change status to concluido)
    
    Only allowed for users with role 'execucao' (for their own OS) or 'admin'.
    Requires a foto_comprovacao (proof photo).
    """
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    
    if not os:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada"
        )
    
    # Check if OS can be finalized
    if os.status != "em_andamento":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esta O.S não pode ser finalizada. Status atual: {os.status}"
        )
    
    # Check permissions
    if current_user.role == "execucao" and os.tecnico_executor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode finalizar suas próprias O.S"
        )
    
    # Update OS
    os.status = "concluido"
    os.foto_comprovacao = request.foto_comprovacao
    os.concluido_em = datetime.utcnow()
    
    if request.observacoes:
        os.observacoes = request.observacoes
    
    db.commit()
    db.refresh(os)
    
    return _format_os_response(os)


@router.patch("/{os_id}/finalizar-com-foto", response_model=OrdemServicoResponse)
async def finalizar_os_com_foto(
    os_id: int,
    foto_comprovacao: UploadFile = File(...),
    observacoes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin", "execucao"))
):
    """
    Finalize an Ordem de Serviço with direct file upload (change status to concluido)
    
    This replaces the need for a pre-uploaded image URL.
    """
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    
    if not os:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada"
        )
    
    # Check if OS can be finalized
    if os.status != "em_andamento":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Esta O.S não pode ser finalizada. Status atual: {os.status}"
        )
    
    # Check permissions
    if current_user.role == "execucao" and os.tecnico_executor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode finalizar suas próprias O.S"
        )
    
    # Upload photo to Cloudinary
    foto_url = await upload_image(foto_comprovacao, folder="os-sistema/comprovacao")
    
    # Update OS
    os.status = "concluido"
    os.foto_comprovacao = foto_url
    os.concluido_em = datetime.utcnow()
    
    if observacoes:
        os.observacoes = observacoes
    
    db.commit()
    db.refresh(os)
    
    return _format_os_response(os)


@router.patch("/{os_id}", response_model=OrdemServicoResponse)
def update_os(
    os_id: int,
    os_update: OrdemServicoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Update an Ordem de Serviço (Admin only)
    
    Admins can edit any OS, including changing status and observations.
    """
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    
    if not os:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada"
        )
    
    # Update fields
    if os_update.status is not None:
        os.status = os_update.status
    
    if os_update.observacoes is not None:
        os.observacoes = os_update.observacoes
    
    if os_update.tecnico_executor_id is not None:
        os.tecnico_executor_id = os_update.tecnico_executor_id
    
    db.commit()
    db.refresh(os)
    
    return _format_os_response(os)


@router.delete("/{os_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_os(
    os_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Delete an Ordem de Serviço (Admin only)
    """
    os = db.query(OrdemServico).filter(OrdemServico.id == os_id).first()
    
    if not os:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ordem de serviço não encontrada"
        )
    
    db.delete(os)
    db.commit()
    
    return None


def _format_os_response(os: OrdemServico) -> OrdemServicoResponse:
    """Helper function to format OS response with computed fields"""
    return OrdemServicoResponse(
        id=os.id,
        numero_os=os.numero_os,
        status=os.status,
        tecnico_campo=TecnicoInfo.from_orm(os.tecnico_campo),
        tecnico_executor=TecnicoInfo.from_orm(os.tecnico_executor) if os.tecnico_executor else None,
        foto_power_meter=os.foto_power_meter,
        foto_caixa=os.foto_caixa,
        localizacao_lat=os.localizacao_lat,
        localizacao_lng=os.localizacao_lng,
        localizacao_precisao=os.localizacao_precisao,
        print_os_cliente=os.print_os_cliente,
        pppoe_cliente=os.pppoe_cliente,
        motivo_abertura=os.motivo_abertura,
        telegram_nick=os.telegram_nick,
        telegram_phone=os.telegram_phone,
        foto_comprovacao=os.foto_comprovacao,
        observacoes=os.observacoes,
        criado_em=os.criado_em,
        iniciado_em=os.iniciado_em,
        concluido_em=os.concluido_em,
        tempo_espera_min=os.tempo_espera_minutos,
        tempo_execucao_min=os.tempo_execucao_minutos,
        tempo_total_min=os.tempo_total_minutos
    )
