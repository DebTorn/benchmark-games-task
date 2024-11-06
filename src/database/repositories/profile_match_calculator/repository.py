from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ProfileMatchCalculator

class ProfileMatchCalculatorRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, profile_match_calculator_id: int) -> ProfileMatchCalculator:
        result = await self.session.query(ProfileMatchCalculator) \
                .filter(ProfileMatchCalculator.id == profile_match_calculator_id) \
                .first()
                
        return result
    
    async def create(self, profile_matcch_calculator_data: dict) -> ProfileMatchCalculator:
        newProfileMatchCalc = ProfileMatchCalculator(**profile_matcch_calculator_data)
        
        self.session.add(newProfileMatchCalc)
        await self.session.commit()
        await self.session.refresh(newProfileMatchCalc)
        
        return newProfileMatchCalc