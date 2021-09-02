import os
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict

import sys

def get_filelist(dir):
 filelist = []
 newDir = dir
 result_list = []
 for s in os.listdir(dir):
  newDir=os.path.join(dir,s)
  filelist.append(newDir)
 for j in filelist:
  if os.path.isdir(j):
   for i in os.listdir(j):
    result_list.append(os.path.join(j,i))
 return result_list

def tokenize(word_str):
    words_list = []
    for split_w in re.split(r'[^a-zA-Z0-9]', word_str.lower()):# O(N)
        if split_w != '':
            words_list.append((split_w))# O(1)
    return words_list





if __name__ == "__main__":
    get_all_json = get_filelist('DEV')
    my_result = defaultdict(lambda: defaultdict(int))

    for json_name in get_all_json[1:10]:
        json_dict = defaultdict(int)
        f = open(json_name,'r')
        result = json.load(f)
        soup = BeautifulSoup(result["content"], 'html.parser')
        total_tokens = tokenize(soup.get_text())

        for word in total_tokens:

            my_result[word][json_name] += 1

            #print(word, json_dict)

    print(my_result)

    print(sys.getsizeof(my_result) )
    print(len(my_result))


'''
list = get_filelist('DEV', [])
print(len(list))
#for e in list:
# #print(e)
with open("DEV/aiclub_ics_uci_edu/906c24a2203dd5d6cce210c733c48b336ef58293212218808cf8fb88edcecc3b.json",'r') as load_f:
    load_dict = json.load(load_f)
print(load_dict['url'])

f = open("DEV/aiclub_ics_uci_edu/906c24a2203dd5d6cce210c733c48b336ef58293212218808cf8fb88edcecc3b.json", 'r')
result = json.load(f)
soup = BeautifulSoup(result["content"], 'html.parser')
print(type(soup.get_text()))
a = soup.get_text()
b = tokenize(a)
print(b)'''