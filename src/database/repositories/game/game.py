from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import Game

class GameRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, game_id: int) -> Game:
        
        if game_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(Game) \
                .filter(Game.id == game_id) \
                .first()
                
        return result
    
    def getByIdentifier(self, identifier: str) -> Game:
            if identifier is None:
                raise ValueError("Identifier cannot be None")
            
            result = self.session.query(Game) \
                    .filter(Game.identifier == identifier) \
                    .first()
                    
            return result
    
    def create(self, game_data: dict) -> Game:
        
        if game_data is None or len(game_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByIdentifier(game_data['identifier'])
        
        if existing:
            return existing
        
        newGame = Game(**game_data)
        self.session.add(newGame)
        
        try:
            self.session.commit()
            self.session.refresh(newGame)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Game with this ID or unique constraint already exists.")
        
        return newGame