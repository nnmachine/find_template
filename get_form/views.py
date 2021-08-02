from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tinydb import TinyDB, Query
import json
import re
#Функции валидации и сравнения шаблона были разложены по разным файлам,
#но это было менее удобно для написания



#Функция сравнения шаблона и формы
def DictComp(template, form):
    #Массив типов полей формы для того, чтобы смотреть, полностью ли шаблон удовлетворяет форме,
    #если все поля шаблона есть в форме, но в форме есть некоторые поля, которых в шаблоне нет
    set_form = set(form.values())
    for key in template:
        if key == 'name':
            continue
        if key in form.keys() and template[key] == form[key]:
            if form[key] in set_form:
                #Удаление из множества типов формы типа, если данный тип присутствует в шаблоне, как написано выше
                set_form.remove(form[key])
        #Если ключа шаблона нет среди ключей формы, или значение шаблона и формы при одинаковом ключе различны,
        #то данный шаблон уже не подходит
        if key not in form.keys() or template[key] != form[key]:
            return False
    #Если в массиве остались значения, значит в шаблоне нет необходимых для формы значенй, а значит шаблон не подходит
    if bool(set_form):
        return False
    #Иначе подходит
    return True


def phone_validation(data):
    #Если нужна валидация без учета пробело, то нужно использовать
    # такую регулярку: ^ \d{11}$
    if not re.match(r'^ \d \d{3} \d{3} \d{2} \d{2}$', data):
        return False
    return True


def email_validation(data):
    if not re.match(r'^[0-9A-Za-z\._-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', data):
        return False
    return True


def date_validation(data):
    if re.match(r'^\d\d\d\d-\d\d-\d\d$', data):
        data = data.split('-')
        if int(data[1]) == 0 or int(data[1]) > 12:
            return False
        if int(data[2]) == 0 or int(data[2]) > 31:
            return False
        return True
    if re.match(r'^\d\d\.\d\d\.\d\d\d\d$', data):
        data = data.split('.')
        if int(data[0]) == 0 or int(data[0]) > 31:
            return False
        if int(data[1]) == 0 or int(data[1]) > 12:
            return False
        return True
    return False


#Валидация каждого поля формы
def validation(data):
    for item in data:
        if date_validation(data[item]):
            data[item] = 'date'
        elif phone_validation(data[item]):
            data[item] = 'phone'
        elif email_validation(data[item]):
            data[item] = 'email'
        else:
            data[item] = 'text'
    return data


#Функция, обрабатывающая урл /get_form
@csrf_exempt
def get_form(request):
    db = TinyDB('DBTemplates.json')
    templates = db.all()
    #Словарь из переданной урлу строки и его приведение
    #к виду {'':''} из такого вида {'':['']}
    post_form = dict(request.GET)
    for key in post_form:
        post_form[key] = post_form[key][0]
    post_form = validation(post_form)
    #Массив подходящих имен шаблонов
    #Если нужно наиболее подходящее поле, то реализовать это можно через разность размеров
    #формы и подходящего шаблона. Где разность будет наименьшей, тот шаблон
    #наиболее подходящий
    names = []
    for template in templates:
        if DictComp(template, post_form):
            names.append(template['name'])
    #Если подходящие шаблоны есть, возвращаем их имена
    if names:
        return HttpResponse(names)
    #Иначе возвращаем форму с типами полей
    return HttpResponse(json.dumps(post_form))

