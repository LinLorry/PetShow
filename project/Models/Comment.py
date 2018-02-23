import uuid
from project import db
from .PetLogDataError import PetLog_DataError

#----->评论方面

class Comment(db.Model):
    __tablename__ = "comments"
    __id = db.Column(db.String(16), primary_key=True, nullable=False)
    __card_id = db.Column(db.String(16), nullable=False)
    __user_id = db.Column(db.String(16), nullable=False)
    __to_user_id = db.Column(db.String(16), nullable=False)
    __comment_content = db.Column(db.Text, nullable=False)
    __comment_time = db.Column(db.String(20),nullable=False)
    
    #------>发布卡片的部分
    def comment_on_card(self, comment_card_dict):
        '''示例：newcomment_dict{'card_id':'67687',
                                'user_id':'787897',
                                'to_user_id':'79980980',
                                'commtent_content':'真的有点很烦呢。'}'''
        self.__id = str(uuid.uuid1()).split("-")[0]
        self.__card_id = comment_card_dict['card_id']
        self.__user_id = comment_card_dict['user_id']
        self.__to_user_id = comment_card_dict['to_user_id']
        self.__comment_content = comment_card_dict['comment_content']
        self.__comment_time = comment_card_dict['comment_time']
        return True

    def check_data(self, user_id, data_dict):
        try:
            if not data_dict['content'] or \
                    not data_dict['card_id'] or \
                    not data_dict['time']:
                raise PetLog_DataError(
                    'Error : One comment card lack something')
            else:
                data_dict['user_id'] = user_id
        except PetLog_DataError as error:
            print(error.message)
        except KeyError as error:
            print("KeyError : Don't has " + error)
        else:
            return data_dict

    def insert(self):
        db.session.add(self)
        db.session.commit()
        return True

    #------->删除评论功能（是否能？）
    def delete(self, comment_id):
        comm = self.query.filter_by(_id=comment_id).first()
        db.session.delete(comm)
        db.session.commit()
        return True
    
    #----->查看某卡片的所有评论
    def card_all_comment(self,card_id):
        all = self.query.filter_by(_Comment__card_id=card_id).all()
        peo = []
        for one in all:
            a = User.query.filter_by(_User__id =one.__user_id).first()
            peo.append({"author":"ome","id":one.__id,"reply_to":one.__to_user_id,"time":one.__comment_time,"content":one.__comment_content})
        return peo
    
    #------>获取某条评论的发布者id
    def comment_user(self,comment_id):
        one = self.query.filter_by(_Comment__id=comment_id).first()
        return one
