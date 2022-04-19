from core.locales import *


MAIN_MENU_KEYBOARD = [
    [
        {
            "text": MAIN_MENU_ITEM1
        }
    ]
]

LOCATION_KEYBOARD = [
    [
        {
            "text": LOCATION_BUTTON,
            "request_location": True
        }
    ]
]

CONTACT_KEYBOARD = [
    [
        {
            "text": CONTACT_BUTTON,
            "request_contact": True
        }
    ]
]

COMMENT_KEYBOARD = [
    [
        {
            "text": NO_COMMENT
        }
    ]
]


# def get_mfy_text(mfy):
#     text = "👆<b>MFY nomi: {}</b>".format(mfy.title)

#     qvp = mfy.qvp

#     text += "\n\n🏥Mudiri: {}".format(qvp.manager)
#     text += "\n☎️Telefon raqami: {}".format(clean_phone_number(qvp.manager_phone))
#     text += "\n👨‍⚕️Oilaviy shifokor: {}".format(qvp.doctor)
#     text += "\n☎️Telefon raqami: {}".format(clean_phone_number(qvp.doctor_phone))
#     text += "\n📍Manzil: {}".format(qvp.address)
    
#     return text