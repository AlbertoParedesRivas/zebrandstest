# ZeBrands's test

REST API of a products catalog with user adminstrators. The stack i used is Python with Flask and Docker

## Instalation

You need to fill a **.env** file with the corresponding values shown in the **example.env** blueprint. After you've done with the .env file save it in the root directory of the repository.
Next you need to clone this repository and within the directory it creates run:

    docker-compose up

Or if you use docker desktop the next command should also work:

    docker compose up

After the services started you can now start making request.
I exported the postman collections and enviroment i used to test this app, the files are in the **postman-test** directory

## Entities

There are three entities in this app:

### Admins

-   id (uuid)
-   name (string)
-   lastname (string)
-   email (string) _(unique)_
-   password (string)

### Products

-   id (uuid)
-   name (string)
-   price (float)
-   brand (string)
-   stock (integer)
-   sku (string) _(unique)_

### Product_Views

-   id (uuid)
-   date_visited (date)
-   product_id (uuid)

## Endpoints

### Admins related endpoints

#### /login POST:

-   Receives email and password
-   Returns an access_token

#### /admins POST

-   Receives name, lastname, email and password
-   Returns the created admin

#### /admins GET

-   Returns a list of all the administrators

#### /admins/:admin_id GET

-   Returns the admin with id of :admin_id

#### /admins/:admin_id PUT

-   Receives name, lastname, email and password
-   Returns the modified admin with id of :admin_id

#### /admins/:admin_id DELETE

-   Returns a message stating if the administrator with id of :admin_id has been deleted

### Products related endpoints

#### /products/:product_id GET

-   Returns the product with the id of :product_id

#### /products/:product_id DELETE

-   Returns a message stating if the product with id of :product_id has been deleted

#### /products/:product_id PUT

-   Receives name, price, brand, stock and sku
-   Returns the modified product with id of :admin_id

#### /products POST

-   Receives name, price, brand, stock and sku
-   Returns the created product

#### /products GET

-   Returns a list of all the products
