from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import Prediction, PredictionReport

class PredictionRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, prediction_id: int) -> Prediction:
        
        if prediction_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(Prediction) \
                .filter(Prediction.id == prediction_id) \
                .first()
                
        return result
    
    def getByIdentifier(self, identifier: int) -> Prediction:
        
        if identifier is None:
            raise ValueError("Identifier cannot be None")
        
        result = self.session.query(Prediction) \
                .filter(Prediction.identifier == identifier) \
                .first()
                
        return result
    
    def create(self, predicition_data: dict) -> Prediction:
        
        if predicition_data is None or len(predicition_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByIdentifier(predicition_data['identifier'])
        
        if existing:
            return existing
        
        newPrediction = Prediction(**predicition_data)
        self.session.add(newPrediction)
        
        try:
            self.session.commit()
            self.session.refresh(newPrediction)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Prediction with this ID or unique constraint already exists.")

        return newPrediction

class PredictionReportRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, prediction_report_id: int) -> PredictionReport:
        
        if prediction_report_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(PredictionReport) \
                .filter(PredictionReport.id == prediction_report_id) \
                .first()
                
        return result
    
    def getByPredictionAndReportId(self, prediction_id: int, report_id: int) -> PredictionReport:
            if prediction_id is None or report_id is None:
                raise ValueError("Prediction ID cannot be None")
            
            result = self.session.query(PredictionReport) \
                    .filter(PredictionReport.prediction_id == prediction_id) \
                    .filter(PredictionReport.report_id == report_id) \
                    .first()
                    
            return result
    
    def create(self, prediction_report_data: dict) -> PredictionReport:
        
        if prediction_report_data is None or len(prediction_report_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByPredictionAndReportId(prediction_report_data['prediction_id'], prediction_report_data['report_id'])
        
        if existing:
            return existing
        
        newPredictionReport = PredictionReport(**prediction_report_data)
        self.session.add(newPredictionReport)
        
        try:
            self.session.commit()
            self.session.refresh(newPredictionReport)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Prediction report with this ID or unique constraint already exists.")
        
        
        return newPredictionReport