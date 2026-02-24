import requests


class ApiManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.website = "https://static-maps.yandex.ru/v1"
        
    def get_pic(self, width: float, height: float, scale):
        '''Метод для получения картинки с карты. 
        Аргументы: широта, долгота, масштаб'''
        url_arguments = f"?ll={width},{height}&spn={scale[0]},{scale[1]}&apikey={self.api_key}"
        return requests.get(self.website+url_arguments), self.website+url_arguments