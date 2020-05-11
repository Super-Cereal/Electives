from requests import get, post


# правильный зaпрос к одному пользователю
print(get('http://localhost:5000/api/users/2').json())
print(f'\033[32m{"!" * 90}\033[0m')

# запрос к несуществующему пользователю
print(get('http://localhost:5000/api/users/9999').json())
print(f'\033[32m{"!" * 90}\033[0m')

# правильный запрос ко всем пользователям
print(get('http://localhost:5000/api/users').json())
print(f'\033[32m{"!" * 90}\033[0m')

# правльная регистрация
print(post('http://localhost:5000/api/users',
           json={'surname': 'sur',
                 'name': 'nam',
                 'age': 38,
                 'password': '12390',
                 'type': 1,
                 'email': 'em@mail'}).json())
print(f'\033[32m{"!" * 90}\033[0m')

# регистрация без обязательных значенией
print(post('http://localhost:5000/api/users',
           json={'surname': 'sur',
                 'name': 'nam',
                 'password': '12390',
                 'email': 'em@mail'}).json())
print(f'\033[32m{"!" * 90}\033[0m')
