from pydantic import EmailStr

class UserDbServices():

    def create_user(user):
        ...

    def get_user_by_id(user_id: int):
        ...


    def get_user_by_email(email: EmailStr):
        ...
    
    def update_user(id: int):
        ...

    def delete_user(user_id: int):
        ...
    