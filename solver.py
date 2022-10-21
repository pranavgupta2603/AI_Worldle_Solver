import numpy as np
import json
def check_double(grey_list, yellow_list, green_list, doubles=[]):
    for i in green_list:
        for j in grey_list:
            if i[0] == j[0]:
                doubles.append(j)
                grey_list.remove(j)
    for i in yellow_list:
        for j in grey_list:
            if i[0] == j[0]:
                doubles.append(j)
                grey_list.remove(j)
    return grey_list, doubles

def check_yellow(word, yellow_list):
    prime = False
    if len(yellow_list) == 0:
        return True
    for y in yellow_list:
        if word.find(y[0]) != -1 and word[y[1]] != y[0]:
            prime = True
        else:
            prime=False
            break
            
    return prime
            
def check_grey(word, only_greys, grey_list, doubles):
    
    if len(grey_list) == 0:
        return False
    for i in range(0, len(word)):
        if (word[i], i) in doubles:
            return True
        if word[i] in only_greys:
            return True
    else:
        return False
    
def check_green(word, green_list):
    prime = False
    if len(green_list) == 0:
        return True
    for g in green_list:
        if word[g[1]] == g[0]:
            prime = True
        else:
            prime = False
            break
    return prime
    	
def solver(letters, num):
    file = open("dictionary.json")
    data = json.load(file)
    data = list(data.keys())
    x = [i for i in data if len(i) == 5]
    letters = letters[:num] #do this only when wordle is already completed
    #letters.append([('p', "green"), ('a', "green"), ('s', "grey"), ('s', 'green'), ('e', 'green')])
    print(len(x))
    
    grey_list = list(set([(j[0],  i.index(j)) for i in letters for j in i if j[1] == "grey"]))
    yellow_list = list(set([(j[0], i.index(j)) for i in letters for j in i if j[1] == "yellow"]))
    green_list = list(set([(j[0], i.index(j)) for i in letters for j in i if j[1] == "green"]))
    grey_list, doubles = check_double(grey_list, yellow_list, green_list)
    
    only_greys = [i[0] for i in grey_list]
    """
    print("***********")
    print(doubles)
    print(only_greys)
    print("***********")
    print(grey_list)
    print(yellow_list)
    print(green_list)"""

    short = {} #consists of all possible words
    finalised = ["0", "0", "0", "0", "0"]
    for i in x:
        if not(check_grey(i, only_greys, grey_list, doubles)):
            if check_yellow(i, yellow_list):
                if check_green(i, green_list):
                    short[i] = 0
                    
    for i in green_list:
        finalised[i[1]] = i[0]
        
    
    let_dict = {}
    prime = False
    for i in short:
        for j in range(0, len(i)):
            for g in green_list:
                if g[0] == i[j] and g[1] == j:
                    prime = True
            if prime == False:
                if i[j] not in let_dict:
                    let_dict[i[j]] = 1
                else:
                    let_dict[i[j]] += 1
            prime=False
    let_dict = dict(sorted(let_dict.items(), key=lambda item: item[1])) #all letters

    #print(short)
    #print(finalised)
    #print(let_dict)
    
    word_count = []
    for i in range(0, len(finalised)):
        if finalised[i] == "0":
            for let in let_dict:
                for word in short:
                    if word[i] == let:
                        
                        word_count.append((let, i))
                        #print(let, word)
    temp_dict = {}
    for i in list(set(word_count)):
        print(i, word_count.count(i))
        key = i[0] + str(i[1])
        temp_dict[key] = word_count.count(i)
    print(temp_dict)    
    score_words = {}
    for word in short:
        total = 0
        splitted_word = list(word)
        for i in range(0, len(splitted_word)):
            #print((splitted_word[i] + str(i)))
            if (splitted_word[i] + str(i)) in temp_dict:
                total += temp_dict[splitted_word[i] + str(i)]
        short[word] = total
    short = dict(sorted(short.items(), key=lambda item: item[1]))
    print()
    print()
    print(short)





