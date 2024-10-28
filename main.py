from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from fastapi.params import Body 
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):             # the pydantic library is used to import the Basemodel 
    title: str  
    content: str
    published: bool = True
    rating: Optional[int] = None

# request Get method url: "/"

# if the urls have same path then the server only executes the request in order wise


my_posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title": # the array here is converted 
    "favorite foods","content":"I like Pizza","id":2}]                             # to json format and sent to api 

def find_index_post(id):
    for i,p in enumerate(my_posts):   # creates an enumerate object that produces pairs containing an index and the value at that index.
        if p['id'] == id:
            return i
        
# the first code
@app.get("/")                    # the fastapi runs only the first path operation with the given url and then stops
def root():                             # But if the url differs then it only runs the path written 
    return{"message":"welcome to my api!!!"}   # "/" is a path
                                        # @app.get(fastapi instance) is known as the decorator converts a function to fastapi

''' When there is a change in the code we can use the code as uvicorn filename:app --reload 
so that the server automatically reloads the server everytime'''

@app.get("/post")
def get_post():
    return {"data":"This is your posts"}


@app.post("/createposts")
def createpost(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title: {payload['title']},  content: {payload['content']}"}

@app.post("/createpost")
def create_post(payload: dict=Body(...)):
    print(payload)
    return{"new_post":f"title {payload['title']} content: {payload['content']}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)# we showing 201 status in postman when run this path operation                          
def create_posts(post: Post):         
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000) 
    my_posts.append(post_dict)                
    return{"data":post_dict}                
                                         # removing the title or the content in the body of Postman is  
                                         # going to throw a value error because the schema validation should be
                                         # according to the pydantic Basemodel which is defined as the class 'Post'
                                         # in the top

@app.get("/posts")                # REMEMBER BEFORE RUNNING THIS PATH OPERATION WE NEED TO RUN THE ABOVE POST OPERATION
def get_posts():                  # OPERATION IN ORDER FOR SUCCESSFUL APPEND OF TWO DATA  
    return {"data": my_posts}                                         
                                         
'''In the above path operation we are trying to add a id to the body of the post which is present in the postman 
in json raw body using the randrange funciton from random library and then we are appending the post_dict which is
the post present in the postman to my_post present in the top returning the data in postman output as 
return {"data":my_posts} of the get request which shows my_post data in dictionary form 
'''

# title str, content str


'''
@app.get("/posts/{id}")          
def get_post(id):               
    print(id)                    
    return{"post_details":f"Here is the post id {id}"}'''
                            # the id is a path parameter which is used to extract the id we give in the postman
                            # we are using the get request to extract the id we are interested in and the id
                            # is extracted from my_posts which is at the top 
                            # we need to mention the id with url such as http://127.0.0.1:8000/posts/2 .
                            # In url the number 2 is the id and we get the output as 2 in vscode terminal
                            # and return statement in Postman
    
# The above path operation is not the best practice to extract the id. The following path operation is the improved
# version

'''
@app.get("/posts/{id}")        # This Path operation is specificlly used to extract the detail of particular id
def get_post(id: int):         # The int type is used in function to make sure that it is integer and not any 
    post = find_post(id)       # other data type and if it is any other data type, it doesn't throws an error but says the value is invalid
    print(post)                # In this path operation once we write the url with id it shows the complete detail               
    return{"post_details":post} # along with the id in the Postman
# REMEMBER to always convert the id from string type to integer type
'''

'''The path operation order does matter when calling a path operation. Because if two decorators have the same url
then the url in the first path operation is executed and stoping and second path operation isn't executed'''

def find_post(id):            # Here we are trying to compare the id we mention in the url to the IDs in my_post
    for p in my_posts:        # my_posts is a dictionary which is present above 
        if p['id'] == id:     
            return p          


@app.get("/posts/{id}")             # in this code we are throwing a error when an id is not found 
def get_post(id:int,response:Response):
    post = find_post(id)          # finding the id through above find_post function
    if not post:
       # response.status_code = status.HTTP_404_NOT_FOUND        # the 404 http status code is used to for a detail not found
       # return {"message":f"post with id: {id} was not found"}  # returning the message if id is not found
    
       # the above two were slow to execute.here is a one line fast method
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, # import HTTPException library from fastpai from top
                           detail=f"post with id: {id} was not found")
    return{"post":post}


def find_index_post(id):
    for i,p in enumerate(my_posts):   # creates an enumerate object that produces pairs containing an index and the value at that index.
        if p['id'] == id:
            return i

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT) # http is used to show status code as 204 in postman 
def delete_post(id:int):
    # deleting post
    # find the index in the array that has required ID
    # my_post.pop(index)
    index = find_index_post(id)
    
    if index == None:                # if an is not found in the array then to throw http status code as 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # we are using the response code here because to not get 
                                                            # any error when we try to delete a post which is already 
                                                            # deleted and to show empty in the output of postman

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    index = find_index_post(id)
    
    if index == None:                # if an is not found in the array then to throw http status code as 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")    
    
    # If the ID is found
    post_dict = post.dict()   # converting the detail stored in the frontend to regular dictionary
    post_dict['id'] = id      # adding the id to the post_dict
    my_posts[index] = post_dict  # for the post within the index we are replacing with post_dict
    return {"data":post_dict}    