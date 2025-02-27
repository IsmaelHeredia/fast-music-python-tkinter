from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DB_NAME = "musictk.db"
DATABASE_URL = f"sqlite:///{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

def migrate():
    from models import PlaylistSong, Song, PlaylistVideo, Video, Stations, PlaylistHistory, Configuration  # 🔥 Importamos modelos aquí para evitar problemas

    Base.metadata.create_all(engine)

    session = get_session()
    
    config = Configuration(songs_directory=None, videos_directory=None,
                           songs_directory_gd=None, songs_directory_downloads=None,
                           videos_directory_downloads=None)
    history = PlaylistHistory(songs_list=None, videos_list=None)

    session.add_all([config, history])
    session.commit()