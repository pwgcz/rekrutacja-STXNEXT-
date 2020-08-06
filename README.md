**Library**
---
  _Created API base on data from  Google API available at given URL: https://www.googleapis.com/books/v1/volumes?q=Hobbit. API create instance of books to corresponding parameter (in given example parameters is Hobbit). API provide sorting by published_date and many authors, also sort by published date. Initial database contain books with parameters 'Hobbit'._
* **URL**

  * _/db_
  * _/books_
  * _/books/<book_id>_

* **Method:**
  
  * _/db_  `POST` - download data from google API and save to database
  * _/books_ `GET` - list of all books
  * _/books/<book_id>_ `GET` - book of given id (book id match id from google API)
  
*  **URL Params**
     
   _URL params are provided for `/books` endpoint_

    * **all params are optional:**<br />
      * author=[string] - provide filtering over authors, can pass many params with author and response list witch all matching authors<br />
      * published_date=[string] - provide filtering over published date<br />
      * sort=[published_date] - sort all list of book in descending or ascending order<br />
    
   
   
* **Data Params**

  _Method Post for for endpoint /db require Data Param_
    * **Example of param body data:**  <br />
    `{ 'q' : 'war' }`
  

* **Success Response:**
  
  _Response for endpoint: books/YyXoAAAACAAJ_

  * **Code:** 200 <br />
    **Content:** `{
    "title": "Hobbit czyli Tam i z powrotem",
    "authors": ["J. R. R. Tolkien"],
    "published_date": "2004",
    "categories": [
        "Baggins, Bilbo (Fictitious character)"
      ],
    "average_rating": 5,
    "ratings_count": 2,
    "thumbnail": "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
}`
 
* **Notes:**

    * _Code contains unit tests_
    * _Link URL for working App:_
    * _Create superuser in Django Admin to illustrate data saved in database, example:_
    ![Screenshot from 2020-08-06 18-10-26](https://user-images.githubusercontent.com/62465226/89555322-30525580-d810-11ea-9d43-4f4f742ba5a3.png)
    * _Login  to admin site and go to /api endpoint to illustrate available endpoint and format of data, example:_
    ![Screenshot from 2020-08-06 17-23-33](https://user-images.githubusercontent.com/62465226/89555082-ec5f5080-d80f-11ea-9aaa-9b16da4474e7.png)

    
   