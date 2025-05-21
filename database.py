from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

def get_sao_paulo_time():
    sao_paulo_tz = pytz.timezone("America/Sao_Paulo")
    return datetime.now(sao_paulo_tz)

class Locomotiva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperatura_motor = db.Column(db.Float, nullable=False)
    consumo_combustivel_km = db.Column(db.Float, nullable=False)
    ja_sofreu_manutencao = db.Column(db.String(1), nullable=False)
    pressao_oleo_motor = db.Column(db.Float, nullable=False)
    temperatura_combustivel = db.Column(db.Float, nullable=False)
    temperatura_oleo_refrigeracao = db.Column(db.Float, nullable=False)
    data_criacao = db.Column(db.DateTime, default=get_sao_paulo_time)

    def __repr__(self):
        return f'<Locomotiva {self.id} - Temperatura Motor: {self.temperatura_motor}°C>'
