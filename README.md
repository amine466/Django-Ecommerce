# Django E-commerce

A simple and fully functional e-commerce website built with Django. This project demonstrates a basic online store, allowing users to browse products, add them to a shopping cart, and complete orders. The website includes user authentication and a basic admin panel for managing products and orders.

## Features

- **User Authentication**: Allows users to register, log in, and manage their account.
- **Product Catalog**: Display products in a grid with details such as price, description, and image.
- **Shopping Cart**: Add products to the shopping cart, update quantities, and view the cart contents.
- **Order Management**: Customers can place orders, and administrators can manage orders.
- **Admin Dashboard**: Admins can add, edit, and delete products, and manage orders.

## Admin Dashboard

Here’s a screenshot of the admin dashboard where administrators can manage products and orders:

![Admin Dashboard](images/Screenshot%202025-03-22%20161240.png)

## Website Screenshot

Here’s a screenshot of the homepage where users can browse products:

![Website Homepage](images/Screenshot%202025-03-22%20161153.png)

## Installation

To run this project locally, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/amine466/Django-Ecommerce.git
```
### 2. Navigate into the project directory
```bash
Django-Ecommerce
```
### 3. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```
### 4. Install dependencies
```bash
pip install -r requirements.txt
```
### 5. Set up the database
```bash
pip install -r requirements.txt
```
### 6. Run the development server
```bash
python manage.py runserver
```
You can now visit the site at http://127.0.0.1:8000/ in your browser.

## Usage
- Visit the homepage to browse products.

- Sign up or log in to make purchases.

- Use the admin panel (http://127.0.0.1:8000/admin/) to manage products and orders.

## Technologies Used

- Django: Web framework for building the application.

- Python: Programming language.

- SQLite: Database for development (you can switch to another database if desired).

- Bootstrap: Frontend framework for styling.

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.
