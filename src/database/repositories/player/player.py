from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import Player

class PlayerRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, player_id: int) -> Player:
        
        if player_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(Player) \
                .filter(Player.id == player_id) \
                .first()
                
        return result
    
    def create(self, player_data: dict) -> Player:
        
        if player_data is None or len(player_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getById(player_data['id'])
        
        if existing:
            return existing
        
        newPlayer = Player(**player_data)
        self.session.add(newPlayer)
        
        try:
            self.session.commit()
            self.session.refresh(newPlayer)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Player with this ID or unique constraint already exists.")
        
        return newPlayer