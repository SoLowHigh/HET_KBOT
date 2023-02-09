# import requests
# from bs4 import BeautifulSoup

# url = 'https://en.wikipedia.org/wiki/' +'нью-йорк'
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.find('div', class_='no-article-text-sister-projects'))

# with open('docs/NoU', 'r') as f_cmd:
#     f = f_cmd.read()



# if any(s in line for line in f):
#     print("Строка s содержит в себе одну из строк в файле f")
# else: print('no')

# print(f)

obj = {'flag1': 1, 'flag2': True}

print(obj['flag1'])