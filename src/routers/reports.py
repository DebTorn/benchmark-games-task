from fastapi import APIRouter

router = APIRouter()

@router.post('/import')
def import_report():
    return {'message': 'Report imported successfully'}

