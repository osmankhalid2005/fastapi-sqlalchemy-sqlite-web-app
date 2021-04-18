'''
Here core functions are defined for different operations.
'''
from typing import Dict

from fastapi import Depends, FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def read_form():
    return 'hello world'


########## TO SHOW HOME PAGE #################
@app.get('/home')
def home_get(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request})


########## TO SHOW SINGLE USER FROM A TABLE #################
@app.get('/search_user')
def Search_User_Get(request: Request):
    result=""   
    return templates.TemplateResponse('search_user.html', context={'request': request, 'user': result})

@app.post('/search_user')
def Search_User_Post(request: Request, db: Session = Depends(get_db), user_id: int = Form(...)):
    result = db.query(models.User).filter(models.User.id == user_id).first()    
    return templates.TemplateResponse('search_user.html', context={'request': request, 'user': result, 'user_id': user_id})

########### TO SHOW LIST OF USERS ##########################

@app.get('/show_users')
def Show_Users_Get(request: Request, db: Session = Depends(get_db)):    
    from_limit=0
    to_limit=100
    result = db.query(models.User).offset(from_limit).limit(to_limit).all()   
    return templates.TemplateResponse('show_users.html', context={'request': request, 'result': result, 'from_limit': from_limit, 'to_limit': to_limit})

@app.post('/show_users')
def Show_Users_Post(request: Request, db: Session = Depends(get_db), from_limit: int = Form(...), to_limit: int = Form(...)):
    result = db.query(models.User).offset(from_limit).limit(to_limit).all()   
    return templates.TemplateResponse('show_users.html', context={'request': request, 'result': result, 'from_limit': from_limit, 'to_limit': to_limit})


########## TO EDIT SINGLE USER FROM A TABLE FOR EDIT #################

@app.post('/edit_user')
def Edit_User_Post(request: Request, db: Session = Depends(get_db), user_id: int = Form(...)):                
    result = db.query(models.User).filter(models.User.id == user_id).first()    
    return templates.TemplateResponse('edit_user.html', context={'request': request, 'result': result, 'user_id': user_id})

@app.post('/update_user')
def Update_User_Post(request: Request, db: Session = Depends(get_db), user_id: int = Form(...), user_name: str = Form(...), user_email: str = Form(...), user_address: str = Form(...)):
    db.query(models.User).filter(models.User.id==user_id).update({"name": user_name, "email": user_email, "address": user_address})    
    db.commit()
    result = db.query(models.User).filter(models.User.id == user_id).first()    
    return templates.TemplateResponse('edit_user.html', context={'request': request, 'result': result, 'user_id': user_id})

######### TO DELETE A USER FROM TABLE #########################

@app.post('/delete_user')
def Delete_User_Post(request: Request, db: Session = Depends(get_db), user_id: int = Form(...)):
    db.query(models.User).filter(models.User.id==user_id).delete()
    db.commit()
    from_limit=0
    to_limit=100
    result = db.query(models.User).offset(from_limit).limit(to_limit).all()   
    return templates.TemplateResponse('show_users.html', context={'request': request, 'result': result, 'from_limit': from_limit, 'to_limit': to_limit})

############ TO INSERT A NEW USER IN DATABASE ###################

@app.get('/insert_user')
def Insert_User_Get(request: Request):
    result=""      
    return templates.TemplateResponse('insert_user.html', context={'request': request, 'result': result})

@app.post('/insert_user')
def Insert_User_Post(request: Request, db: Session = Depends(get_db), user_name: str = Form(...), user_email: str = Form(...), user_passwd: str = Form(...), user_address: str = Form(...)):
    db_user = models.User(email=user_email, name=user_name, hashed_password=user_passwd, address=user_address)
    db.add(db_user)
    db.commit()    
    db.refresh(db_user)
    user_id = db_user.id # getting the last newly inserted primary key      
    result = db.query(models.User).filter(models.User.id == user_id).first() 
    return templates.TemplateResponse('search_user.html', context={'request': request, 'result': result, 'user_id': user_id})
      

######### TO DISPLAY ITEMS OF A USER ####################

@app.post('/show_user_items')
def Show_User_Items_Post(request: Request, db: Session = Depends(get_db), user_id: int = Form(...)):
    items = db.query(models.Item).filter(models.Item.owner_id == user_id).all()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse('show_user_items.html', context={'request': request, 'user': user, 'items': items})

######## TO DISPLAY SINGLE ITEM OF A GIVEN USER ##########
@app.post('/show_user_item')
def Show_User_item_Post(request: Request, db: Session = Depends(get_db), item_id: int = Form(...)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    user = db.query(models.User).filter(models.User.id == item.owner_id).first()    
    return templates.TemplateResponse('show_user_item.html', context={'request': request, 'user': user, 'item': item})


######## TO EDIT ITEM ##########
@app.post('/edit_user_item')
def Edit_User_item_Post(request: Request, db: Session = Depends(get_db), item_id: int = Form(...)):
    print(item_id)
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    user = db.query(models.User).filter(models.User.id == item.owner_id).first()    
    return templates.TemplateResponse('edit_user_item.html', context={'request': request, 'user': user, 'item': item})

@app.post('/update_user_item')
def Update_User_item_Post(request: Request, db: Session = Depends(get_db), item_id: int = Form(...), item_title: str = Form(...), item_desc: str = Form(...)):
    db.query(models.Item).filter(models.Item.id==item_id).update({"title": item_title, "description": item_desc})    
    db.commit()    
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    user = db.query(models.User).filter(models.User.id == item.owner_id).first()    
    return templates.TemplateResponse('edit_user_item.html', context={'request': request, 'user': user, 'item': item})

######## TO DELETE A USER ITEM ############
@app.post('/delete_user_item')
def Delete_User_Item(request: Request, db: Session = Depends(get_db), item_id: int = Form(...), user_id: int = Form(...)):
    db.query(models.Item).filter(models.Item.id==item_id).delete()
    db.commit()    
    items = db.query(models.Item).filter(models.Item.owner_id == user_id).all()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse('show_user_items.html', context={'request': request, 'user': user, 'items': items})

############## TO INSERT NEW ITEM FOR A USER ###################

@app.post('/insert_user_item_form')
def Insert_User_Item_Form(request: Request, db: Session = Depends(get_db), user_id: int = Form(...)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse('insert_user_item.html', context={'request': request, 'user': user})


@app.post('/insert_user_item_post')
def Insert_User_Item_Post(request: Request, db: Session = Depends(get_db), user_id: int = Form(...), item_title: str = Form(...), item_desc: str = Form(...)):
    new_item = models.Item(title=item_title, description=item_desc, owner_id=user_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    item_id = new_item.id # getting the last newly inserted primary key      
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()    
    return templates.TemplateResponse('show_user_item.html', context={'request': request, 'item': item, 'user': user})



########## TO SHOW SINGLE USER FROM A TABLE #################
@app.get('/search_item')
def Search_Item_Get(request: Request):     
    return templates.TemplateResponse('search_item.html', context={'request': request})

# The below function is run by ajax code

@app.post('/search_item')
def Search_Item_ajax(item: Dict[str, int], db: Session = Depends(get_db)):
    item_id = item['item_id']    
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        return {"MSG": "NOT_FOUND"}
    else:
        user = db.query(models.User).filter(models.User.id == item.owner_id).first()
        return {"id": item_id, "title": item.title, "description": item.description, "owner_id": item.owner_id, "user_name": user.name, "user_email": user.email }

    
########### TO SHOW LIST OF ITEMS ##########################

@app.get('/show_items')
def Show_Items_Get(request: Request, db: Session = Depends(get_db)):    
    from_limit=0
    to_limit=100
    result = db.query(models.Item).offset(from_limit).limit(to_limit).all()   
    return templates.TemplateResponse('show_items.html', context={'request': request, 'result': result, 'from_limit': from_limit, 'to_limit': to_limit})

@app.post('/show_items')
def Show_Items_Post(request: Request, db: Session = Depends(get_db), from_limit: int = Form(...), to_limit: int = Form(...)):
    result = db.query(models.Item).offset(from_limit).limit(to_limit).all()   
    return templates.TemplateResponse('show_items.html', context={'request': request, 'result': result, 'from_limit': from_limit, 'to_limit': to_limit})
