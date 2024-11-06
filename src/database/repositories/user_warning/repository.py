from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import UserWarning

class UserWarningRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, user_warning_id: int) -> UserWarning:
        result = await self.session.query(UserWarning) \
                .filter(UserWarning.id == user_warning_id) \
                .first()
                
        return result
    
    async def create(self, user_warning_data: dict) -> UserWarning:
        newUserWarning = UserWarning(**user_warning_data)
        
        self.session.add(newUserWarning)
        await self.session.commit()
        await self.session.refresh(newUserWarning)
        
        return newUserWarning