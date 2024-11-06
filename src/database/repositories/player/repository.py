from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Player

class PlayerRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, player_id: int) -> Player:
        result = await self.session.query(Player) \
                .filter(Player.id == player_id) \
                .first()
                
        return result
    
    async def create(self, player_data: dict) -> Player:
        newPlayer = Player(**player_data)
        
        self.session.add(newPlayer)
        await self.session.commit()
        await self.session.refresh(newPlayer)
        
        return newPlayer