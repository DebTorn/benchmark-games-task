from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import Report, PredictionReport, Prediction, UserWarning, ProfileMatch, ProfileMatchCalculator, ReportLink
import decimal

class ReportRepository():
    def __init__(self, session: Session):
        self.session = session

    # Returns a report by ID
    def getById(self, report_id: int) -> Report:
        
        if report_id is None:
            raise ValueError("Report ID cannot be None")
        
        result = self.session.query(Report) \
                .filter(Report.id == report_id) \
                .first()
                
        return result

    # Create a new report
    def create(self, report_data: dict) -> Report:
        
        if report_data is None or len(report_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getById(report_data['id'])
        
        if existing:
            return existing
        
        newReport = Report(**report_data)
        self.session.add(newReport)
        
        try:
            self.session.commit()
            self.session.refresh(newReport)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("Report with this ID or unique constraint already exists.")
        
        return newReport
    
    # Returns a list of reports that have a prediction with the given identifier and a value greater than or equal to the given value
    def getReportsByPredictionValue(self, identifier: str, value: decimal.Decimal, limit: int = 10) -> list[Report]:
        
        if identifier is None:
            raise ValueError("Identifier cannot be None")
        
        if value is None:
            raise ValueError("Value cannot be None")
        
        prediction = self.session.query(Prediction) \
                    .filter(Prediction.identifier == identifier) \
                    .first()
        
        if prediction is None:
            raise ValueError(f"Prediction with identifier {identifier} not found")
        
        result = self.session.query(Report) \
                .join(PredictionReport, PredictionReport.report_id == Report.id) \
                .join(Prediction, PredictionReport.prediction_id == Prediction.id) \
                .filter(Prediction.identifier == identifier) \
                .filter(PredictionReport.value >= value) \
                .limit(limit) \
                .all()
                
        return result
    
    # Returns a list of reports where the error field is not null
    def getAllErroredReports(self, limit: int = 10) -> list[Report]:
        result = self.session.query(Report) \
                .filter(Report.error != None) \
                .limit(limit) \
                .all()
        return result

    # Returns a list of reports that have entries in user_warnings table
    def getAllWarningedReports(self, limit: int = 10) -> list[Report]:
        result = self.session.query(Report) \
                .join(UserWarning, UserWarning.report_id == Report.id) \
                .limit(limit) \
                .all()
        return result
    
    # Returns a list of reports that have a profile match with the given calculator ID and a value greater than or equal to the given value
    def getReportsByProfileMatchCalculatorValue(self, calculator_id: int, value: decimal.Decimal, limit: int = 10) -> list[Report]:
        
        if calculator_id is None:
            raise ValueError("Calculator ID cannot be None")
        
        if value is None:
            raise ValueError("Value cannot be None")
        
        calculator = self.session.query(ProfileMatchCalculator) \
                    .filter(ProfileMatchCalculator.id == calculator_id) \
                    .first()

        if calculator is None:
            raise ValueError(f"Profile match calculator with ID {calculator_id} not found")
        
        result = self.session.query(Report) \
                .join(ProfileMatch, ProfileMatch.report_id == Report.id) \
                .filter(ProfileMatch.calculator_id == calculator_id) \
                .filter((ProfileMatch.value * decimal.Decimal(100)) > value) \
                .limit(limit) \
                .all()
        return result

class ReportLinkRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, report_link_id: int) -> ReportLink:
        
        if report_link_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(ReportLink) \
                .filter(ReportLink.id == report_link_id) \
                .first()
                
        return result
    
    def getByReportIdAndType(self, report_id: int, type: str) -> ReportLink:
            
            if report_id is None or type is None:
                raise ValueError("Report ID and link type cannot be None")
            
            result = self.session.query(ReportLink) \
                    .filter(ReportLink.report_id == report_id) \
                    .filter(ReportLink.type == type) \
                    .first()
                    
            return result
    
    def create(self, report_link_data: dict) -> ReportLink:
        
        if report_link_data is None or len(report_link_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByReportIdAndType(report_link_data['report_id'], report_link_data['type'])
        
        if existing:
            return existing
        
        newReportLink = ReportLink(**report_link_data)
        self.session.add(newReportLink)
        
        try:
            self.session.commit()
            self.session.refresh(newReportLink)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("ReportLink with this ID or unique constraint already exists.")
        
        return newReportLink