# Базы данных. Лабораторная работа №3
## Вариант №13
## Выполнил: Любимов Александр, студент группы КВ-42

База данных, со схемой "звезда", где основная сущность это Survey и сущосности входящие в нее это Person и Doctor(также одна дополнительная сущность Hospital). Реализован поиск по ключевой фразе и ключевому слову, так же поиск по дате. Изначально база данных заполняется с помощью json файлов, методом вызываемым вручную во избежание перезаписи.

## Функционал базы данных: 
- Отображение и поиск всех сущностей
- Добавление, удаление и изменение сущностей
- База данных реализована языком MySQL с исрользования ORM

## Пример кода:
- Абстрактный класс для всех сущностей:

```python
class AbstractManager(object):
	def __init__(self, table_name, columns_list):
		self.__table_name = table_name
		self.__columns = columns_list
	def get_objects_where(self, condition):
		try:
			con = mdb.connect('localhost', 'root', 'root', 'db2')
			cur = con.cursor(mdb.cursors.DictCursor)
			cur.execute("SELECT * FROM " + self.__table_name + " " + condition)
			return cur.fetchall()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		finally:
			if con:
				con.close()
	def delete(self, condition):
		try:
			con = mdb.connect('localhost', 'root', 'root', 'db2')
			cur = con.cursor()
			cur.execute("DELETE FROM " + self.__table_name + " " + condition)
			con.commit()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		finally:
			if con:
				con.close()
	def insert(self, row):
		try:
			con = mdb.connect('localhost', 'root', 'root', 'db2')
			cur = con.cursor()
			request = "INSERT INTO " + self.__table_name + "("
			values_part = "VALUES('"
			for column in self.__columns:
				request += column + ", " 
				values_part += str(row[column]) + "', '"

			request = request[:-2] + ") "
			values_part = values_part[:-3] + ")"
			request += values_part

			cur.execute(request)
			con.commit()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		finally:
			if con:
				con.close()
	def insert_all(self, data):
		try:
			con = mdb.connect('localhost', 'root', 'root', 'db2')
			cur = con.cursor()
			for row in data:
				request = "INSERT INTO " + self.__table_name + "("
				values_part = "VALUES('"
				for column in self.__columns:
					request += column + ", " 
					values_part += str(row[column]) + "', '"

				request = request[:-2] + ") "
				values_part = values_part[:-3] + ")"
				request += values_part
				cur.execute(request)

			con.commit()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		finally:
			if con:
				con.close()
	def update(self, id, row):
		try:
			con = mdb.connect('localhost', 'root', 'root', 'db2')
			cur = con.cursor()

			request = "UPDATE " + self.__table_name + " SET "

			for column in self.__columns:
				request += column + "= '" + str(row[column]) +  "', "

			request = request[:-2] + " WHERE id = " + str(id)

			cur.execute(request)
			con.commit()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		finally:
			if con:
				con.close()
	def full_text_search(self, condition):
		try:
			con = mdb.connect('localhost', 'root', 'root', 'db2')
			cur = con.cursor(mdb.cursors.DictCursor)
			cur.execute("SELECT * FROM " + self.__table_name + " " + condition)
			return cur.fetchall()
		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		finally:
			if con:
				con.close()
	def get_all(self):
		return self.get_objects_where("")
	def get_by_id(self, id):
		return self.get_objects_where("WHERE id = " + str(id))[0]
	def delete_all(self):
		self.delete("")
	def delete_by_id(self, id):
		self.delete("WHERE id = " + str(id))
 ```

- Метод отображения списка больниц:
 
```python
def hospitals_list(request):
	msg = False
	if request.method == 'POST' and 'minutes' in request.POST:
		create_event(request.POST['minutes'])
		msg = True
	if 'q' in request.GET and request.GET['q'] != "":
		text = request.GET["q"]
		if request.GET.get("optradio", None) == "word":
			query = Q(name__contains=text) | Q(city__contains=text) | Q(street__contains=text)
		else:
			query = Q(name__exact=text) | Q(city__exact=text) | Q(street__exact=text)
		
		hospitals = Hospital.objects.filter(query)
	else:
		hospitals = Hospital.objects.all()
	context = { 'objects' : hospitals, 'title' : "hospital", 'msg' : msg}
	return render(request, 'CoolApp/objects_list.html', context)
```

- Метод создания события:
 
```python
 def create_event(minutes_to_wait):
    try:
    	con = mdb.connect('localhost', 'root', 'root', 'mydb')
        with con:

            cur = con.cursor()
            cur.execute('SET @@global.event_scheduler = ON;')
            cur.execute("CREATE EVENT logCleaner "
                         "ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL %s MINUTE "
                         "DO CALL clearLog(); " % minutes_to_wait)
            con.commit()
            return 0
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if con:
            con.close()
 ```
 
 
## Примеры работы программы

- Начальная страница:
<img src="https://pp.vk.me/c836432/v836432399/12624/0floqAATqIA.jpg" align="center"/>

- Отображение логов удаления пациентов:
<img src="https://pp.vk.me/c836432/v836432399/1262e/PC0f0NWMe2o.jpg" align="center"/>
