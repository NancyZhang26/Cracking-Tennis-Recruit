from typing import Optional
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.connection import get_conn
from backend.models import Player

    # player_name: str
    # gender: str | None
    # player_id: int
    # singles_utr: Decimal | None
    # doubles_utr: Decimal | None 
    # location: str | None
def insert_player(player: Player) -> None:
    sql = """
        INSERT INTO players (player_name, gender, player_id, singles_utr, doubles_utr, location, school_id)
        values(%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (player_id) DO UPDATE SET
            player_name = EXCLUDED.player_name,
            gender = EXCLUDED.gender, 
            player_id = EXCLUDED.player_id, 
            singles_utr = EXCLUDED.singles_utr, 
            doubles_utr = EXCLUDED.doubles_utr, 
            location = EXCLUDED.location, 
            school_id = EXCLUDED.school_id;
    """ 
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, 
                (player["player_name"],
                 player["gender"], 
                 player["player_id"],
                 player["singles_utr"], 
                 player["doubles_utr"], 
                 player["location"],
                 player["school_id"]
            ))

player: Player = {
    "player_name": "nance Z!",
    "gender": "f",
    "location": "Shanghai, China",
    "player_id": 1234,
    "singles_utr": 7,
    "doubles_utr": 9,
    "school_id": 1534
}

insert_player(player=player)

def delete_player(player_id: int) -> None:
    sql = """
        DELETE FROM players 
        WHERE player_id = %s 
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (player_id,)) # Second param needs to be a list of items, need the comma too to show it is a tuple

delete_player(1234)