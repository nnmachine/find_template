import requests
import ast
import json

#form.txt - файл с формами, где формы представлены в виде:
#f_name1=value1&f_name2=value2
file_forms = open('forms.txt', 'r')
list_forms = []
for line in file_forms:
    #Убираются переносы строки
    list_forms.append(line.rstrip())

#Формы передаются на урл
for form in list_forms:
    value = '?'+form
    url = 'http://127.0.0.1:8000/get_form/'+value
    request = requests.post(url)
    response = requests.get(url)
    #если response можно сделать словарем, значит вернулась форма...
    try:
        form_dict = ast.literal_eval(response.text)
        print(json.dumps(form_dict, indent=4))
    #...иначе вернулось имя шаблона
    except:
        print(response.text)
file_forms.close()
