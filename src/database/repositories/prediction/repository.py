from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Prediction

class PredictionRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, prediction_id: int) -> Prediction:
        result = await self.session.query(Prediction) \
                .filter(Prediction.id == prediction_id) \
                .first()
                
        return result
    
    async def create(self, predicition_data: dict) -> Prediction:
        newPrediction = Prediction(**predicition_data)
        
        self.session.add(newPrediction)
        await self.session.commit()
        await self.session.refresh(newPrediction)
        
        return newPrediction