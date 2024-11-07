from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from src.config.database import get_session
from src.database.repositories.player import PlayerRepository
from src.database.repositories.aggregator import AggregatorRepository
from src.database.repositories.report import ReportRepository, ReportLinkRepository
from src.database.repositories.prediction import PredictionRepository, PredictionReportRepository
from src.database.repositories.game import GameRepository
from src.database.repositories.user_warning import UserWarningRepository
from src.database.repositories.profile_match import ProfileMatchCalculatorConfigRepository, ProfileMatchCalculatorFunctionRepository, ProfileMatchCalculatorRepository, ProfileMatchRepository
from src.config.enums.user_warning_enums import LevelEnum, CategoryEnum
from src.config.enums.report_link_enums import TypeEnum
import json
import decimal
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter()

@router.post('/import')
async def import_report(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    try:
        content = await file.read()
        data = json.loads(content)
        
        player = None
        aggregator = None
        userWarnings = []
        predictions = []
        profileMatches = []
        reportLinks = []
        
        if "player" not in data:
            raise HTTPException(
                status_code=404,
                detail="Player not found"
            ) 
        
        player = data.get("player")

        if "aggregator" not in data:
            raise HTTPException(
                status_code=404,
                detail="Aggregator not found"
            ) 
        
        aggregator = data.get("aggregator")
        
        if "user_warnings" not in data:
            userWarnings = []
        else:
            userWarnings = data.get("user_warnings")  
        
        if "predictions" not in data:
            predictions = []
        else:
            predictions = data.get("predictions")   
        
        if "profile_matches" not in data:
            profileMatches = []
        else:
            profileMatches = data.get("profile_matches")
        
        if "report_links" not in data:
            reportLinks = []
        else:
            reportLinks = data.get("report_links")  
        
        
        # Create player
        playerData = {
            "id": int(player.get("id")),
            "uuid": player.get("uuid"),
            "name": player.get("name"),
            "email": player.get("email")
        }
            
        playerRepo = PlayerRepository(session)
        createdPlayer = playerRepo.create(playerData)
        
        # Create aggregator
        aggregatorData = {
            "id": int(aggregator.get("id")),
            "name": aggregator.get("name")
        }
            
        aggregatorRepo = AggregatorRepository(session)
        createdAggregator = aggregatorRepo.create(aggregatorData)
        
        # Create report
        reportData = {
            "id": int(data.get("id")),
            "player_id": createdPlayer.id,
            "aggregator_id": createdAggregator.id,
            "valid": bool(data.get("valid")),
            "error": data.get("error"),
            "state": data.get("state"),
            "raw_report_url": data.get("raw_report_url"),
            "raw_json": data,
            "created_at": data.get("created_at"),
        }
        
        reportRepo = ReportRepository(session)
        createdReport = reportRepo.create(reportData)
        
        # Create prediction(s)
        for prediction in predictions:
            
            kpi = prediction.get("kpi")
            
            # Create Prediction
            predictionData = {
                "identifier": kpi.get("identifier"),
                "name": kpi.get("name"),
                "description": kpi.get("description")
            }
            
            predictionRepo = PredictionRepository(session)
            createdPrediction = predictionRepo.create(predictionData)
            
            # Create PredictionReport                
            predictionReportData = {
                "prediction_id": createdPrediction.id,
                "report_id": createdReport.id,
                "order": None,
                "excluded": bool(kpi.get("excluded")),
                "obsolate": bool(kpi.get("obsolate")),
                "value": None
            }
            
            if kpi.get("order") is not None:
                predictionReportData["order"] = int(kpi.get("order"))
            
            if prediction.get("value") is not None: 
                predictionReportData["value"] = decimal.Decimal(prediction.get("value"))
            
            predictionReportRepo = PredictionReportRepository(session)
            predictionReportRepo.create(predictionReportData)
            
        # Create UserWarning
        for userWarning in userWarnings:
                    
            # Create Game
            gameData = {
                "identifier": userWarning.get("game"),
                "name": userWarning.get("game_name")
            }
                    
            gameRepo = GameRepository(session)
            createdGame = gameRepo.create(gameData)
            
            # Create UserWarning
            userWarningData = {
                "game_id": createdGame.id,
                "report_id": createdReport.id,
                "level": None,
                "category": None,
                "message": userWarning.get("message"),
            }
                
            try:
                userWarningData["level"] = LevelEnum(userWarning.get("level")).value
                userWarningData["category"] = CategoryEnum(userWarning.get("category")).value
            except ValueError as e:
                raise HTTPException(
                    status_code=500,
                    detail="Invalid value for level or category"
                ) 
                
            userWarningRepo = UserWarningRepository(session)
            userWarningRepo.create(userWarningData)
            
            
        # Create ReportLink(s)
        for reportLink in reportLinks:
            
            print(reportLink)
            
            reportLinkData = {
                "report_id": createdReport.id,
                "type": None,
                "url": reportLink[1],
            }
            
            if reportLink[0] is not None:
            
                try:
                    reportLinkData["type"] = TypeEnum(reportLink[0])
                except ValueError as e:
                    raise HTTPException(
                        status_code=500,
                        detail="Invalid value for type"
                    ) 
            
                reportLinkRepo = ReportLinkRepository(session)
                reportLinkRepo.create(reportLinkData)
            
        # Create ProfileMatch(es)
        for profileMatch in profileMatches:
            calculator = profileMatch.get("calculator")
            jsonData = profileMatch.get("json_data")
            jsonDataCalculator = jsonData.get('calculator')
            
            # Create ProfileMatchCalculatorConfig
            
            profileMatchCalculatorConfigData = {
                "identifier": jsonDataCalculator.get("config"),
                "name": calculator.get("config_name")
            }
            
            profileMatchCalculatorConfigsRepo = ProfileMatchCalculatorConfigRepository(session)
            createdProfileMatchCalculatorConfigs = profileMatchCalculatorConfigsRepo.create(profileMatchCalculatorConfigData)
            
            # Create ProfileMatchCalculatorFunction
            profileMatchCalculatorFunctionData = {
                "identifier": jsonDataCalculator.get("calc_func"),
            }
            
            profileMatchCalculatorFunctionRepo = ProfileMatchCalculatorFunctionRepository(session)
            createdProfileMatchCalculatorFunction = profileMatchCalculatorFunctionRepo.create(profileMatchCalculatorFunctionData)
                
            # Create ProfileMatchCalculator
            profileMatchCalculatorData = {
                "id": int(calculator.get("id")),
                "display_name": calculator.get("display_name"),
                "function_id": createdProfileMatchCalculatorFunction.id,
                "config_id": createdProfileMatchCalculatorConfigs.id,
            }
            
            profileMatchCalculatorRepo = ProfileMatchCalculatorRepository(session)
            createdProfileMatchCalculator = profileMatchCalculatorRepo.create(profileMatchCalculatorData)
                
            # Create ProfileMatch
            profileMatchData = {
                "report_id": createdReport.id,
                "calculator_id": createdProfileMatchCalculator.id,
                "error": profileMatch.get("error"),
                "manual": bool(profileMatch.get("manual")),
                "value": decimal.Decimal(profileMatch.get("value")),
                "model1_score": decimal.Decimal(jsonData.get("model1_score")),
                "model1_score_perc": decimal.Decimal(jsonData.get("model1_score_perc")),
                "warnings": jsonData.get("warnings"),
                "gps_list": jsonData.get("gps_list"),
                "created_at": profileMatch.get("created_at"),
            }
            
            profileMatchRepo = ProfileMatchRepository(session)
            profileMatchRepo.create(profileMatchData)
            
        return {"success": "Report imported successfully"}
        
    except Exception as e:
        
        error_message = str(e)
        stack_trace = traceback.format_exc()
        logger.error(f"Error occurred: {error_message}\n{stack_trace}")
        
        raise HTTPException(
            status_code=500,
            detail="Something went wrong"
        )