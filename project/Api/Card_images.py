import os
import uuid
from werkzeug import secure_filename
from flask_restful import Resource
from flask import request, current_app, g, jsonify, Response
from project.extra import login_required, checke_interface, allowed_image

class upload_card_image(Resource):
    #上传卡片图像的类
    @login_required
    def post(self):
        file = request.files['image']
        #因前端要求修改
        ''' if file and allowed_image(file.filename):
            #str1是用户的id
            #str2是随机的uuid
            #str3是图片的后缀
            str1 = g.user.get_user_id()
            str2 = str(uuid.uuid1()).split("-")[0]
            str3 = '.' + file.filename.rsplit('.')[1]

            filename = str1 + str2 + str3 

            file.save (os.path.join(
                current_app.config['CARD_IMAGES_FOLDER'],
                filename))
        else:
            return jsonify(status = 0,\
                        message = "failed") '''
        str1 = g.user.get_id()
        str2 = str(uuid.uuid1()).split("-")[0]
        str3 = '.png'
        
        filename = str1 + str2 + str3 

        file.save (os.path.join(
            current_app.config['CARD_IMAGES_FOLDER'],
            filename))

        #文件上传成功，返回文件名
        return jsonify(status = 1,\
                    filename = filename)