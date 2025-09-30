from auth_app.models import Account
from profile_app.models import Profile

user1, _ = Account.objects.get_or_create(username='homer', first_name='Homer', last_name='Simpson', email='homer@gmail.de', is_staff=True, user_type='customer')
user1.set_password('!Test123')
user1.save()
Profile.objects.create(user=user1, location='Springfield', description='Liebt Donuts und Fernsehen', tel='+49 157 1234567')

user2, _ = Account.objects.get_or_create(username='bart', first_name='Bart', last_name='Simpson', email='bart@gmail.de', is_staff=True, user_type='customer')
user2.set_password('!Test123')
user2.save()
Profile.objects.create(user=user2, location='Springfield', description='Schüler mit vielen Streichen', tel='+49 160 9876543')

user3, _ = Account.objects.get_or_create(username='sonic', first_name='sonic', last_name='The Hedgehog', email='sonic@gmail.de', is_staff=True, user_type='business')
user3.set_password('!Test123')
user3.save()
Profile.objects.create(user=user3, location='Berlin', description='Super schneller blauer Igel', tel='+49 151 1122334')

user4, _ = Account.objects.get_or_create(username='tales', first_name='Miles', last_name='Prower', email='tales@gmail.de', is_staff=True, user_type='business')
user4.set_password('!Test123')
user4.save()
Profile.objects.create(user=user4, location='Hamburg', description='Mechaniker und Erfinder mit zwei Schwänzen', tel='+49 152 5566778')

user5, _ = Account.objects.get_or_create(username='mm', first_name='Max', last_name='Mustermann', email='mustermann@gmail.de', is_staff=True, user_type='business')
user5.set_password('!Test123')
user5.save()
Profile.objects.create(user=user5, location='München', description='Standard-Testnutzer für Demos', tel='+49 170 8899001')

user6, _ = Account.objects.get_or_create(username='jessie', first_name='jessie', last_name='blue', email='jessie@gmail.de', is_staff=True, user_type='business')
user6.set_password('!Test123')
user6.save()
Profile.objects.create(user=user6, location='Köln', description='Hat eine Vorliebe für blaue Kleidung', tel='+49 162 3344556')

user7, _ = Account.objects.get_or_create(username='april', first_name='April', last_name='Eagle', email='april@gmail.de', is_staff=True, user_type='business')
user7.set_password('!Test123')
user7.save()
Profile.objects.create(user=user7, location='Düsseldorf', description='Journalistin mit Sinn für Gerechtigkeit', tel='+49 155 7788990')

user8, _ = Account.objects.get_or_create(username='saber', first_name='Saber', last_name='Rider', email='saber@gmail.de', is_staff=True, user_type='business')
user8.set_password('!Test123')
user8.save()
Profile.objects.create(user=user8, location='Leipzig', description='Anführer der Saber Riders', tel='+49 159 2233445')

user9, _ = Account.objects.get_or_create(username='Darth Vader', first_name='Anakin', last_name='Skywalker', email='vader@gmail.de', is_staff=True, user_type='business')
user9.set_password('!Test123')
user9.save()
Profile.objects.create(user=user9, location='Frankfurt', description='Mächtiger Sith-Lord mit dunkler Vergangenheit', tel='+49 175 4455667')

user10, _ = Account.objects.get_or_create(username='Dr. Robotnik', first_name='Ivo', last_name='Robotnik', email='robotnik@gmail.de', is_staff=True, user_type='business')
user10.set_password('!Test123')
user10.save()
Profile.objects.create(user=user10, location='Stuttgart', description='Bösewicht und genialer Erfinder', tel='+49 176 9988776')