from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import Report, PredictionReport, Prediction, UserWarning, ProfileMatch, ProfileMatchCalculator
import decimal

class ReportRepository():
    def __init__(self, session: AsyncSession):
        self.session = session

    # Returns a report by ID
    async def getById(self, report_id: int) -> Report:
        
        if report_id is None:
            raise ValueError("Report ID cannot be None")
        
        result = await self.session.query(Report) \
                .filter(Report.id == report_id) \
                .first()
                
        return result

    # Create a new report
    async def create(self, report_data: dict) -> Report:
        
        if report_data is None or len(report_data) == 0:
            raise ValueError("Report data cannot be None or empty")
        
        newReport = Report(**report_data)
        self.session.add(newReport)
        await self.session.commit()
        await self.session.refresh(newReport)
        
        return newReport
    
    # Returns a list of reports that have a prediction with the given identifier and a value greater than or equal to the given value
    async def getReportsByPredictionValue(self, identifier: str, value: decimal.Decimal, limit: int = 10) -> list[Report]:
        
        if identifier is None:
            raise ValueError("Identifier cannot be None")
        
        if value is None:
            raise ValueError("Value cannot be None")
        
        prediction = await self.session.query(Prediction) \
                    .filter(Prediction.identifier == identifier) \
                    .first()
        
        if prediction is None:
            raise ValueError(f"Prediction with identifier {identifier} not found")
        
        result = await self.session.query(Report) \
                .join(PredictionReport, PredictionReport.report_id == Report.id) \
                .join(Prediction, PredictionReport.prediction_id == Prediction.id) \
                .filter(Prediction.identifier == identifier) \
                .filter(PredictionReport.value >= value) \
                .limit(limit) \
                .all()
                
        return result
    
    # Returns a list of reports where the error field is not null
    async def getAllErroredReports(self, limit: int = 10) -> list[Report]:
        result = await self.session.query(Report) \
                .filter(Report.error != None) \
                .limit(limit) \
                .all()
        return result

    # Returns a list of reports that have entries in user_warnings table
    async def getAllWarningedReports(self, limit: int = 10) -> list[Report]:
        result = await self.session.query(Report) \
                .join(UserWarning, UserWarning.report_id == Report.id) \
                .limit(limit) \
                .all()
        return result
    
    # Returns a list of reports that have a profile match with the given calculator ID and a value greater than or equal to the given value
    async def getReportsByProfileMatchCalculatorValue(self, calculator_id: int, value: decimal.Decimal, limit: int = 10) -> list[Report]:
        
        if calculator_id is None:
            raise ValueError("Calculator ID cannot be None")
        
        if value is None:
            raise ValueError("Value cannot be None")
        
        calculator = await self.session.query(ProfileMatchCalculator) \
                    .filter(ProfileMatchCalculator.id == calculator_id) \
                    .first()

        if calculator is None:
            raise ValueError(f"Profile match calculator with ID {calculator_id} not found")
        
        result = await self.session.query(Report) \
                .join(ProfileMatch, ProfileMatch.report_id == Report.id) \
                .filter(ProfileMatch.calculator_id == calculator_id) \
                .filter(Report.profile_match_value > value) \
                .limit(limit) \
                .all()
        return result