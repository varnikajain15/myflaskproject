from flask import Flask, request, render_template, url_for, redirect
import controller as dynamodb

app = Flask(__name__)


@app.route('/test')
def test():
    print("TEST SUCCESS")
    return 'TEST SUCCESS'
    

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create')
def root_route():
    dynamodb.create_table_books()
    #return 'Table created'
    return render_template('create.html')

@app.route('/createentry')
def add_entry():
    #dynamodb.create_table_books()
    #return 'Table created'
    return render_template('createentry.html')     


@app.route('/books', methods=['POST','GET'])
def add_books():
    if request.method== 'POST':
        data = request.form
        #return request.form['id']
        
        response = dynamodb.write_to_books(int(data['id']), data['title'], data['author']) 
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return render_template('table.html')
        return {  
            'msg': 'Some error occcured',
            'response': response
         }



"""     data = request.get_json()
    #response = dynamodb.write_to_books(id, title, author)
    response = dynamodb.write_to_books(data['id'], data['title'], data['author']) 
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
        }
    return {  
        'msg': 'Some error occcured',
        'response': response
    }   """  
  
"""   id = request.form.get['id']
    title = request.form.get['title']
    author = request.form.get['author']  """
    
    #
    #  
    
    #   
    




""" @app.route('/books/', methods=['GET'])
def get_data():
    response = dynamodb.read_the_data()
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if ('Item' in response):
            return { 'Item': response['Item'] }
        return { 'msg' : 'Item not found!' }
    return {
        'msg': 'Some error occured',
        'response': response
    } """

@app.route('/read',methods = ['POST', 'GET'])
def read():
   if request.method == 'POST':
      user = request.form
      return redirect(url_for('get_books',id = int(user['id'])))
   else:
      user = request.args.get('id')
      return render_template('table.html')   

@app.route('/books/<int:id>', methods=['GET'])
def get_books(id):
    response = dynamodb.read_from_books(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        if ('Item' in response):
            return { 'Item': response['Item'] }
        return { 'msg' : 'Item not found!' }
    return {
        'msg': 'Some error occured',
        'response': response
    }

@app.route('/delete',methods = ['POST', 'GET','DELETE'])
def delete():
   if request.method == 'POST':
      user = request.form
      return redirect(url_for('delete_books',id = int(user['id'])))
   else:
      user = request.args.get('id')
      return render_template('table.html')      

@app.route('/delete/<int:id>')
def delete_books(id):
    response = dynamodb.delete_from_books(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return render_template('delete.html')  
        """ return {
            'msg': 'Deleted successfully',
        } """
    return {  
        'msg': 'Some error occcured',
        'response': response
    } 
@app.route('/update',methods = ['POST', 'GET','PUT'])
def update():
   if request.method == 'POST':
      user = request.form
      return render_template('update.html')
      #return redirect(url_for('update_books',id = int(user['id'])))
   else:
      user = request.args.get('id')
      return render_template('table.html')     

@app.route('/updatedata',methods = ['POST', 'GET','PUT'])
def updatedata():
   if request.method == 'POST':
      user = request.form
      response = dynamodb.update_in_books(int(user['id']),user) 
      if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }
      return {  
            'msg': 'Some error occcured',
            'response': response
         }  
      #return redirect(url_for('update_books',id = int(user['id'])))
   else:
      user = request.args.get('id')
      return render_template('table.html')     

@app.route('/update/<int:id>')
def update_books(id,data):
    if request.method== 'POST':
        #data = request.form
        #return request.form['id']
        
        response = dynamodb.update_in_books(int(data['id']), data) 
        if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }
        return {  
            'msg': 'Some error occcured',
            'response': response
         }
    else:
        return{
            'msg' : 'sorry'
        }     

    """ data = request.get_json()
    response = dynamodb.update_in_books(id, data)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'                : 'Updated successfully',
            'ModifiedAttributes' : response['Attributes'],
            'response'           : response['ResponseMetadata']
        }
    return {
        'msg'      : 'Some error occured',
        'response' : response
    }   """ 


    


@app.route('/review/books/<int:id>', methods=['POST'])
def review_books(id):
    response = dynamodb.review_a_books(id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg'      : 'Review the books successfully',
            'Reviews'    : response['Attributes']['reviews'],
            'response' : response['ResponseMetadata']
        }
    return {
        'msg'      : 'Some error occured',
        'response' : response
    }

@app.route('/books/delete')   
def delete_table():
    response = dynamodb.delete_the_table()
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return render_template('delete.html') 
        """ return {
            'msg': 'Deleted table successfully',
        } """
    return {  
        'msg': 'Some error occcured',
        'response': response
    } 



if __name__ == '__main__':
    app.run(port=5000,debug=True)
    #app.run(host='127.0.0.1', port=5000, debug=True) #running on port 5000