from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.database.models import ProfileMatch, ProfileMatchCalculator, ProfileMatchCalculatorConfigs, ProfileMatchCalculatorFunction

class ProfileMatchRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, prof_match_id: int) -> ProfileMatch:
        
        if prof_match_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(ProfileMatch) \
                .filter(ProfileMatch.id == prof_match_id) \
                .first()
                
        return result
    
    def getReportAndCalculatorId(self, report_id: int, calculator_id: int) -> ProfileMatch:
            if report_id is None or calculator_id is None:
                raise ValueError("Report ID and Calculator ID cannot be None")
            
            result = self.session.query(ProfileMatch) \
                    .filter(ProfileMatch.report_id == report_id) \
                    .filter(ProfileMatch.calculator_id == calculator_id) \
                    .first()
                    
            return result
    
    def create(self, prof_match_data: dict) -> ProfileMatch:
        
        if prof_match_data is None or len(prof_match_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getReportAndCalculatorId(prof_match_data['report_id'], prof_match_data['calculator_id'])
        
        if existing:
            return existing
        
        newProfileMatch = ProfileMatch(**prof_match_data)
        self.session.add(newProfileMatch)
        
        try:
            self.session.commit()
            self.session.refresh(newProfileMatch)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("ProfileMatch with this ID or unique constraint already exists.")
        
        return newProfileMatch
    
class ProfileMatchCalculatorRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, profile_match_calculator_id: int) -> ProfileMatchCalculator:
        
        if profile_match_calculator_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(ProfileMatchCalculator) \
                .filter(ProfileMatchCalculator.id == profile_match_calculator_id) \
                .first()
                
        return result
    
    def getByFunctionAndConfigId(self, function_id: int, config_id: int) -> ProfileMatchCalculator:
            if function_id is None or config_id is None:
                raise ValueError("Function ID and Config ID cannot be None")
            
            result = self.session.query(ProfileMatchCalculator) \
                    .filter(ProfileMatchCalculator.function_id == function_id) \
                    .filter(ProfileMatchCalculator.config_id == config_id) \
                    .first()
                    
            return result
    
    def create(self, profile_matcch_calculator_data: dict) -> ProfileMatchCalculator:
        
        if profile_matcch_calculator_data is None or len(profile_matcch_calculator_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByFunctionAndConfigId(profile_matcch_calculator_data['function_id'], profile_matcch_calculator_data['config_id'])
        
        if existing:
            return existing
        
        newProfileMatchCalc = ProfileMatchCalculator(**profile_matcch_calculator_data)
        self.session.add(newProfileMatchCalc)
        
        try:
            self.session.commit()
            self.session.refresh(newProfileMatchCalc)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("ProfileMatchCalculator with this ID or unique constraint already exists.")
        
        return newProfileMatchCalc
    
class ProfileMatchCalculatorConfigRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, profile_match_calculator_config_id: int) -> ProfileMatchCalculatorConfigs:
        
        if profile_match_calculator_config_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(ProfileMatchCalculatorConfigs) \
                .filter(ProfileMatchCalculatorConfigs.id == profile_match_calculator_config_id) \
                .first()
                
        return result
    
    def getByIdentifier(self, identifier: str) -> ProfileMatchCalculatorConfigs:
            
            if identifier is None:
                raise ValueError("Identifier cannot be None")
            
            result = self.session.query(ProfileMatchCalculatorConfigs) \
                    .filter(ProfileMatchCalculatorConfigs.identifier == identifier) \
                    .first()
                    
            return result
    
    def create(self, profile_match_calculator_config_data: dict) -> ProfileMatchCalculatorConfigs:
        
        if profile_match_calculator_config_data is None or len(profile_match_calculator_config_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByIdentifier(profile_match_calculator_config_data['identifier'])
        
        if existing:
            return existing
        
        newProfileMatchCalcConf = ProfileMatchCalculatorConfigs(**profile_match_calculator_config_data)
        self.session.add(newProfileMatchCalcConf)
        
        try:
            self.session.commit()
            self.session.refresh(newProfileMatchCalcConf)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("ProfileMatchCalculatorConfigs with this ID or unique constraint already exists.")
        
        return newProfileMatchCalcConf
    
class ProfileMatchCalculatorFunctionRepository():
    def __init__(self, session: Session):
        self.session = session
    
    def getById(self, prof_match_calc_func_id: int) -> ProfileMatchCalculatorFunction:
        
        if prof_match_calc_func_id is None:
            raise ValueError("ID cannot be None")
        
        result = self.session.query(ProfileMatchCalculatorFunction) \
                .filter(ProfileMatchCalculatorFunction.id == prof_match_calc_func_id) \
                .first()
                
        return result
    
    def getByIdentifier(self, identifier: str) -> ProfileMatchCalculatorFunction:
                
                if identifier is None:
                    raise ValueError("Identifier cannot be None")
                
                result = self.session.query(ProfileMatchCalculatorFunction) \
                        .filter(ProfileMatchCalculatorFunction.identifier == identifier) \
                        .first()
                        
                return result
    
    def create(self, prof_match_calc_func_data: dict) -> ProfileMatchCalculatorFunction:
        
        if prof_match_calc_func_data is None or len(prof_match_calc_func_data) == 0:
            raise ValueError("The data cannot be None or empty")
        
        existing = self.getByIdentifier(prof_match_calc_func_data['identifier'])
        
        if existing:
            return existing
        
        newProfMatchCalcFunc = ProfileMatchCalculatorFunction(**prof_match_calc_func_data)
        self.session.add(newProfMatchCalcFunc)
        
        try:
            self.session.commit()
            self.session.refresh(newProfMatchCalcFunc)
        except IntegrityError:
            self.session.rollback()
            raise ValueError("ProfileMatchCalculatorFunction with this ID or unique constraint already exists.")
        
        return newProfMatchCalcFunc