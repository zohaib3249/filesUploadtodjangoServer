import requests
import os
import hashlib
import os

import requests
import json
def read_in_chunks(file_object, CHUNK_SIZE):
    while True:
        data = file_object.read(CHUNK_SIZE)
        if not data:
            break
        yield data
path=("/home/zohaibyousaf/Desktop/easyfiles.7z")


in_file = open(path, "rb")

CHUNK_SIZE = 500*1024

size = os.path.getsize(path)

#URL="https://youtubeboosterserver.herokuapp.com/LoginUser"
URLPut='http://127.0.0.1:8000/fileUploadPut/'
URL='http://127.0.0.1:8000/chunked_upload/'

path1=os.path.basename(path)
filename, file_extension = os.path.splitext(path1)
print(filename,file_extension)
data={
    "filename":filename+file_extension,
    "userid":2,
    "TotalFileSize":size,
    
}
headers={}
r=requests.put(url=URLPut,data=data) 
ServerResponse=json.loads(r.text)
print(ServerResponse)
in_file.seek(ServerResponse['index'])
if ServerResponse['status']=="Incomplete":
    for chunk in read_in_chunks(in_file, CHUNK_SIZE):
        index=int(ServerResponse['index'])
      
        print(ServerResponse['TotalFileSize'],ServerResponse['uploadedFileSize'])
        TotalSize=ServerResponse['TotalFileSize']
        offset = index + len(chunk)
        #index = offset 
        try: 
            dfile = {'Fileid':str(ServerResponse['id']),'filename':ServerResponse['filename'],'index':str(index),'offset':str(offset)} 
            r = requests.post(URL,data=dfile,files={"file": chunk})
            ServerResponse=json.loads(r.text)
            if ServerResponse['status']=="Complete":
                print("File uploaded ")
                break
            
            print(ServerResponse)
        except Exception as e:
            print(e)
else:
    print("FIle already exist")
    in_file.close()
        









































def getToken():
    URL = 'http://127.0.0.1:8000/chunked_upload/'

    client = requests.session()

    # Retrieve the CSRF token first
    client.get(URL)  # sets cookie
    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        csrftoken = client.cookies['csrftoken']
    
        return csrftoken
   

    from requests.auth import HTTPBasicAuth
    url = 'http://127.0.0.1:8000/chunked_upload/'

    path=("/home/zohaibyousaf/Desktop/easyfiles.7z")

    auth = HTTPBasicAuth(username='abdullah', password='pakistan123456')
    in_file = open(path, "rb")
    file_data = in_file.read()
    CHUNK_SIZE = 100

    size = os.path.getsize(path)

    offset = 0
    print(f'bytes {offset}-{offset + len(file_data) -1}/{size}')

    """r = requests.put(
        url,
        headers={
            "Content-Range": f'bytes {offset}-{offset + len(data) -1}/{size}',
        },
        data={"field_name": 'field_name'},
        files={'file': data},
        auth=auth,
    )"""
    r = requests.put(
        url,
        headers={
            "Content-Range": "bytes {}-{}/{}".format(offset, offset + len(file_data) - 1, size),
        },
        data={"filename": "build_file"},
        files={'file': file_data},
        auth=auth,
        
    )




def send():
   

    

    file = '/home/zohaibyousaf/Desktop/easyfiles.7z'

    size = os.path.getsize(file)

    hash_md5 = hashlib.md5()

    CHUNK_SIZE = 100

    with open(file, 'rb') as f:
        url = 'http://127.0.0.1:8000/chunked_upload/'
        offset = 0
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b''):
            hash_md5.update(chunk)
            res = requests.put(
                url,
                data={'filename': 'my_new_file'},
                files={'file': chunk},
                headers={
                    'Content-Range': f'bytes {offset}-{offset + len(chunk) -1}/{size}'
                },
                
            )
            print(res.text)
            offset = int(res.json().get('offset'))
            url = res.json().get('url')
        finalize = requests.post(url, data={'md5': hash_md5.hexdigest()}, auth=auth)
        print(finalize.status_code)
        print(finalize.json())

