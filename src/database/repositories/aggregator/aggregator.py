from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import Aggregator

class AggregatorRepository():
    def __init__(self, session: Session):
        self.session = session  
    
    def getById(self, aggregator_id: int) -> Aggregator:
        
        if aggregator_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(Aggregator) \
                .filter(Aggregator.id == aggregator_id) \
                .first()
                
        return result
    
    def create(self, aggregator_data: dict) -> Aggregator:
        
        if aggregator_data is None or len(aggregator_data) == 0:
            raise ValueError("Report data cannot be None or empty")
        
        existing = self.getById(aggregator_data['id'])
        
        if existing:
            return existing
        
        newAggregator = Aggregator(**aggregator_data)
        self.session.add(newAggregator)
        
        try:
            self.session.commit()
            self.session.refresh(newAggregator)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Aggregator with this ID or unique constraint already exists.")
        
        
        return newAggregator