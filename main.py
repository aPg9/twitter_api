# Python
from http.client import HTTPException
import json
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

#Pydantic
from pydantic import BaseModel 
from pydantic import EmailStr
from pydantic import Field

# Fastapi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Form, Path

app = FastAPI()


# Models

class UserBase(BaseModel):
    user_id: UUID = Field (...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field (
        ...,
        min_length= 8,
        max_length= 64 
    )  

class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length= 20,
    )
    message: str = Field(
        default= "Login Successfully!!"
    )

class User(UserBase):    
    first_name: str = Field(
        ...,
        min_length= 1,
        max_length= 50,
    )
    last_name: str = Field(
        ...,
        min_length= 1,
        max_length= 50,
    )
    birth_date: Optional[date] = Field(default=None)

class UserResgister(User):
    password: str = Field (
        ...,
        min_length= 8,
        max_length= 64 
    )  

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length= 1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Auxiliar functions

def read_data(file):
    with open(f"{file}.json", "r+", encoding="utf-8") as f:
        return json.loads(f.read())

def overwrite_data(file, result_list):
    with open(f"{file}.json", "w", encoding="utf-8") as f:
        f.seek(0)
        f.write(json.dumps(result_list))

def show_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This {info} doesn't exist!"
        )

def delete_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            results.remove(data)
            overwrite_data(file, results)
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This {info} doesn't exist!"
        )


#-----> Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
def signup(user: UserResgister = Body(...)):     
    """
    Signup

    This path operation register a user in the app

    Parameters:
        -Request body parameter
            - **user: UserRegister**

    Returns a json with basic user information:
        - **user_id: UUID**
        - **email: Emailstr**
        - **first_name: str**
        - **last_name: str**        
        - **birth_date: date**
    """
    results = read_data("users")
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    results.append(user_dict)
    overwrite_data("users", results)
    

### Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"]
)
def login(
    username: str = Form(...),
    password: str = Form(...)
    ):
    """
    Login

    This path operation login a user in the app.

    Parameters:
    - Request body parameter:
        - **username: str** --> Return a model with username.
        - **password: str** --> Do not return person's password.
    
    Sing up a user of the app.

    """    
    return LoginOut(username=username)

### Show all users 
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    """
    This path operation shows all users in the app

    Parameters:
        -

    Retunrs a json list with all users in the app, with the following keys:
        - **user_id: UUID**
        - **email: Emailstr**
        - **first_name: str**
        - **last_name: str**        
        - **birth_date: date**
        """  
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())                             #-----> Cargamos todo el contenido del archivo en la variable results
        return results


### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Show a user",
    tags=["Users"]
)
def show_a_user(user_id: str = Path(
    ...,
    title="User's ID",
    description="Enter User's ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa2")):
    """
    This path operation shows a user in the app

    Parameters:
        -

    Retunrs a json list with a user that has been registered in the app, following the next keys:
        - **tweet_id: UUID**
        - **content: str** 
        - **created_at: datetime** 
        - **updated_at: Optional[datetime]** 
        - **by: User** 
    """
    return show_data("users", user_id, "user")  


### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_a_user(user_id: str = Path(
    ...,
    title="User ID",
    description="Enter a User ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa2")
    ):
    """
    This path operation updates a tweet in the app

    Parameters:
        -

    Retunrs a json list with a tweet in the app, with the following keys:
        - **tweet_id: UUID**
        - **content: str** 
        - **created_at: datetime** 
        - **updated_at: Optional[datetime]** 
        - **by: User** 
    """   
    return delete_data("users", user_id,"user")
    

### Update a user
@app.put(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_a_user(user_id: str = Path(
    ...,
    title="User ID",
    description="Enter a User ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa2"),
    user: UserResgister = Body(...)
    ):
    """
    This path operation updates a tweet in the app

    Parameters:
        -

    Retunrs a json list with a tweet in the app, with the following keys:
        - **tweet_id: UUID**
        - **content: str** 
        - **created_at: datetime** 
        - **updated_at: Optional[datetime]** 
        - **by: User** 
    """   
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
      
    results = read_data("users")
    for user in results:
        if user["user_id"] == user_id:
            results[results.index(user)] = user_dict           
            overwrite_data("users", results) 
            return user    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!") 


##-----> Tweets
### Show all tweets

@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
    )
def home():
    """
    This path operation shows all tweets in the app

    Parameters:
        -

    Retunrs a json list with all tweets in the app, with the following keys:
        - **tweet_id: UUID**
        - **content: str** 
        - **created_at: datetime** 
        - **updated_at: Optional[datetime]** 
        - **by: User** 
    """  

    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())                           
        return results
   

### Post a tweet

@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):     #-----> Le pedimos al usuario que nos envie un request body con un json que tenga un tweet
    """
    Post a tweet

    This path operation post a tweet in the app

    Parameters:
        - Parameters
            - tweet : Tweet

    Returns a json with basic tweet information:
        - **tweet_id: UUID**
        - **content: str** 
        - **created_at: datetime** 
        - **updated_at: Optional[datetime]** 
        - **by: User** 
    """
    with open ("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())                                
        tweet_dict = tweet.dict()                                       
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str (tweet_dict["by"]["birth_date"])        
        results.append(tweet_dict)
        f.seek(0)                                                      
        f.write(json.dumps(results))                                  
        return tweet
  

### Show a tweet

@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(tweet_id: str = Path(
    ...,
    title="Tweet ID",
    description="Enter a Tweet ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa2")
    ):
    """
    This path operation shows a tweet in the app

    Parameters:
        -

    Retunrs a json list with a tweet in the app, with the following keys:
        - **tweet_id: UUID**
        - **content: str** 
        - **created_at: datetime** 
        - **updated_at: Optional[datetime]** 
        - **by: User** 
    """
    return show_data("tweets", tweet_id, "tweet")
    
    
### Delete a tweet

@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Deletes a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(tweet_id: str = Path(
    ...,
    title="Delete Tweet",
    description="Deletes a tweet",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa2")
    ):
    """
    Delete a Tweet

    This path operation delete a tweet from the app

    Parameters:
        - tweet_id: UUID

    Deletes a tweet from database.
        
    """
    delete_data("tweets", tweet_id, "tweet")


# Update a tweet    

@app.post(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Updates a tweet",
    tags=["Tweets"]
)

def update_a_tweet(tweet_id: str = Path(
    ...,
    title="Tweet ID",
    description="Enter a Tweet ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa2"),
    content: str = Form(
        ..., 
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet")
    ):
    """
    This path operation updates a tweet in the app

    Parameters:
        -

    Retunrs a json list with a tweet in the app, with the following keys:
        - **tweet_id: UUID**
        - **content: str** 
        - **created_at: datetime** 
        - **updated_at: Optional[datetime]** 
        - **by: User** 
    """   
    tweet_id = str(tweet_id)
    results = read_data("tweets")  

    for tweet in results:
        if tweet["tweet_id"] == tweet_id:
            tweet["tweet_id"] = str(tweet["tweet_id"])
            tweet["content"] = content
            tweet["updated_at"] = str(datetime.now())
            print(tweet)
            overwrite_data("tweets", results) 
            return tweet    
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This tweet doesn't exist!") 
