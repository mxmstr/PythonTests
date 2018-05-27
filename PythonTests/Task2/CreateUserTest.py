# Eric Lynch https://github.com/mxmstr

# CreateUserTest
"""Test adding user data"""

import os, requests
from io import StringIO

ADD_USER_URL = 'https://api.intercom.io/users'
DELETE_USER_URL = 'https://api.intercom.io/user_delete_requests'


def Usage(script_name):
    
    print( 'Usage: python3 ' + script_name + ' <Your access token>' )


def AddUser(request_name, access_token):

    payload = open(request_name)
    headers = {
        'Authorization' : 'Bearer ' + access_token, 
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
        }
    
    return requests.post(ADD_USER_URL, data=payload, headers=headers)


def DeleteUser(internal_id, access_token):
    
    payload = open(StringIO.StringIO('{intercom_user_id": "' + internal_id + '"}'))
    headers = {
        'Authorization' : 'Bearer ' + access_token, 
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
        }
    
    return requests.post(DELETE_USER_URL, data=payload, headers=headers)

    
if __name__ == "__main__":
    
    import sys
    
    # Get access token argument
    if len(sys.argv) != 2:
        Usage(os.path.basename(sys.argv[0]))
        sys.exit()
        
    access_token = sys.argv[1]
    
    
    # Test several user create requests, rollback upon success
    for request in ['request1.json', 'request2.json', 'request3.json']:
        
        add_response = AddUser(request, access_token)
        
        if add_response.status_code == 200:
            
            print('User created.')
            
            internal_id = add_response.json['id']
            user_id = add_response.json['user_id']
            delete_response = DeleteUser(internal_id, access_token)
            
            if delete_response.status_code == 200:
                
                print('User deleted.')
                
                deleted_user_id = delete_response.json['id']
                if user_id != deleted_user_id:
                    print('Wrong user deleted!')
                
            else:
                print('Failed to delete user.')
            
        else:
            print('Failed to add user.')
    
    