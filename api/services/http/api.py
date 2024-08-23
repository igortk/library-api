import http

from flask import Flask, request, jsonify

from api.constants.messages import SUCCESSFUL_BOOK_CREATE, ERROR_AVAILABILITY_STATUS_NOT_FOUNT, ERROR_GENRE_NOT_FOUND, \
    ERROR_BOOK_NOT_FOUND, SUCCESSFUL_BOOK_DELETE, ERROR_SOMETHING_WRONG
from api.dto.api.requests import *
from api.dto.api.responses import ApiResponse
from api.dto.db.models import *
from api.services.postgres.provider import PostgresProvider
import json


class BookRoutes:
    def __init__(self, app: Flask, pg_provider: PostgresProvider):
        self.app = app
        self.register_routes()
        self.pg_provider = pg_provider

    def register_routes(self):
        @self.app.get("/books")
        def get_all_books():
            books = self.pg_provider.get_all_books()
            return jsonify([book.to_json() for book in books]), 200

        @self.app.post("/books")
        def add_book():
            response = ApiResponse(id=0, message=SUCCESSFUL_BOOK_CREATE)
            status_code = http.HTTPStatus.CREATED

            try:
                book_data = AddBook(**request.get_json())
                response.id = book_data.id

                genre = self.pg_provider.get_genre_by_name(book_data.genre)

                if not genre:
                    status_code = http.HTTPStatus.NOT_FOUND
                    response.message = ERROR_GENRE_NOT_FOUND

                availability_status = self.pg_provider.get_availability_status_by_name(book_data.availability)
                if not availability_status:
                    status_code = http.HTTPStatus.NOT_FOUND
                    response.message = ERROR_AVAILABILITY_STATUS_NOT_FOUNT

                book = BookTable(
                    title=book_data.title,
                    author=book_data.author,
                    publication_date=book_data.publication_date,
                    isbn=book_data.isbn,
                    page_count=book_data.page_count,
                    language=book_data.language,
                    description=book_data.description,
                    publisher=book_data.publisher,
                    genre_id=genre.id,
                    availability_id=availability_status.id
                )

                self.pg_provider.add_new(book)
            except Exception as e:
                print(e)
            finally:
                return jsonify(json.loads(json.dumps(response.__dict__))), status_code

        @self.app.get("/books/<id>")
        def get_book_by_id(id):
            error_response = ApiResponse(id=id, message=ERROR_BOOK_NOT_FOUND)
            book_data = self.pg_provider.get_book_by_id(id)

            if not book_data:
                return jsonify(json.loads(json.dumps(error_response.__dict__))), http.HTTPStatus.NOT_FOUND

            book_response = Book(
                title=book_data.title,
                author=book_data.author,
                publication_date=book_data.publication_date.isoformat(),
                isbn=book_data.isbn,
                page_count=book_data.page_count,
                language=book_data.language,
                description=book_data.description,
                publisher=book_data.publisher,
                genre=book_data.genre.name,
                availability=book_data.availability.status,
                id=book_data.id
            )

            return jsonify(json.loads(json.dumps(book_response.__dict__))), http.HTTPStatus.OK

        @self.app.put("/books/<id>")
        def update_book_info(id):
            return "update successful"

        @self.app.delete("/books/<id>")
        def delete_book(id):
            response = ApiResponse(id=id, message=SUCCESSFUL_BOOK_DELETE)
            status_code = http.HTTPStatus.OK

            try:
                is_deleted = self.pg_provider.delete_book_by_id(id)
                if is_deleted:
                    response.message = ERROR_BOOK_NOT_FOUND
                    status_code = http.HTTPStatus.NOT_FOUND
            except Exception as ex:
                response.message = ERROR_SOMETHING_WRONG
                status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR
                print(ex)  # TODO add/change to logger
            finally:
                return jsonify(json.loads(json.dumps(response.__dict__))), status_code
