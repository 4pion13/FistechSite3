
from sweater.models import SendDataProducts, Processors, Videocards
from sweater import login_manager, db, app, mail,  Message, ALLOWED_EXTENSIONS
def show_processor():
    show = Processors.query.all()
    print(show)
    return show

def show_videocards():
    show_card = Videocards.query.all()
    print(show_card)
    print(type(show_card))
    return show_card

def show_applications_database():
    show_applications_data = SendDataProducts.query.filter_by(status="1").all()
    '''for x in show_applications_data:
        application_list = []
        application_list.append(x)
        print(application_list)
        print(type(application_list))'''

    return show_applications_data

def show_test_data(id_aplication):
    show_applications_data = SendDataProducts.query.filter_by(id=id_aplication).all()

    return show_applications_data


