# Inventory
The application provides API to create/update/delete Item and its Variants within application.
It also allows users to register users, login them and keeps tracks of any user action performed to Create/Update/Delete Item and its Variants.

## Usage


## Prerequisite

Please install python version 3.7.0.

In order to install all dependencies executes below:

```
 pip install -r requirements.txt 

```

## Starting the application

Open `app/config.py` and update `postgres_local_base` variable with db string.

To setup DB tables executes below:
```
python3 migrate.py db init
python3 migrate.py db migrate
python3 migrate.py db upgrade
```

In order to run the application execute below.
```
python3 run.py
```

Application will be running on `http://localhost:5000/`

## API Documentation
API provides list of operation application can perform.

## Users

### User Registration
Send a `POST` request to `v1/auth/register` endpoint with the payload in
`Json`

An example would be
```
{
  "email": "example@gmail.com",
  "password": "123456"
}
```
Expected response:
```
{
    "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDkzMDI4NDcsImlhdCI6MTU0OTIxNjQyNywic3ViIjozfQ.f-rCyN7c_oTfl15og-Sto0E4PMRq4ADT-UCcjdk-cGI",
    "message": "Successfully registered",
    "status": "success"
}
```
### User Login
The user is able to login by send sending a `POST` request to
`v1/auth/login` with the json payload below.
```
{
  "email": "example@gmail.com",
  "password": "123456"
}
```
Expected response:
```
{
    "auth_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDkzMDI5OTksImlhdCI6MTU0OTIxNjU3OSwic3ViIjozfQ.e2Bn0y2HcugSUIpSlPnCm9gBdJtFLbc-DTJIGccoIm4",
    "message": "Successfully logged In",
    "status": "success"
}
```
### User Logout
The api also enables a user to logout. The `auth/logout` endpoint
provides this functionality.
The `POST` request to the endpoint must have an `Authorization`
header containing the auth token, otherwise the user wont be logged out.

Example of the Authorization header
```
Authorization Bearer <token>
```

If the operation is successful, the response below will be returned.
```
{
    "message": "Successfully logged out",
    "status": "success"
}
```
If the token has expired this will be returned.

```
{
    "message": "Signature expired, Please sign in again",
    "status": "failed"
}
```

For an invalid token
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}

```

Without an Authorization header
```
{
    "message": "Provide an authorization header",
    "status": "failed"
}
```

## Item
The user can create item, update item, delete item from application

### Create Item
Below is an example to create Item by sending `POST` request to `v1/item/`.

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
```
Request payload:

**name** is a required attribute. 


```
{
	"name" : "Casual_Shirt_Denim",
	"brand" : "Denim",
	"category" : "Casual Shirt",
	"productCode" : "CS_D_09036"
}
```

Expected Response:

```
{
    "brand": "Denim",
    "category": "Casual Shirt",
    "id": 7,
    "name": "Casual_Shirt_Denim",
    "productCode": "CS_D_09036",
    "status": "success"
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```

### Update item
Update an existing item by sending `PUT` request to `v1/item/`

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
```
Request payload:
```
{
	"name" : "Casual_Shirt_Denim_01",
	"brand" : "Denim",
	"category" : "Casual Shirt",
	"productCode" : "CS_D_03409"
}
```
Expected Response
```
{
    "brand": "Denim",
    "category": "Casual Shirt",
    "id": 9,
    "name": "Casual_Shirt_Denim_01",
    "productCode": "CS_D_03409",
    "status": "success"
}
```
In case item name is not present in database
```
{
    "message": "item resource cannot be found",
    "status": "failed"
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```
### Get Item list
Below is the example to get list of items by sending `GET` request to `v1/item/`.

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
```
Expected Response:
```
{
    "count": 6,
    "items": [
        {
            "brand": "Roadster",
            "category": "Jeans",
            "id": 2,
            "name": "Roadster_jeans5",
            "productCode": "J_R_01243"
        },
        {
            "brand": "Peter England",
            "category": "Shirt",
            "id": 3,
            "name": "PE_Shirt1",
            "productCode": "S_PE_02347"
        },
        {
            "brand": "Peter England",
            "category": "Casual Shirt",
            "id": 4,
            "name": "PE_Casual_Shirt2",
            "productCode": "S_PE_03248"
        },
        {
            "brand": "Jokey",
            "category": "Boxer",
            "id": 5,
            "name": "Jokey_Boxer1",
            "productCode": "B_J_05971"
        }
    ],
    "next": "http://localhost:5000/v1/item/?page=2",
    "previous": null,
    "status": "success"
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```

### Delete Item
Below is example to delete item by sending `DELETE` request to `v1/item/`

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
```
Payload
```
{
	"name" : "Roadster_jeans5"
}
```
Expected response
```
{
    "message": "Successfully deleted the item Roadster_jeans5",
    "status": "success"
}
```
If unknown item name is sent in payload then following response is returned
```
{
    "message": "item resource cannot be found",
    "status": "failed"
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```

## Variants
You can also add, update, delete variants.

### Create Variant
Below is an example create variant by sending `POST` request to `v1/variant/`

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
```
Request payload:
```
{
	"name" : "Peter_England_Shirt_L",
	"item_id" : 3,
	"sellingPrice" : 1600,
	"costPrice" : 1300,
	"quantity" : 10
}
```
Expected response:
```
{
    "costPrice": "1300",
    "id": 5,
    "item_id": 3,
    "name": "Peter_England_Shirt_L",
    "quantity": 10,
    "sellingPrice": "1600",
    "status": "success"
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```
### Update Variant
Update a variant by sending `PUT` request to `v1/variant/`

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
``` 
Payload
```
{
	"name" : "Peter_England_Shirt_L",
	"item_id" : 3,
	"sellingPrice" : 2000,
	"costPrice" : 1500,
	"quantity" : 5
}
```
Expected Response
```
{
    "costPrice": "1500",
    "id": 5,
    "item_id": 3,
    "name": "Peter_England_Shirt_L",
    "quantity": 5,
    "sellingPrice": "2000",
    "status": "success"
}
```
In case variant is not found in database
```
{
    "message": "variant resource cannot be found",
    "status": "failed"
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```
### Get Variant List
Below is an example get variant by sending `GET` request to `v1/variant/`

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
```
Expected Response
```
{
    "count": 5,
    "next": "http://localhost:5000/v1/variant/?page=2",
    "previous": null,
    "status": "success",
    "variants": [
        {
            "costPrice": "1200",
            "id": 1,
            "item_id": 2,
            "name": "jeans5_blue",
            "quantity": 7,
            "sellingPrice": "1400"
        },
        {
            "costPrice": "1300",
            "id": 2,
            "item_id": 3,
            "name": "Peter_England_Shirt",
            "quantity": 10,
            "sellingPrice": "1600"
        },
        {
            "costPrice": "600",
            "id": 3,
            "item_id": 5,
            "name": "Jockey_boer",
            "quantity": 8,
            "sellingPrice": "800"
        },
        {
            "costPrice": "600",
            "id": 4,
            "item_id": 5,
            "name": "Jockey_boxer_L",
            "quantity": 8,
            "sellingPrice": "800"
        }
    ]
}
```
In case you want to fetch variant of specific item, send `GET` to `v1/variant/?item_id=<item_id>`

Expected response
```
{
    "count": 2,
    "next": null,
    "previous": null,
    "status": "success",
    "variants": [
        {
            "costPrice": "600",
            "id": 3,
            "item_id": 5,
            "name": "Jockey_boer",
            "quantity": 8,
            "sellingPrice": "800"
        },
        {
            "costPrice": "600",
            "id": 4,
            "item_id": 5,
            "name": "Jockey_boxer_L",
            "quantity": 8,
            "sellingPrice": "800"
        }
    ]
}
```
In case you want to fetch variant of specific item, send `GET` to `v1/variant/?name=<variant_name>`

Expected response
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "status": "success",
    "variants": [
        {
            "costPrice": "1200",
            "id": 1,
            "item_id": 2,
            "name": "jeans5_blue",
            "quantity": 7,
            "sellingPrice": "1400"
        }
    ]
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```
### Delete Variant
Delete a variant by sending `DELETE` request to `/v1/variant/`

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
``` 
Payload
```
{
	"name" : "Peter_England_Shirt_L"
}
```
Expected Response
```
{
    "message": "Successfully deleted the variant Peter_England_Shirt_L",
    "status": "success"
}
```
If auth token is missing then following response is returned:
```
{
    "message": "Token is missing",
    "status": "failed"
}
```
If auth token is invalid then follwing response is returned
```
{
    "message": "Invalid token. Please sign in again",
    "status": "failed"
}
```

## User Action

### Get list of user action
Retrieve list of user action by sending `GET` request to `v1/useraction/`

An auth token must be attached in the Authorization
header. 
```
Content-Type : application/json
Authorization : Bearer <auth-token>
``` 
Expected response

```
{
    "count": 18,
    "next": "http://localhost:5000/v1/useraction/?page=2",
    "previous": null,
    "status": "success",
    "variants": [
        {
            "action": "CREATED",
            "id": 1,
            "item_name": "Roadster_jeans5",
            "timestamp": "Sun, 03 Feb 2019 13:55:34 GMT",
            "username": "example@gmail.com",
            "variant_name": null
        },
        {
            "action": "UPDATED",
            "id": 2,
            "item_name": "Roadster_jeans5",
            "timestamp": "Sun, 03 Feb 2019 13:56:09 GMT",
            "username": "example@gmail.com",
            "variant_name": null
        },
        {
            "action": "DELETED",
            "id": 3,
            "item_name": "Roadster_jeans5",
            "timestamp": "Sun, 03 Feb 2019 13:56:32 GMT",
            "username": "example@gmail.com",
            "variant_name": null
        },
        {
            "action": "CREATED",
            "id": 4,
            "item_name": "Roadster_jeans5",
            "timestamp": "Sun, 03 Feb 2019 13:57:29 GMT",
            "username": "example@gmail.com",
            "variant_name": null
        }
    ]
}
```

Get useraction for specific user by sending `GET` request to `v1/useraction/?user_name=<user_email>`
example: `v1/useraction/?user_name=example1@gmail.com`

Expected Response:
```
{
    "count": 5,
    "next": "http://localhost:5000/v1/useraction/?page=2",
    "previous": null,
    "status": "success",
    "variants": [
        {
            "action": "CREATED",
            "id": 9,
            "item_name": "Jokey_Boxer1",
            "timestamp": "Sun, 03 Feb 2019 15:21:10 GMT",
            "username": "example1@gmail.com",
            "variant_name": null
        },
        {
            "action": "CREATED",
            "id": 11,
            "item_name": "Polo_Tshirt",
            "timestamp": "Sun, 03 Feb 2019 15:39:10 GMT",
            "username": "example1@gmail.com",
            "variant_name": null
        },
        {
            "action": "CREATED",
            "id": 12,
            "item_name": "Casual_Shirt_Denim",
            "timestamp": "Sun, 03 Feb 2019 18:07:17 GMT",
            "username": "example1@gmail.com",
            "variant_name": null
        },
        {
            "action": "CREATED",
            "id": 17,
            "item_name": "Casual_Shirt_Denim_01",
            "timestamp": "Sun, 03 Feb 2019 18:50:39 GMT",
            "username": "example1@gmail.com",
            "variant_name": null
        }
    ]
}
```