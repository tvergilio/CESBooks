# CES Bookstore
CES Bookstore is a web application to manage book sales, written in Python using the Flask framework. 
It is intended for internal use at Centre of English Studies, Leeds.

## Features
1. Login - secure password verified login.
2. Current Stock - displays all books currently in stock.
3. Sell - sells a book to a student.
4. Swap - exchanges a used book for a new title.
5. Buy - buys a used book from a student.
6. History - lists the transactions that have been made
7. Add Stock - adds new stock to the database, new titles or more copies of an existing book.
8. Register - allows new users to register for access.

## Integrations
1. The application integrates with a MySQL relational database.
2. The connection string is set in the application.py file.
3. Scripts to create the database schema can be found in the migrations folder.

## Future Development
1. The application will be integrated with a barcode scanner for ease of entering accurate ISBNs.

## Hosting
A live version of the application can be found
[here](http://redyelruc.pythonanywhere.com/login).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
Copyright (c) 2020 Aidan Curley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.