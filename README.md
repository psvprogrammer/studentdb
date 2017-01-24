# studentdb
Simple Django project that lets to manage database of the students

CRUD functionality avaliable only for superuser (user:admin psw:admin)

Project deployed on azure:
http://student-db.azurewebsites.net/

To load data from fixtures on empty db:
1. loaddata fixtures/auth/user_data.json	- users
2. loaddata fixtures/app/app_data.json		- students appropriate to users in 1
