CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publication_date DATE NOT NULL,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    page_count INT NOT NULL,
    language VARCHAR(50) NOT NULL,
    description TEXT,
    publisher VARCHAR(100) NOT NULL,
    genre_id INT NOT NULL,
    availability_id INT NOT NULL,
    FOREIGN KEY (genre_id) REFERENCES genres(id),
    FOREIGN KEY (availability_id) REFERENCES availability_statuses(id)
);