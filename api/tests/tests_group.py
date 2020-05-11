from requests import get


# правильный зaпрос к одному факультативу
print(get('http://localhost:5000/api/groups/1').json())
print(f'\033[32m{"!" * 90}\033[0m')

# запрос к несуществующему факультативу
print(get('http://localhost:5000/api/groups/9999').json())
print(f'\033[32m{"!" * 90}\033[0m')

# правильный запрос ко всем факультативам
print(get('http://localhost:5000/api/groups').json())
print(f'\033[32m{"!" * 90}\033[0m')
