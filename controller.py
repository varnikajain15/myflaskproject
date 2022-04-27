from urllib import response
from boto3 import resource
import config

#AWS CONFIGURATIONS
AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
 
resource = resource(
   'dynamodb',
   aws_access_key_id     = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME
)

#CREATE TABLE

def create_table_books():   
   table = resource.create_table(
       TableName = 'Books', # Name of the table
       KeySchema = [
           {
               'AttributeName': 'id',
               'KeyType'      : 'HASH' #RANGE = sort key, HASH = partition key
           }
       ],
       AttributeDefinitions = [
           {
               'AttributeName': 'id', # Name of the attribute
               'AttributeType': 'N'   # N = Number (B= Binary, S = String)
           }
       ],
       ProvisionedThroughput={
           'ReadCapacityUnits'  : 10,
           'WriteCapacityUnits': 10
       }
   )
   return table

BooksTable = resource.Table('Books')

#CRUD OPERATIONS
#CREATE

def write_to_books(id, title, author):
    response = BooksTable.put_item(
        Item = {
            'id'     : id,
            'title'  : title,
            'author' : author,
            'reviews'  : 0
        }
    )
    return response

#READ


def read_from_books(id):
    response = BooksTable.get_item(
        Key = {
            'id'     : id
        },
        AttributesToGet = [
            'id','title', 'author' # valid types dont throw error, 
        ]                      # Other types should be converted to python type before sending as json response
    )
    return response

""" def read_the_data():
    response = BooksTable.get_item(
        AttributeToGet = [
            'id','title','author'
        ]
    )    
    return response """

#UPDATE    

def update_in_books(id, data:dict):
    response = BooksTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates={
            'title': {
                'Value'  : data['title'],
                'Action' : 'PUT' # # available options = DELETE(delete), PUT(set/update), ADD(increment)
            },
            'author': {
                'Value'  : data['author'],
                'Action' : 'PUT'
            }
        },
        ReturnValues = "UPDATED_NEW"  # returns the new updated values
    )
    return response

#Update ‘reviews’ property for an entry.    

def review_a_books(id):
    response = BooksTable.update_item(
        Key = {
            'id': id
        },
        AttributeUpdates = {
            'reviews': {
                'Value'  : 1,
                'Action' : 'ADD'
            }
        },
        ReturnValues = "UPDATED_NEW"
    )
    response['Attributes']['reviews'] = int(response['Attributes']['reviews'])
    return response

def modify_author_for_books(id, author):
    response = BooksTable.update_item(
        Key = {
            'id': id
        },
        UpdateExpression = 'SET info.author = :author', #set author to new value
        #ConditionExpression = '', # execute until this condition fails # no condition
        ExpressionAttributeValues = { # Value for the variables used in the above expressions
            ':new_author': author
        },
        ReturnValues = "UPDATED_NEW"  #what to return
    )
    return response

#DELETE    

def delete_from_books(id):
    response = BooksTable.delete_item(
        Key = {
            'id': id
        }
    )

    return response

def delete_the_table():
    response = BooksTable.delete()

    return response