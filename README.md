# API_PO
A vendor purchase management REST api developed with Django and Django REST . 
Teck Stack :- Django , Django REST , Docker , Docker compose , PostGres
## Start up the application 
Make sure docker and docker compose is installed locally . 
Clone this repository .

    git clone https://github.com/chahatsagarmain/api_po.git

Move to the clone directory .

    cd api_po
Build the docker compose file .

    docker compose up -d --build 

## Accessing the API endpoints 
All the endpoints are protected with Token based authentication . A valid token can be acquired by logging or registering as a user . The token should then be passed with Authorization request header with value Token <token_value>
### Login 
-   **URL:** `localhost:8000/api/login`
-   **Method:** `POST`
-   **Description:** Endpoint for user login.
-   **Permissions:** AllowAny
- `{  "username":  "Username",  "password":  "Password"  }`
- ### Register
-   **URL:** `localhost:8000/api/register`
-   **Method:** `POST`
-   **Description:** Endpoint for user register.
-   **Permissions:** AllowAny
- `{  "username":  "Username",  "password":  "Password" , "email" : "email"} 
The method will return a token which have to be used with all subsequent requests.

### Authentication

All endpoints require token-based authentication. Include the authentication token in the request headers.

### Purchase Orders

#### List All Purchase Orders

-   **URL:** `localhost:8000/api/purchase_orders/`
-   **Method:** `GET`
-   **Description:** Retrieve a list of all purchase orders.
-   **Permissions:** Requires authentication.
-   **Response:** Returns a list of all purchase orders.

#### Create a Purchase Order

-   **URL:** `localhost:8000/api/purchase_orders/`
-   **Method:** `POST`
-   **Description:** Create a new purchase order.
-   **Permissions:** Requires authentication.
-   **Request Body:** Create a order with minimal details  , other data like vendor or rating is updated using put method . 
    
    `{
      "items": "Items Details",
      "quantity": "Total Quantity",
      "status": "PO Status"
    }` 
    
-   **Response:** Returns the created purchase order.

#### Retrieve Purchase Order Details

-   **URL:** `localhost:8000/api/purchase_orders/{po_id}/`
-   **Method:** `GET`
-   **Description:** Retrieve details of a specific purchase order.
-   **Permissions:** Requires authentication.
-   **Response:** Returns the purchase order with the specified ID.

#### Update Purchase Order Details

-   **URL:** `localhost:8000/api/purchase_orders/{po_id}/`
-   **Method:** `PUT`
-   **Description:** Update details of a specific purchase order. vendor assignment , quality rating , fullfillment rate updation
-   **Permissions:** Requires authentication.
-   **Request Body:** JSON or form data like .

    {	"vendor"  :  2, "status"  :  "pending", "quality_rating"  :  4 , "issue" : null}

-   **Response:** Returns the updated purchase order.

#### Delete a Purchase Order

-   **URL:** `localhost:8000/api/purchase_orders/{po_id}/`
-   **Method:** `DELETE`
-   **Description:** Delete a specific purchase order.
-   **Permissions:** Requires authentication.
-   **Response:** Returns success message upon deletion.

  
Sure, I'll provide the documentation for these vendor-related API endpoints, including the base URL and authentication requirements:

----------

## Vendor Management API Documentation

### Base URL

bash

Copy code

`http://localhost:8000/api/` 

### Authentication

All endpoints require token-based authentication. Include the authentication token in the request headers.

### Vendor Management

#### List All Vendors

-   **URL:** `http://localhost:8000/api/vendors/`
-   **Method:** `GET`
-   **Description:** Retrieve a list of all vendors.
-   **Permissions:** Requires authentication.
-   **Response:** Returns a list of all vendors.

#### Create a Vendor

-   **URL:** `http://localhost:8000/api/vendors/`
-   **Method:** `POST`
-   **Description:** Create a new vendor.
-   **Permissions:** Requires authentication.
-   **Request Body:** `{	"name"  :  "vendor5" , "contact_details"  :  "details_5" , "address"  :  "address_5" , "vendor_code"  :  "code5"}`
-   **Response:** Returns the created vendor.

#### Retrieve Vendor Details

-   **URL:** `http://localhost:8000/api/vendors/{vendor_id}/`
-   **Method:** `GET`
-   **Description:** Retrieve details of a specific vendor.
-   **Permissions:** Requires authentication.
-   **Response:** Returns the vendor with the specified ID.

#### Update Vendor Details

-   **URL:** `http://localhost:8000/api/vendors/{vendor_id}/`
-   **Method:** `PUT`
-   **Description:** Update details of a specific vendor.
-   **Permissions:** Requires authentication.
-   **Request Body:** 	
    {	"name"  :  "vendor3" , "contact_details"  :  "details_2" , "address"  :  "address_1" , "vendor_code"  :  "code_3"	}

-   **Response:** Returns a success message upon updating the vendor.

#### Delete a Vendor

-   **URL:** `http://localhost:8000/api/vendors/{vendor_id}/`
-   **Method:** `DELETE`
-   **Description:** Delete a specific vendor.
-   **Permissions:** Requires authentication.
-   **Response:** Returns a success message upon deletion of the vendor.
   
