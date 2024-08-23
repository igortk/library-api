from typing import Type

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from api.dto.db.models import BookTable, GenreTable, AvailabilityStatusTable
from api.settings import PostgresSettings


class PostgresProvider:
    def __init__(self, pg_settings: PostgresSettings):
        engine = create_engine(url=pg_settings.url)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_all_books(self) -> [BookTable]:
        return self.session.query(BookTable).all()

    def get_book_by_id(self, id: int) -> BookTable | None:
        return self.session.query(BookTable).filter_by(id=id).first()

    def get_genre_by_name(self, genre_name) -> GenreTable | None:
        return self.session.query(GenreTable).filter_by(name=genre_name).first()

    def get_availability_status_by_name(self, status_name) -> AvailabilityStatusTable | None:
        return self.session.query(AvailabilityStatusTable).filter_by(status=status_name).first()

    def delete_book_by_id(self, id: int) -> bool:
        rows_count = self.session.query(BookTable).filter(BookTable.id == id).delete()
        if rows_count == 0:
            return False
        self.session.commit()

        return True

    def add_new(self, value):
        self.session.add(value)
        self.session.commit()
