#-*- coding:utf-8 -*-
from flask import Flask,request,jsonify,abort,url_for
from flask_cors import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = " you can't guess it for 989079878 years"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yu98224734@localhost/PetShow'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
CORS(app,supports_credentials=True)

db=SQLAlchemy(app)
auth =HTTPBasicAuth()



#user begin--->
class User(db.Model):
    """user model"""
    __tablename__ = "users"
    _id = db.Column(db.String(16),primary_key=True,nullable=False)
    user_nickname = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    phonenumber = db.Column(db.String(11),unique=True,nullable=False)
    gender = db.Column(db.String(1),nullable=True)
    avatar_path = db.Column(db.String(128),nullable=True)
    motto = db.Column(db.String(256),nullable=True)
    address = db.Column(db.String(30),nullable=True)
    joined_time = db.Column(db.DateTime,nullable=False)
    grade = db.Column(db.Integer,nullable=False,default=1)

    #password 
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.__password_hash = pwd_context.encrypt(password + \
                                         self.__user_name + \
                                         current_app.config['SALT'])
    def verify_password(self, password):
        return pwd_context.verify(password + \
                                self.__user_name + \
                                current_app.config['SALT'],\
                                self.password_hash)
    def generate_auth_token(selfi,expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in = expiration)        return s.dumps({'id':self._id,'username':self._user_name})
    
#regist ---------->

@app.route('/api/regist',methods = ['POST'])
def new_user():
   # user_id = uuid.uuid1()
    nickname = request.json['nickname']
    phonenumber = request.json['phonenumber']
    password = request.json['password'] 
    if User.query.filter_by(phonenumber=phonenumber).first() is not None:
        return (jsonify({'massage':'The phone number has been registered!'})),400
    if user_nickname is None or password is None:
        return (jsonify({'massage':' The account number and password must not be empty.'})),400
    new = User(user_nickname=nickname,phonenumber = phonenumber)
    db.session.add(new)
    db.session.commit()
    return (jsonify({'message':'ok'})) 
    
login -------->
@app.route('/api/Login',methods = ['POST'])
def loginin():
   
    phone = request.json['phonenumber']
    password = request.json['password']
   
    user = User.query.filter_by(phonenumber=phone).first()
    if user.verify_password(password):
        g.user = User.query.filter_by(user_id = user_id).first()
        token = g.user.generate_auth_token().decode("utf8")
        return (jsonify({"status":1,"token":token}))
     


#card image --------->
@app.route('/api/card_images',methods=['POST'])
def images_of_card():
     
    _ALLOWED_EXTENSIONS = set (['jpg','png','jpeg'])
    def allowed_file(self,filename):
        return '.' in filename and \
            filename.rsplit('.',1)[1] in \
            self.__ALLOWED_EXTENSIONS
    def post(self):
        file = request.files['image']
        if file and self.allowed_file(file.filename):
            #str1是用户的id
            #str2是用户发布的图片数
            #str3是图片的后缀
            str1 = g.user.get_user_id()
            str2 = g.user.get_image_number()
            str3 = '.' + file.filename.rsplit('.')[1]

            filename = str1 + str2 + str3 

            file.save (os.path.join(\
                current_app.config['CARD_IMAGES_FOLDER'],\
                filename))
            
            #文件上传成功，返回文件名
            return jsonify(status = 1,filename = filename)
        #没有文件或文件格式不是允许的文件格式，返回"f",失败
        else:
            return jsonify(status = 0,message = "failed")

#post card------->
@app.route('/api/Post_card',methods=['POST'])
def post(self):
        card_dict = request.json

        try:
            card_dict['content']
            card_dict['images']

            #内容和图片不能同时没有
            if not (card_dict['content'].strip() or \
                    card_dict['images'].strip()):
                return jsonify(status = 0,\
                message = "content and image can't exist at the same time.")
        
        except KeyError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        except AttributeError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")        
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        #用于调试查看的
        print ("content:%s,images:" % \
            (card_dict['content']),\
            card_dict['images'])

        try:      
            g.user.create_card(card_dict)
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        return jsonify(status = 1,\
                        message = "success")
#




if __name__ == '__main__':
    app.run(debug = True)
ycp@ycpppp:~/my_pet/app$ vim api.py 
ycp@ycpppp:~/my_pet/app$ cat api.py
#-*- coding:utf-8 -*-
from flask import Flask,request,jsonify,abort,url_for
from flask_cors import *
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = " you can't guess it for 989079878 years"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yu98224734@localhost/PetShow'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
CORS(app,supports_credentials=True)

db=SQLAlchemy(app)
auth =HTTPBasicAuth()



#user begin--->
class User(db.Model):
    """user model"""
    __tablename__ = "users"
    _id = db.Column(db.String(16),primary_key=True,nullable=False)
    user_nickname = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    phonenumber = db.Column(db.String(11),unique=True,nullable=False)
    gender = db.Column(db.String(1),nullable=True)
    avatar_path = db.Column(db.String(128),nullable=True)
    motto = db.Column(db.String(256),nullable=True)
    address = db.Column(db.String(30),nullable=True)
    joined_time = db.Column(db.DateTime,nullable=False)
    grade = db.Column(db.Integer,nullable=False,default=1)

    #password 
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.__password_hash = pwd_context.encrypt(password + \
                                         self.__user_name + \
                                         current_app.config['SALT'])
    def verify_password(self, password):
        return pwd_context.verify(password + \
                                self.__user_name + \
                                current_app.config['SALT'],\
                                self.password_hash)
    def generate_auth_token(selfi,expiration = 600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in = expiration)        return s.dumps({'id':self._id,'username':self._user_name})
    
#regist ---------->

@app.route('/api/regist',methods = ['POST'])
def new_user():
#获取前端发来的信息。
   # user_id = uuid.uuid1()
    nickname = request.json['nickname']
    phonenumber = request.json['phonenumber']
    password = request.json['password'] 
    if User.query.filter_by(phonenumber=phonenumber).first() is not None:
        return (jsonify({'massage':'The phone number has been registered!'})),400
    if user_nickname is None or password is None:
        return (jsonify({'massage':' The account number and password must not be empty.'})),400
    new = User(user_nickname=nickname,phonenumber = phonenumber)
    db.session.add(new)
    db.session.commit()
    return (jsonify({'message':'ok'})) 
    
#login -------->
@app.route('/api/Login',methods = ['POST'])
def loginin():
   
    phone = request.json['phonenumber']
    password = request.json['password']
   
    user = User.query.filter_by(phonenumber=phone).first()
    if user.verify_password(password):
        g.user = User.query.filter_by(user_id = user_id).first()
        token = g.user.generate_auth_token().decode("utf8")
        return (jsonify({"status":1,"token":token}))
     

#card beghin -------------->

class Tag(db.Model):
    __tablename__ ="tags"
    _id = db.Column(db.String(16),nullable=False)
    tag_name = db.Column(db.String(32),nullable=False)

class Card_with_tag(db.Model):
    __tablename__ = "card_with_tag"
    _id = db.Column(db.String(16),nullable=False)
    card_id = db.Column(db.String(16),nullable=False)
    tag_id = db.Column(db.String(16),nullable=False)

class Pet(db.Model):
    __tablename__ = "pets"
    pet_id = db.Column(db.String(16),nullable=False,primary_key=True)
    category = db.Column(db.String(32),nullable=False)
    detailed_category = db.Column(db.String(64),nullable=True)
    pet_name = db.Column(db.Stirng(20),nullable=False)
    user_id = db.Column(db.String(16),nullable=False)
    time = db.Column(db.DateTime,nullable=False)
    gender = db.Column(db.String(1),nullable=False)
     
class Card(db.Model):
    """card model"""
    __tablename__ = "cards"
    _id = db.Column(db.String(16),primary_key= True,nullable=False)
    user_id = db.Column(db.String(16),nullable=False)
    pet_id = db.Column(db.String(16),nullable=False)
    card_content = db.Column(db.Text,nullable=True)
    card_image_path = db.Column(db.String(128),nullable=True)
    card_time = da.Column(db.DateTime,nullable=False)
    


#card image --------->
@app.route('/api/card_images',methods=['POST'])
def images_of_card():
     
    _ALLOWED_EXTENSIONS = set (['jpg','png','jpeg'])
    def allowed_file(self,filename):
        return '.' in filename and \
            filename.rsplit('.',1)[1] in \
            self.__ALLOWED_EXTENSIONS
    def post(self):
        file = request.files['image']
        if file and self.allowed_file(file.filename):
            #str1是用户的id
            #str2是用户发布的图片数
            #str3是图片的后缀
            str1 = g.user.get_user_id()
            str2 = g.user.get_image_number()
            str3 = '.' + file.filename.rsplit('.')[1]

            filename = str1 + str2 + str3 

            file.save (os.path.join(\
                current_app.config['CARD_IMAGES_FOLDER'],\
                filename))
            
            #文件上传成功，返回文件名
            return jsonify(status = 1,filename = filename)
        #没有文件或文件格式不是允许的文件格式，返回"f",失败
        else:
            return jsonify(status = 0,message = "failed")

#post card------->
@app.route('/api/Post_card',methods=['POST'])
def post(self):
        card_dict = request.json

        try:
            card_dict['content']
            card_dict['images']

            #内容和图片不能同时没有
            if not (card_dict['content'].strip() or \
                    card_dict['images'].strip()):
                return jsonify(status = 0,\
                message = "content and image can't exist at the same time.")
        
        except KeyError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")
        except AttributeError:
            return jsonify(status = 0,message = "error!!please don't try to do someting wrong")        
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        #用于调试查看的
        print ("content:%s,images:" % \
            (card_dict['content']),\
            card_dict['images'])

        try:      
            g.user.create_card(card_dict)
        except:
            return jsonify(status = 0,message = "look like something wrong happen")

        return jsonify(status = 1,\
                        message = "success")
#card for time------->
@app.route('/api/time_card')
def card_for_time():
    user = request.json['user_id']
    pets = Pet.query.filter_by(user_id=user).all()
    for pet in pets:
        things = Card.query.filter_by(pet_id=pet.pet_id).
        
#the comment begin ---------->

class Comments(db.Models):
    __tablename__ = 'comments'
    _id = db.Column(db.String(16),primary_key=True)
    card_id = db.Column(db.String(16), nullable=False)
    to_user_id = db.Column(db.String(16),nullable=False)
    comment_content = db.Column(db.Text,nullable=False)

class Praise(db.Models):
    __tablename__ = 'praise'
    card_id = db.Column(db.String(16),nullable=False)
    user_id = db.Column(db.String(16),nullable=False)

#the chat --------->



#relationship begin ---------->

class Follow(db.Models):
    __tablename__ = 'follow'    
    user_id = db.Column(db.String(16),nullable=False)
    be_concerned_id = db.Column(db.String(16),nullable=False)
    id_ = db.Column(db.String(16),primary_key = True)

# who follow who?---------->







#to be continued --------------->
if __name__ == '__main__':
    app.run(debug = True)

