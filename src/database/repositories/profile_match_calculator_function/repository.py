from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ProfileMatchCalculatorFunction

class ProfileMatchCalculatorFunctionRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, prof_match_calc_func_id: int) -> ProfileMatchCalculatorFunction:
        result = await self.session.query(ProfileMatchCalculatorFunction) \
                .filter(ProfileMatchCalculatorFunction.id == prof_match_calc_func_id) \
                .first()
                
        return result
    
    async def create(self, prof_match_calc_func_data: dict) -> ProfileMatchCalculatorFunction:
        newProfMatchCalcFunc = ProfileMatchCalculatorFunction(**prof_match_calc_func_data)
        
        self.session.add(newProfMatchCalcFunc)
        await self.session.commit()
        await self.session.refresh(newProfMatchCalcFunc)
        
        return newProfMatchCalcFunc