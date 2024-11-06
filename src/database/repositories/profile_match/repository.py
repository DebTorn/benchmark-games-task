from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import ProfileMatch

class ProfileMatchRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, prof_match_id: int) -> ProfileMatch:
        result = await self.session.query(ProfileMatch) \
                .filter(ProfileMatch.id == prof_match_id) \
                .first()
                
        return result
    
    async def create(self, prof_match_data: dict) -> ProfileMatch:
        newProfileMatch = ProfileMatch(**prof_match_data)
        
        self.session.add(newProfileMatch)
        await self.session.commit()
        await self.session.refresh(newProfileMatch)
        
        return newProfileMatch