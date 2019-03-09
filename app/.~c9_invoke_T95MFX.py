from model import model
import os, json
from urllib.parse import parse_qs
from random import randint

def POSTResponse(url, content):
    
    data = parse_qs(content)
    response = ''
    if url == '/homepage':
        response = open('./views/homepage.tmp').read()
        
    elif url == '/form-signin':
        response = open('./views/form_signin.tmp').read()
        
    elif url == '/form-login':
        response = open('./views/form_login.tmp').read()
        
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
        if model.get_user_id(email) == -1:
            response = model.add_new_user(name, email, password, 0)
        else:
            response = "User already registered."
            
    elif url == '/form-poem':
        response = open('./views/form_poem.tmp').read()
        
    elif url == '/form-bio':
        user_id = data['userid'][0]
        old_content = model.get_user_bio(user_id)
        form  = open('./views/form_bio.tmp').read()
        response = json.dumps({"content": old_content, "form": form})

    elif url == '/save-poem':
        user_id = data['userid'][0]
        title = data['title'][0]
        content = data['content'][0]
        response = model.add_new_poem(user_id,title,content)
        
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
        print(data)
        poet_id = data['user_id'][0]
        logged = data['logged_id'][0]
        poems = model.get_all_poems_of_poet(poet_id)
        response = "<h2 class='text-info' style='font-family:Lato;'>"+model.poetName(poet_id)+"</h2>"
        for poem in poems:
            response += "<h4>"+"<span class='mr-3'>"+poem[0]+'</span>'
            response += '<span class="text-warning" style="font-size:12px"><i class="fas fa-star"></i></span>'*randint(1,5)+"</h4>"
            response += '<div class="d-none">'+poem[1].replace('\n',"<br>")+"</div>"
            if logged != '0':
                response += '<div class="d-flex bg-light">'
                response += '<div class="text-success mr-auto p-2" style="font-size:24px;"><i class="fas fa-thumbs-up"></i></div>'
                response += '<div class="p-2 mr-1"><button  class="btn-sm btn-primary" onclick=""style="font-size:12px;font-family:Lato;">Edit</button></div>'
                response += '<div class="p-2"><a  class="btn btn-sm btn-primary" style="font-size:12px;font-family:Lato;" href="#" role="button">Translate</a></div>'
                response +="</div>"
            # else:
            #     response += "<br>"
        
    elif url == '/user-bio':
        user_id = data['user_id'][0]
        response = '<h3 class="text-muted">Biography</h3>'
        bio = model.get_user_bio(user_id)
        if bio != None:
            response += bio[0].replace('\n',"<br>")
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
