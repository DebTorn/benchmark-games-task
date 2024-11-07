from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from src.config.database import get_session
from src.database.repositories.report import ReportRepository
import decimal

router = APIRouter()

@router.get("/competency")
async def filter_by_competency(
    identifier: str, 
    min_value: decimal.Decimal,
    limit: Optional[int] = 10,
    session: Session = Depends(get_session)
):
    reportRepo = ReportRepository(session)

    results = reportRepo.getReportsByPredictionValue(identifier, min_value, limit)
    return results

@router.get("/profile-match")
async def filter_by_profile_match(
    calculator_id: int,
    min_value: decimal.Decimal,
    limit: Optional[int] = 10,
    session: Session = Depends(get_session)
):
    reportRepo = ReportRepository(session)

    results = reportRepo.getReportsByProfileMatchCalculatorValue(calculator_id, min_value, limit)
    return results

@router.get("/reports/{type}")
async def filter_by_report_link_type(
    type: str,
    limit: Optional[int] = 10,
    session: Session = Depends(get_session)
):
    reportRepo = ReportRepository(session)

    if type not in ["error", "warning"]:
        raise HTTPException(status_code=400, detail="Invalid report type")
    
    results = []
    
    if type == "error":
        results = reportRepo.getAllErroredReports(limit)
    elif type == "warning":
        results = reportRepo.getAllWarningedReports(limit)

    return results