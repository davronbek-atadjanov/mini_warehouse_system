1. git clone https://github.com/davronbek-atadjanov/mini_warehouse_system.git
2. python -m venv venv
3. source venv/bin/activate (Linux) yoki venv\Scripts\activate (Windows)
4. pip install -r requirements.txt

 Migrate qilmasdan oldin o'zlaringizni databaselaringizni ma'lumotlarini setting.py dagi databasega kiritishingiz kerak bo'ladi va keyin migrat qilishingiz mumkin bo'ladi.
 Bu dastur PostgresSql uchun moslashtirilgan,

5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py createsuperuser
8. python manage.py runserver

