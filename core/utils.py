from django.conf import settings
import requests as r
import os


def clean_phone_number(phone):
    if not phone or len(str(phone)) < 3:
        return ""
    
    phone = str(phone)
    if phone.endswith(".0"):
        phone = phone[:-2]
    
    result = str(phone) \
            .replace("(", "") \
            .replace(")", "") \
            .replace("/", "") \
            .replace("\\", "") \
            .replace("-", "") \
            .replace("_", "") \
            .replace("+", "") \
            .replace(" ", "") \
            .replace(".", "") \
            .replace("\n", "") \
            .replace("\t", "")
    
    sign = "+"
    if len(result) <= 9:
        sign = "+998"
    
    if len(result) == 10:
        sign = ""
    
    if len(result) == 0:
        return "-"

    return sign + result


def is_photo(file_path):
    TYPES = ["jpg", "jpeg"]
    parts = file_path.split(".")
    if len(parts):
        return parts[-1].lower() in TYPES
    return False


def is_video(file_path):
    parts = file_path.split(".")
    if len(parts) == 1:
        return True
    return False


def download_telegram_photo(path):
    BASE_URL = "https://api.telegram.org/file/bot{}/{}".format(settings.BOT_TOKEN, path)
    print(BASE_URL)
    response = r.get(BASE_URL)
    if response.status_code == 200:
        writing_path = os.path.join(settings.MEDIA_ROOT, *path.split("/")[1:])
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "temp"), exist_ok=True)
        with open(writing_path, mode="wb") as file:
            file.write(response.content)
        
        parts = path.split("/")
        return (writing_path, os.path.join(settings.MEDIA_URL, parts[-1]))

    return False