# Базы данных. Лабораторная работа №2
## Вариант №10
## Выполнил: Латюк Сергей, студент группы КВ-42

База данных, со схемой "звезда", где основная сущность это Survey и сущосности входящие в нее это Person и Doctor(также одна дополнительная сущность Hospital). Реализован поиск по ключевой фразе и ключевому слову, так же поиск по дате. Изначально база данных заполняется с помощью json файлов, методом вызываемым вручную во избежание перезаписи.

## Функционал базы данных: 
- Отображение и поиск всех сущностей
- Добавление, удаление и изменение сущностей
- База данных реализована языком MySQL без исрользования ORM

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
	if 'q' in request.GET and request.GET['q'] != "":
		text = request.GET["q"]
		print request.GET.get("optradio", None)
		condition = "WHERE MATCH (name, city, street) AGAINST ('"
		if request.GET.get("optradio", None) == "word":
			text = " ".join(['+' + s for s in text.split()])
			condition += text
		else:
			condition += "\"" + text +"\""
		
		condition += "' IN BOOLEAN MODE);"
		hospitals = ObjectsManager.get_hospitals_manager().full_text_search(condition)
	else:
		hospitals = ObjectsManager.get_hospitals_manager().get_all()
	context = { 'objects' : hospitals, 'title' : "hospital"}
	return render(request, 'CoolApp/objects_list.html', context)
```

- Метод заполнения таблицы:
 
```python
 def populate_tables():

	hospital_data = load_data("files/hospitals.json")
	hospitalManager = HospitalsManager()
	hospitalManager.insert_all(hospital_data["hospitals"])

	person_data = load_data("files/persons.json")
	personManager = PersonsManager()
	personManager.insert_all(person_data["persons"])

	doctor_data = load_data("files/doctors.json")
	doctorManager = DoctorsManager()
	doctorManager.insert_all(doctor_data["doctors"])
	
	survey_data = load_data("files/survey_results.json")
	surveyManager = SurveysManager()
	surveyManager.insert_all(survey_data["SurveyResults"])
 ```
 
 
## Примеры работы программы

- Начальная страница:
<img src="https://pp.vk.me/c836432/v836432399/12610/v66Qd3hdf_M.jpg" align="center"/>

- Отображение списка пациентов:
<img src="https://pp.vk.me/c836432/v836432399/1261a/_z-nrpbvNx0.jpg" align="center"/>
