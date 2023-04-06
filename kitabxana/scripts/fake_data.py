import os
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitap_pazari.settings')

import django
django.setup()

### Modellerimize ve django içeriklerine erişmek için yukarıdaki gibi ayarlamaları yapmamız lazım
### SIRALAMA ÇOK ÖNEMLİ

from django.contrib.auth.models import User
from faker import Faker
import requests



def set_user():
    fake = Faker('en_US')
    f_name = fake.first_name()
    l_name = fake.last_name()
    u_name = f'{f_name.lower()}_{l_name.lower()}'
    email = f'{u_name}@{fake.domain_name()}'
    print(f_name, l_name, email)

    user_check = User.objects.filter(username=u_name)

    while user_check.exists():
        u_name = u_name + random.randrange(1, 99)
        user_check = User.objects.filter(username=u_name)


    user = User(
        username = u_name,
        first_name = f_name,
        last_name = l_name,
        email = email,
        is_staff = fake.boolean(chance_of_getting_true=50),
    )

    user.set_password('Testing321..')
    user.save()
    print('User created', u_name)


from kitablar.api.serializers import KitabSerializers
    
    
def kitab_ekle(konu):
     fake = Faker(['en_US'])
     url ='https://openlibrary.org/search.json'         # url-i aliriq
     payloads = {'q': konu}                             # query keyini funksiyadaki bizim yazdigimiz atributa = edirik ki biz ora bir sey gonderdikde bir basa urle otursun
     response = requests.get(url, params=payloads)      # daha sonra responsumuzu yaziriq, url ve parametrlerimizi daxil edirik
    
     if response.status_code != 200:                            #yoxlama yaradiriq eyer gelen status code 200 deyilse bize xeta kodu gondersin deyirik
         print('Hatali istek yapildi', response.status_code)
         return 
        
     jsn = response.json()                                     #yox eyer 200 durse jsonu al deyirik.
    
     kitablar = jsn.get('docs')               # Indi ise bizim json faylimizda bir cox bolmeler var.Bu bolmerden biri 'docs'dur.Bu 'docs' un icinde kitab dictleri ve kitab haqqinda muxtelif bilgiler var. Bize basqa seyler lazim olmadigi ucun biz 'docs' bolmesini aliriq

     for kitab in kitablar:                 #daha sonra kitablar ucun loop yaradib datamizi dict formasinda aliriq
        data = dict(
            isim = kitab.get('title'),
            yazar = kitab.get('author_name'),
            aciklama = kitab.get('subject'),
            yayim_tarihi = fake.date_time_between(start_date='-10y', end_date='now',tzinfo=None)
        )
        
        serializer = KitabSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            continue