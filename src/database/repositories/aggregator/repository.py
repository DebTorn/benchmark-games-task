from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Aggregator

class AggregatorRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, aggregator_id: int) -> Aggregator:
        result = await self.session.query(Aggregator) \
                .filter(Aggregator.id == aggregator_id) \
                .first()
                
        return result
    
    async def create(self, aggregator_data: dict) -> Aggregator:
        newAggregator = Aggregator(**aggregator_data)
        
        self.session.add(newAggregator)
        await self.session.commit()
        await self.session.refresh(newAggregator)
        
        return newAggregator