import requests
import lxml
from bs4 import BeautifulSoup
import pandas as pd
base_url = "https://mamifood.org"

def get_categories_list(url):
  f = requests.get(url)
  categories_list = []
  soup = BeautifulSoup(f.text, 'lxml')
  categories = soup.find_all('div', class_='Subgroupbox')
  for category in categories:
    print(category)
    categories_list.append((category))



def get_foods_list(url):
  f = requests.get(url)
  foods_name = []
  soup = BeautifulSoup(f.text, 'lxml')
  foods = soup.find('div', {
  'class': 'm-foodbox'
}).find_all('article')
  for food in foods:
      name = food.contents[3].contents[3].contents[0]
      name = name.replace('طرز تهیه', '')
      url = food.contents[3].contents[3].attrs['href']
      url = base_url + url
      foods_name.append([name, url])
  
  return foods_name

def get_foods_recipe(url):
  food_detail  = {}
  f = requests.get(url)
  soup = BeautifulSoup(f.text, 'html.parser')
  ingred_list = []
  ingredients = soup.find_all('div', class_='dotbetween')
  for ingred in ingredients:
    ingred_name = ingred.find('div', class_='foodstuff')
    ingred_name = ingred_name.find('a', class_='btnCustomer').contents[0]
    ingred_amount = ingred.find('div', class_='amount').contents[0]
    ingred_list.append({"name": ingred_name, "size": ingred_amount})
  
  return ingred_list

# get_foods_recipe("https://mamifood.org/cooking-training/recipe/9879/%D8%B7%D8%B1%D8%B2-%D8%AA%D9%87%DB%8C%D9%87-%D9%BE%DB%8C%D8%AA%D8%B2%D8%A7%DB%8C-%D8%A7%D8%B3%D9%81%D9%86%D8%A7%D8%AC")

if __name__ == "__main__":
  urls = [
    "https://mamifood.org/cooking-training/group/12/%D8%BA%D8%B0%D8%A7%DB%8C-%D8%A7%D8%B5%D9%84%DB%8C"
  ]
  for url in urls:
    urls, category = get_categories_list(url)
    for url in urls:
      urls = get_foods_list(url)
      for url in urls:
        food_dict = get_foods_recipe(url)