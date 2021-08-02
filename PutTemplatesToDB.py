from tinydb import TinyDB, Query
import ast


#Функция, которая складывает записанные в файле templates_to_db.txt
#шаблоны в БД. В templates_to_db.txt шаблон должен иметь следующий вид:
#{'name':'template name', 'field1':'value1', 'field2':'value2'}
db = TinyDB('DBTemplates.json')
templates_txt = open('templates_to_db.txt', 'r')
for line in templates_txt:
    new_field = ast.literal_eval(line.rstrip())
    db.insert(new_field)

