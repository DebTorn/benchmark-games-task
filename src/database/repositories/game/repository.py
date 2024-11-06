from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Game

class GameRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def getById(self, game_id: int) -> Game:
        result = await self.session.query(Game) \
                .filter(Game.id == game_id) \
                .first()
                
        return result
    
    async def create(self, game_data: dict) -> Game:
        newGame = Game(**game_data)
        
        self.session.add(newGame)
        await self.session.commit()
        await self.session.refresh(newGame)
        
        return newGame