from model import model
import os, json
from urllib.parse import parse_qs
from random import randint

def POSTResponse(url, content):
    
    data = parse_qs(content)
    response = ''
    if url == '/homepage':
        response = open('./views/homepage.tmp').read()
        
    elif url == '/auth':
        email = data['email'][0]
        password = data['password'][0] 
        if model.check_password(email,password):
            credentials = model.get_user_credentials(email)
            response = json.dumps(credentials)
            
    elif url == '/register':
        name = data['name'][0]
        email = data['email'][0]
        password = data['password'][0]
        country_code = data['country'][0]
        if model.get_user_id(email) == -1:
            response = model.add_new_user(name, email, password, country_code, 0)
        else:
            response = "User already registered."
        
    elif url == '/get-bio':
        user_id = data['userid'][0]
        old_content = model.get_user_bio(user_id)
        response = json.dumps({"content": old_content})
        
    elif url == '/get-poem':
        poem_id = data['poem_id'][0]
        poem = model.get_poem(poem_id)
        response = json.dumps({"title": poem[0], "poem_type": poem[1], "text": poem[2], "poem_id":poem[3]})
    
    elif url == '/update-poem':
        poem_id = data['poem_id'][0]
        poem_type = data['poem_type'][0]
        title = data['title'][0]
        content = data['content'][0]
        response = model.update_poem(poem_id, poem_type, title, content)
        
    elif url =='/delete-poem':
        poem_id = data['poem_id'][0]
        response = model.delete_poem(poem_id)

    elif url == '/save-poem':
        user_id = data['userid'][0]
        poem_type = data['poem_type'][0]
        title = data['title'][0]
        content = data['content'][0]
        response = model.add_new_poem(user_id, poem_type, title, content)
        
    elif url == '/save-bio':
        userid = data['userid'][0]
        content = data['content'][0]
        response = model.add_new_bio(userid,content)
        
    elif url == '/poets':
        namelist = model.poetsList();
        names = ""
        for poet in sorted(namelist):
            names += "<a href=\"javascript:ShowPoems("+str(poet[1])+")\">"
            names += poet[0] +"</a><br>"
        response = open("./views/poems.tmp").read().replace("#poets#",names)
        
    elif url == '/user-poems':
        poet_id = data['user_id'][0]
        logged = data['logged_id'][0]
        poems = model.get_all_poems_of_poet(poet_id)
        response = '<h2 class="text-info" style="font-family:Lato;">'
        response += model.poetName(poet_id)+"</h2>"
        i = 0;
        for poem in poems:
            i += 1
            response += '<a href="javaScript:TogglePoem('+'\''+str(i)+'\')">'
            response += '<span class="mr-3">'+poem[1]+'</span>'
            response += '<span class="text-warning" style="font-size:12px"><i class="fas fa-star"></i></span>'*randint(1,5)
            response += '</a><br>'
            response += '<div id="'+str(i)+'"class="d-none">'+poem[2].replace('\n',"<br>")
            if logged != '0':
                response += '<div class="d-flex bg-light">'
                if logged != poet_id:
                    response += '<div class="text-success mr-auto p-2" style="font-size:24px;"><i class="fas fa-thumbs-up"></i></div>'
                if logged == poet_id:
                    response += '<div class="p-2 mr-1"><button  class="btn-sm btn-primary" onclick="EditPoem('+str(poem[0])+')">Edit</button></div>'
                    response += '<div class="p-2 mr-1"><button  class="btn-sm btn-primary" onclick="DeletePoem('+str(poem[0])+')">Delete</button></div>'
                response += '<div class="p-2"><button  class="btn-sm btn-primary"  onclick="NotImplemented()">Translate</button></div>'
                response += '<div class="p-2"><button  class="btn-sm btn-primary"  onclick="NotImplemented()">Translations</button></div>'
                response +="</div>"
            response += '</div>'
            # else:
            #     response += "<br>"
        
    elif url == '/user-bio':
        user_id = data['user_id'][0]
        logged_id = data['logged_id'][0]
        response = '<h4 class="text-muted">Biography</h4>'
        bio = model.get_user_bio(user_id)
        if bio != None:
            response += '<div class="text-justify w-75">'+bio[0].replace('\n',"<br>")+'</div>'
        if user_id == logged_id:
            response +='<div class="d-flex bg-light"><div class="p-2 mr-1"><button class="btn btn-primary input-xs" onclick="PublishBio()">Edit</button></div></div>'
    return response

def GETResponse(path):
    filename = path.split("/")[-1]
    if filename == "":
        filename = './views/index.html'
    file_ext = filename.split(".")[-1]  
    mode = "r"
    if file_ext == "html" or file_ext == 'tmp':
        content_type = "text/html"
    elif file_ext == "js":
        filename = './static/js/'+filename
        content_type = "text/plain"
    elif file_ext == "css": 
        filename = './static/css/'+filename
        content_type = "text/css"
    elif file_ext in ["ico","jpg","jpeg","png","gif"]:
        filename = './static/images/'+filename
        content_type = "image/x-icon"
        mode = "rb"
    else:
        return ["Page not found".encode('utf-8'),"text/html"]
    
    if os.access(filename, os.R_OK) and not os.path.isdir(filename):
        # Cient asking for a file
        file_content = open(filename, mode).read()
        if mode == "r": 
            file_content = file_content.encode('utf-8')
        return [file_content, content_type]
    else:
        return ["Page not found".encode('utf-8'),"text/html"]
