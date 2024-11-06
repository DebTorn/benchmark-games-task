from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ReportLink

class ReportLinkRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, report_link_id: int) -> ReportLink:
        result = await self.session.query(ReportLink) \
                .filter(ReportLink.id == report_link_id) \
                .first()
                
        return result
    
    async def create(self, report_link_data: dict) -> ReportLink:
        newReportLink = ReportLink(**report_link_data)
        
        self.session.add(newReportLink)
        await self.session.commit()
        await self.session.refresh(newReportLink)
        
        return newReportLink