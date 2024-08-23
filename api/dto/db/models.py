from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class GenreTable(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    books = relationship("BookTable", back_populates="genre")


class AvailabilityStatusTable(Base):
    __tablename__ = 'availability_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), unique=True, nullable=False)

    books = relationship("BookTable", back_populates="availability")


class BookTable(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    publication_date = Column(Date, nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    page_count = Column(Integer, nullable=False)
    language = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    publisher = Column(String(100), nullable=False)

    availability_id = Column(Integer, ForeignKey('availability_statuses.id'), nullable=False)

    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)

    availability = relationship("AvailabilityStatusTable", back_populates="books")
    genre = relationship("GenreTable", back_populates="books")

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'publication_date': self.publication_date.isoformat(),
            'isbn': self.isbn,
            'page_count': self.page_count,
            'language': self.language,
            'description': self.description,
            'publisher': self.publisher,
            'genre': self.genre.name,
            'availability': self.availability.status
        }
