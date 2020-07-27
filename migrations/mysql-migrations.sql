USE finance;
# ----
# -- Drop table for users
# ----
DROP TABLE IF EXISTS users;

# ----
# -- Table structure for users
# ----
CREATE TABLE users
(
    id       INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
    username TEXT                               NOT NULL,
    hash     TEXT                               NOT NULL
);

# ----
# -- Data dump for users, a total of 2 rows
# ----
INSERT INTO users (username, hash)
VALUES ("Aidan", "pbkdf2:sha256:150000$ts8TeHZ0$c0e79f0fa4a812fc081f7a0a9c5c88b7e9099d6d3b069be237321e9460f7c649");
INSERT INTO users (username, hash)
VALUES ("Rob", "pbkdf2:sha256:150000$VSoXKJv9$a34e5c53fbdbe525b21c3a85e1bdd48c488b2afbb9feda27634df780eb6d1cb6");
# ----
# -- Drop table for books
# ----
DROP TABLE IF EXISTS books;

# ----
# -- Table structure for books
# ----
CREATE TABLE books
(
    isbn       varchar(13) NOT NULL,
    title      varchar(100),
    level      varchar(25),
    edition    smallint,
    stock_new  integer,
    stock_used integer,
    price_new  real,
    price_used real
);

# ----
# -- Data dump for books, a total of 5 rows
# ----
INSERT INTO books (isbn, title, level, edition, stock_new, stock_used, price_new, price_used)
VALUES ("9780194713535", "New Headway", "C1", "3", "12", "4", "30.0", "15.0");
INSERT INTO books (isbn, title, level, edition, stock_new, stock_used, price_new, price_used)
VALUES ("9780194771818", "New Headway", "B2", "3", "1", "2", "30.0", "15.0");
INSERT INTO books (isbn, title, level, edition, stock_new, stock_used, price_new, price_used)
VALUES ("9781447936879", "Cutting Edge", "B1", "3", "11", "3", "32.0", "15.0");
INSERT INTO books (isbn, title, level, edition, stock_new, stock_used, price_new, price_used)
VALUES ("9783125404243", "Empower", "B1", "1", "10", "9", "32.0", "15.0");
INSERT INTO books (isbn, title, level, edition, stock_new, stock_used, price_new, price_used)
VALUES ("9781447936909", "Cutting Edge", "A2-B1", "3", "5", "3", "32.0", "15.0");

# ----
# -- Drop table for transactions
# ----
DROP TABLE IF EXISTS transactions;

# ----
# -- Table structure for transactions
# ----
CREATE TABLE transactions
(
    transaction_type text NOT NULL,
    user_id          integer,
    book_id          text,
    price            real,
    student          text,
    date             date DEFAULT (CURRENT_DATE)
);

# ----
# -- Data dump for transactions, a total of 15 rows
# ----
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SELL", "2", "9780194713535", "30.0", "Frank", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SELL", "2", "9781447936879", "32.0", "Mohammed R.", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SWAP IN", "2", "9780194713535", "0.0", "Hye Jung", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SWAP OUT", "2", "9781447936879", "0.0", "Hye Jung", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SWAP IN", "2", "9780194713535", "0.0", "Franco Pardini", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SWAP OUT", "2", "9781447936879", "0.0", "Franco Pardini", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("BUY", "2", "9780194713535", "-10.0", "Mary", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SELL", "2", "9781447936879", "15.0", "Thalita", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SELL", "2", "9780194713535", "15.0", "Malachy", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SELL", "2", "9781447936909", "15.0", "Rampage", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("BUY", "2", "9780194713535", "-10.0", "Frank", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SWAP IN", "2", "9781447936879", "0.0", "Walter W.", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SWAP OUT", "2", "9780194713535", "0.0", "Walter W.", "2020-07-26");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SELL", "2", "9781447936909", "15.0", "Mario Yamasaki", "2020-07-27");
INSERT INTO transactions (transaction_type, user_id, book_id, price, student, date)
VALUES ("SELL", "2", "9783125404243", "15.0", "Herb Dean", "2020-07-27");

# ----
# -- structure for index username on table users
# ----
ALTER TABLE users
    ADD UNIQUE (username(20));
COMMIT;

# ----
# -- make isbn primary key
# ----
ALTER TABLE books
ADD PRIMARY KEY(isbn);
COMMIT;