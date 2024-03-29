# Confectionery shop application

This is a simple application that demonstrates an E-commerce website using the Django stack. The application loads products from SQLite database and displays them. Users can select to display products in a single category. Users can click on any product to get more information including pricing, calories and description. Users can select items and add them or delete them from their shopping cart. PayPal paying is included.

The application was also written using HTML, CSS and Javascript.

## Prerequisites

You must have the following installed:
- Python 3
- Django

## Running in development

### Database

It is possible to run the app with no database content, but there will be no products to show.

To populate database, type commands below.

### Running the application
Prepare the app:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Start the server:

```bash
python manage.py runserver
```

Screenshots:
![Alt text](https://github.com/conradylx/ProjectWebsite/blob/master/Screenshots/cartpage.png?raw=true "Optional Title")
![Alt text](https://github.com/conradylx/ProjectWebsite/blob/master/Screenshots/homepage.png?raw=true "Optional Title")
![Alt text](https://github.com/conradylx/ProjectWebsite/blob/master/Screenshots/shoppage.png?raw=true "Optional Title")
![Alt text](https://github.com/conradylx/ProjectWebsite/blob/master/Screenshots/sumamrypage.png?raw=true "Optional Title")
