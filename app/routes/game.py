

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import secrets
import string
import qrcode
from io import BytesIO
import base64

from app.db.db import get_db
from app.db.models import Game, GameParticipant
from datetime import datetime, timedelta, timezone


router = APIRouter()



class CreateGameRequest(BaseModel):
    host_id: int
    description: str
    location: str
    duration: int
    size: int







def generate_game_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(6))


def create_unique_code(db: Session):
    while True:
        code = generate_game_code()
        existing = db.query(Game).filter(Game.code == code).first()
        if not existing:
            return code


def generate_qr_base64(code: str):
    join_url = f"http://127.0.0.1:8000/api/games/join/{code}"

    qr = qrcode.make(join_url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    return base64.b64encode(buffer.getvalue()).decode()




@router.post("/games")
def create_game(
    data: CreateGameRequest,
    db: Session = Depends(get_db)
):

    
    host_id = data.host_id

    code = create_unique_code(db)
    qr_img = generate_qr_base64(code)
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(minutes=data.duration)

    new_game = Game(
        host_id=data.host_id,
        description=data.description,
        location=data.location,
        start_time=start_time,
        end_time=end_time,
        size=data.size,
        code=code,
        qr_img=qr_img
    )

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return {
        "game_id": new_game.id,
        "join_code": new_game.code,
        "qr_img": f"data:image/png;base64,{new_game.qr_img}"
    }







