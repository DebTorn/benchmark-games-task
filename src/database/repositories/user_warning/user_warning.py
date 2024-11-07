from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import UserWarning

class UserWarningRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, user_warning_id: int) -> UserWarning:
        
        if user_warning_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(UserWarning) \
                .filter(UserWarning.id == user_warning_id) \
                .first()
                
        return result
    
    def getByReportAndGameIdWithLevelAndCategory(self, report_id: int, game_id: int, level: int, category: str) -> UserWarning:
        
        if report_id is None:
            raise ValueError("Report ID cannot be None")
        
        if game_id is None:
            raise ValueError("Game ID cannot be None")
        
        if level is None:
            raise ValueError("Level cannot be None")
        
        if category is None:
            raise ValueError("Category cannot be None")
        
        result = self.session.query(UserWarning) \
                .filter(UserWarning.report_id == report_id) \
                .filter(UserWarning.game_id == game_id) \
                .filter(UserWarning.level == level) \
                .filter(UserWarning.category == category) \
                .first()
                
        return result
    
    def create(self, user_warning_data: dict) -> UserWarning:
    
        if user_warning_data is None or len(user_warning_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByReportAndGameIdWithLevelAndCategory(user_warning_data['report_id'], user_warning_data['game_id'], user_warning_data['level'], user_warning_data['category'])
        
        if existing:
            return existing
        
        newUserWarning = UserWarning(**user_warning_data)
        self.session.add(newUserWarning)
        
        try:
            self.session.commit()
            self.session.refresh(newUserWarning)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("User Warning with this ID or unique constraint already exists.")
        
        return newUserWarning