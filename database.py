from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class HighScore(Base):
    __tablename__ = 'high_scores'
    id = Column(Integer, primary_key=True)
    player_name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

def init_db():
    engine = create_engine('sqlite:///high_scores.db')
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    return sessionmaker(bind=engine)()

engine = init_db()

def save_score(player_name, score):
    session = get_session(engine)
    high_score = HighScore(player_name=player_name, score=score)
    session.add(high_score)
    session.commit()

def get_scores():
    session = get_session(engine)
    scores = session.query(HighScore).order_by(HighScore.score.desc()).limit(10).all()
    return {score.player_name: score.score for score in scores}
