import requests


def load_to_db():
    book_data = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit').json()
    for book in book_data['items']:
        print(book['id'])
        print(book['volumeInfo']['title'])
        print(book['volumeInfo']['publishedDate'])
        if book['volumeInfo'].keys == 'averageRating':
            print(book['volumeInfo']['averageRating'])

        if book['volumeInfo'].keys == 'ratingsCount':
            print(book['volumeInfo']['ratingsCount'])
        print(book['volumeInfo']['imageLinks']['thumbnail'])
        for author in book['volumeInfo']['authors']:
            print(author)
        if book['volumeInfo'].keys == 'categories':
            for category in book['volumeInfo']['categories']:
                print(category)


if __name__ == '__main__':
    load_to_db()
