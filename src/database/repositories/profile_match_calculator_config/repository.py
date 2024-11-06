from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ProfileMatchCalculatorConfigs

class AggregatorRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, profile_match_calculator_config_id: int) -> ProfileMatchCalculatorConfigs:
        result = await self.session.query(ProfileMatchCalculatorConfigs) \
                .filter(ProfileMatchCalculatorConfigs.id == profile_match_calculator_config_id) \
                .first()
                
        return result
    
    async def create(self, profile_match_calculator_config_data: dict) -> ProfileMatchCalculatorConfigs:
        newProfileMatchCalcConf = ProfileMatchCalculatorConfigs(**profile_match_calculator_config_data)
        
        self.session.add(newProfileMatchCalcConf)
        await self.session.commit()
        await self.session.refresh(newProfileMatchCalcConf)
        
        return newProfileMatchCalcConf