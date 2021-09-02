
import os
import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import sys

def get_filelist(dir):
    doct_id = 1
    filelist = []
    newDir = dir
    result_dict = dict()
    for s in os.listdir(dir):
        newDir=os.path.join(dir,s)
        filelist.append(newDir)
    for j in filelist:
        if os.path.isdir(j):
            for i in os.listdir(j):
                result_dict[doct_id] = (os.path.join(j,i))
                doct_id += 1
    json_result = json.dumps(result_dict)
    result_json = open('2/Doc_id.json', 'w')
    result_json.write(json_result)
    result_json.close()
    return result_dict

def tokenize(word_str):
    words_dict = dict()
    check_place = 0
    for split_w in re.split(r'[^a-zA-Z0-9]', word_str.lower()):# O(N)
        check_place += 1
        if split_w != '':
            if split_w not in words_dict:
                words_dict[split_w] = [check_place]# netest list, list[0] is the number of the words, list[1] is a list that contains all of this word's position in the content
            else:
                #words_dict[split_w][0] += 1
                words_dict[split_w].append(check_place)

    return words_dict


def write_partialIndex(my_result, filename):


    sorted_list = [[k, v] for k, v in sorted(my_result.items())]
    result_json = open(filename,'w+')

    for i in sorted_list:
        json_result = json.dumps(i) + "\n"

        result_json.write(json_result)

    result_json.close()


def deal_Word(plist):


    dicts = defaultdict(list)
    for i in plist:
        if i != '':
            l = eval(i)
            dicts[l[0]]+= l[1]


    order_list = [[k, v] for k, v in sorted(dicts.items())]
    read_index = []
    for j in range(len(plist)):
        #print(eval(plist[j]))
        if plist[j] != '' and eval(plist[j])[0] == order_list[0][0]:
            read_index.append( j)


    return [order_list[0], read_index]


def merge_index():

    p1 = open('result_json_newM1_part1.json', 'r')
    p2 = open('result_json_newM1_part2.json', 'r')
    p3 = open('result_json_newM1_part3.json', 'r')

    Big_file = open('BIG_file.json', 'w')

    p1_line = p1.readline()
    p2_line = p2.readline()
    p3_line = p3.readline()

    seek_dict = dict()
    seek_index = open('seek_index.json', 'w')

    #remove empty


    infront = 0
    while p1_line!= '' and p2_line != '' and p3_line != '':

         combine_list = [p1_line, p2_line, p3_line]

         indexs = deal_Word(combine_list)


         to_big =  str(indexs[0][1]) + '\n'

         Big_file.write(to_big)

         string = indexs[0][0]
         index = infront
         infront += len(to_big)
         seek_dict[string] = index


         if 0 in indexs[1]:
             p1_line = p1.readline()
         if 1 in indexs[1]:
             p2_line = p2.readline()
         if 2 in indexs[1]:
             p3_line = p3.readline()

    seek_result = json.dumps(seek_dict)
    seek_index.write(seek_result)
    seek_index.close()


if __name__ == "__main__":
    get_all_json = get_filelist('DEV')
    print(len(get_all_json))
    my_result = dict()
    check = 0
    for json_name in get_all_json.items():
        check += 1
        print(check)
        f = open(json_name[1],'r')
        result = json.load(f)
        soup = BeautifulSoup(result["content"], 'html.parser')
        total_tokens = tokenize(soup.get_text())
        for word_dict in total_tokens.items():
            if word_dict[0] not in my_result:

                my_result[word_dict[0]] = [ [json_name[0],word_dict[1]]]
            else:

                my_result[word_dict[0]].append([json_name[0],word_dict[1]])

        if check == 19000:
            write_partialIndex(my_result, 'result_json_newM1_part1.json')
            my_result.clear()

        elif check == 28000:
            write_partialIndex(my_result, 'result_json_newM1_part2.json')
            my_result.clear()




    write_partialIndex(my_result, 'result_json_newM1_part3.json')
    my_result.clear()
    merge_index()



        #the dict  key is word and value is a list  there are many tuples in there  in the tuple the 1st index is url
        # 2nd index is a list  with 1st total number of words in the url and 2nd is list with all of the position of the words
        # {word:(URL_id,[[total_num][position1,2,3,4]])}

        #[word,id, totoal_num, posting 1,2,3]


        #["the", [1, [10, 70], [2, [11, 71, 186]], [3, [18, 78, 287, 295, 337, 349, 370, 416, 428, 433, 444, 454, 484, 489, 506, 577, 622, 625, 637, 648, 653, 674, 685, 699, 702, 707, 747, 769, 773, 785, 789, 820, 833, 846, 856, 901, 905, 931, 944, 1000, 1140, 1147, 1187, 1280, 1284, 1291, 1306, 1350, 1365, 1377, 1380, 1386, 1453, 1464, 1467, 1480, 1492, 1525, 1530, 1554, 1569, 1575, 1588, 1591, 1630, 1692, 1720, 1738, 1741, 1747, 2136, 2143, 2159, 2164, 2180, 2193, 2197, 2201, 2218, 2263, 2423, 2433, 2448, 2451, 2464, 2467, 2477, 2484, 2504, 2508, 2529, 2535, 2541, 2544, 2554, 2563, 2568, 2572, 2654, 2657, 2664, 2676, 2682, 2686, 2746, 2757, 2780, 2804, 2815, 2837, 2843, 2850, 2856, 2871, 2891, 2981, 3030, 3035, 3106, 3139, 3172, 3279, 3340, 3373]]]]
    '''
    print(len(my_result.keys()))
    json_result = json.dumps(my_result)
    result_json = open('result_json_newM1_part1.json', 'w')
    result_json.write(json_result)
    result_json.close()
    #these four lines use for check memory
    '''






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