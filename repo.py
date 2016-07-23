#!/usr/bin/env python3
import urllib.request
import getpass
import json
    

def login (api_url, username, password):
    '''This function logs into the ArchivesSpace REST API returning an acccess token'''
    data = urllib.parse.urlencode({'password': password})
    data = data.encode('utf-8')
    req = urllib.request.Request(
        url = api_url+'/users/'+username+'/login', 
        data = data)
    response = urllib.request.urlopen(req)
    status = response.getcode()
    if status != 200:
        # No session token
        print('ERROR: login failed', response.read().decode('utf-8'))
        return ''
    result = json.JSONDecoder().decode(response.read().decode('utf-8'))
    # Session holds the value we want for auth_token
    return result['session']

def create_repo(api_url, auth_token, name, repo_code, org_code = '', image_url = '', url = ''):
    '''This function sends a create request to the ArchivesSpace REST API'''
    data = json.JSONEncoder().encode({
                    'jsonmodel_type': 'repository',
                    'name': name,
                    'repo_code': repo_code,
                    'org_code': org_code,
                    'image_url': image_url,
                    'url': url
                }).encode('utf-8')
    req = urllib.request.Request(
            url = api_url+'/repositories', 
            data = None, 
            headers = {'X-ArchivesSpace-Session': auth_token})
    response = urllib.request.urlopen(req, data)
    status = response.getcode()
    if status != 200:
        print('WARNING http statuc code', status)
    return json.JSONDecoder().decode(response.read().decode('utf-8'))

def list_repos(api_url, auth_token):
    '''List all the repositories, return the listing object'''
    req = urllib.request.Request(
        url = api_url+'/repositories',
        data = None,
        headers = {'X-ArchivesSpace-Session': auth_token})
    response = urllib.request.urlopen(req)
    status = response.getcode()
    if status != 200:
        print('WARNING http statuc code', status)
    return json.JSONDecoder().decode(response.read().decode('utf-8'))

def list_repo(api_url, auth_token, repo_id):
    '''List all the repositories, return the listing object'''
    req = urllib.request.Request(
        url = api_url+'/repositories/'+str(repo_id),
        data = None,
        headers = {'X-ArchivesSpace-Session': auth_token})
    response =  urllib.request.urlopen(req)
    status = response.getcode()
    if status != 200:
        print('WARNING http statuc code', status)
    return json.JSONDecoder().decode(response.read().decode('utf-8'))

def update_repo(api_url, auth_token, repo_id, repo):
    '''This function sends a updates a repository via ArchivesSpace REST API'''
    data = json.JSONEncoder().encode(repo).encode('utf-8')
    req = urllib.request.Request(
        url = api_url+'/repositories/'+repo_id,
        data = None,
        headers = {'X-ArchivesSpace-Session': auth_token})
    response = urllib.request.urlopen(req, data)
    status = response.getcode()
    if status != 200:
        print('WARNING http statuc code', status)
    return json.JSONDecoder().decode(response.read().decode('utf-8'))

def delete_repo(api_url, auth_token, repo_id):
    '''Delete a repository via ArchivesSpace REST API, returns status code 200 on success'''
    req = urllib.request.Request(
        url = api_url+'/repositories/'+str(repo_id),
        data = None,
        headers = {'X-ArchivesSpace-Session': auth_token},
        method = 'DELETE')
    response = urllib.request.urlopen(req)
    status = response.getcode()
    if status != 200:
        print('WARNING http statuc code', status)
    return json.JSONDecoder().decode(response.read().decode('utf-8'))


if __name__ == '__main__':
    # Test login
    print("Testing login()")
    api_url = input('ArchivesSpace API URL: ')
    username = input('ArchivesSpace username: ')
    password = getpass.getpass('ArchivesSpacew password: ')
    print('Logging in', api_url)
    auth_token = login(api_url, username, password)
    print("auth token", auth_token)
    if auth_token != '':
        print('Success!')
    else:
        print('Ooops! something went wrong')
        sys.exit(1)

    # Test create_repo
    print('Testing create_repo()')
    print('Create your first repository')
    name = input('Repo name: ')
    repo_code = input('Repo code: ')
    repo = create_repo(api_url, auth_token, name, repo_code)
    print(json.dumps(repo, indent=4))
    print('Create a second repository')
    name = input('Repo name: ')
    repo_code = input('Repo code: ')
    repo = create_repo(api_url, auth_token, name, repo_code)
    print(json.dumps(repo, indent=4))

    # Test list_repos
    print('Testing list_repos()')
    repos = list_repos(api_url, auth_token)
    print('repositores list', json.dumps(repos, indent=4))

    # Test list_repo
    print('Testing list_repo()')
    repo_id = int(input('Enter repo id: '))
    repo = list_repo(api_url, auth_token, repo_id)
    print('repository list', json.dumps(repos, indent=4))
    
    # Test update_repo
    print('Testing update_repo()')
    repos = list_repos(api_url, auth_token)
    print('Pick a repository id to update', 
        json.dumps(repos, indent=4))
    repo_id = input('Repository numeric id: ')
    print('Getting repository record', repo_id)
    repo = list_repo(api_url, auth_token, repo_id)
    repo['name'] = input('old name is '+repo['name']+', provide a new name: ')
    print('Now we update')
    result = update_repo(api_url, auth_token, repo_id, repo)
    print('Result is', json.dumps(result, indent=4))
    
    # Test delete_repo
    print('Testing delete_repo()')
    repos = list_repos(api_url, auth_token)
    print('Pick a repository id to update', json.dumps(repos, indent=4))
    repo_id = int(input('Repository numeric id to delete: '))
    result = delete_repo(api_url, auth_token, repo_id)
    print('Result is', json.dumps(result, indent=4))
    print(json.dumps(list_repos(api_url, auth_token), indent=4))
    
    # All done!
    print('Success!')