from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import PredictionReport

class PredictionReportRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, prediction_report_id: int) -> PredictionReport:
        result = await self.session.query(PredictionReport) \
                .filter(PredictionReport.id == prediction_report_id) \
                .first()
                
        return result
    
    async def create(self, prediction_report_data: dict) -> PredictionReport:
        newPredictionReport = PredictionReport(**prediction_report_data)
        
        self.session.add(newPredictionReport)
        await self.session.commit()
        await self.session.refresh(newPredictionReport)
        
        return newPredictionReport