from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status

from core.services import BotService, TelegramService
from core.keyboards import *
from core.locales import *
from core.serializers import JustSerializer



class BotViewSet(
        mixins.CreateModelMixin,
        GenericViewSet
    ):
    authentication_classes = []
    permission_classes = []
    serializer_class = JustSerializer


    def create(self, request):
        data = request.data

        data_service = TelegramService(data)
        bot_service = BotService(data)
        
        if data_service.text == START or data_service.text == BACK:
            bot_service.send_message(WELCOME_TEXT, MAIN_MENU_KEYBOARD)
            data_service.set_step("main-menu")

        elif data_service.text == MAIN_MENU_ITEM1:
            bot_service.send_message(UPLOAD_PICS)
            data_service.set_step("pics")
        
        elif data_service.check_step("pics"):
            bot_service.send_message(SEND_LOCATION, LOCATION_KEYBOARD)
            data_service.set_step("location")
        
        elif data_service.check_step("location"):
            bot_service.send_message(SEND_CONTACT, CONTACT_KEYBOARD)
            data_service.set_step("contact")
        
        elif data_service.check_step("contact"):
            bot_service.send_message(WRITE_COMMENT, COMMENT_KEYBOARD)
            data_service.set_step("comment")
        
        elif data_service.check_step("comment"):
            bot_service.send_message(SUCCESS, MAIN_MENU_KEYBOARD)
            data_service.set_step("main-menu")
        
        return Response(status=status.HTTP_200_OK)