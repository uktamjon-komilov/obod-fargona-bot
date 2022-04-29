from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework import status

from core.services import BotService, TelegramService
from core.keyboards import *
from core.locales import *
from core.serializers import JustSerializer
from core.utils import download_telegram_photo
from core.models import *



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
            bot_service.send_message(UPLOAD_PICS, PICS_KEYBOARD)
            data_service.set_step("pics")
        
        elif data_service.text == UPLOAD_PICS_FINISHED:
            bot_service.send_message(SEND_LOCATION, LOCATION_KEYBOARD)
            data_service.set_step("location")
        
        elif data_service.check_step("pics"):
            photo_id = data_service.photo_id
            if photo_id:
                path = bot_service.get_file(photo_id)
                result = download_telegram_photo(path)
                if isinstance(result, tuple):
                    media_path = result[1]
                    appeal = Appeal.objects.get(id=data_service.appeal.id)
                    photo = Photo(appeal=appeal)
                    photo.photo = media_path
                    photo.save()
            else:
                bot_service.send_message(PICS_CORRECT_TYPE, PICS_KEYBOARD)
        
        elif data_service.check_step("location"):
            if data_service.location:
                bot_service.send_message(SEND_CONTACT, CONTACT_KEYBOARD)
                data_service.save_appeal_location()
                data_service.set_step("contact")
            else:
                bot_service.send_message(LOCATION_CORRECT_TYPE, LOCATION_KEYBOARD) 
        
        elif data_service.check_step("contact"):
            if data_service.contact:
                bot_service.send_message(WRITE_COMMENT, COMMENT_KEYBOARD)
                data_service.save_appeal_contact()
                data_service.set_step("comment")
            else:
                bot_service.send_message(CONTACT_CORRECT_TYPE, CONTACT_KEYBOARD) 
        
        elif data_service.check_step("comment"):
            bot_service.send_message(SUCCESS, MAIN_MENU_KEYBOARD)
            data_service.save_appeal_comment()

            try:
                appeal = data_service.appeal
                photos = Photo.objects.filter(appeal=appeal)

                caption = f"""📞Telefon raqam: {appeal.phone}\n💬Izoh: {appeal.comment}\n📍Lokatsiya: {appeal.google_maps_url}"""

                if photos.count() > 1:
                    images = [photo.url for photo in photos]
                    bot_service.send_images(images, caption=caption, chat_id=settings.CHANNEL_ID)
                elif photos.count() == 1:
                    bot_service.send_photo(photos.first().url, caption=caption, chat_id=settings.CHANNEL_ID)
            except Exception as e:
                print("error", e)
            
            data_service.save_appeal_submitted()
            data_service.set_step("main-menu")
        
        return Response(status=status.HTTP_200_OK)