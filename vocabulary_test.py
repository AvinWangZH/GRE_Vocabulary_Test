'''
Functions should be added:
1. statistical analysis
2. mixation testing system
'''


import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError

    
def initiallize_word_list():
    
    list_num = -1
    
    while int(list_num) not in range(100):
        list_num = input('Which word list do you want to initialize? (Enter a number): \n')
        try:
            int(list_num)
        except ValueError:
            list_num = -1
        
    
    word_list = []
    word_dict = {}
    word = ''
    syn_mul_choice_list = []
    temp = []
    
    print('Please enter the word.')
    print('Type "stop" when you finished.')
    
    while word != 'stop':
        word = input()
        if word != 'stop':
            temp = word.split(' ')
            if len(temp) == 1:
                word_list.append(temp[0])
                syn_mul_choice_list.append([])
            else:
                word_list.append(temp[0])
                syn_mul_choice_list.append(temp[1:])
                
            
    for i in word_list:
        word_dict[i] = {'unsure_new': 0, 'do_not_know_new': 0, 'unsure_past': 0, 'do_not_know_past': 0, 'syn_mul_choice': [], 'meaning': []} 
        index = word_list.index(i)
        word_dict[i]['syn_mul_choice'] = syn_mul_choice_list[index]
        
    with open('list_%s.json' %(list_num), 'w') as f:
        json.dump(word_dict, f)
        
    return
    
    
    
def reset_word_list():
    list_num = input('Which word list do you want to reset? (Enter a number): \n')
    
    with open('list_%s.json' %(list_num), 'r') as f:
        word_dict = json.load(f)  
    
    for i in word_dict:
        word_dict[i]['unsure_past'] = 0
        word_dict[i]['do_not_know_past'] = 0
    
    with open('list_%s.json' %(list_num), 'w') as f:
        json.dump(word_dict, f)
        
    return
    
def single_word_list_test():
    list_num = input('Which word list do you want to test on? (Enter a number): ')
    
    with open('list_%s.json' %(list_num), 'r') as f:
        word_dict = json.load(f)  
        
    for i in word_dict:
        print(i)
        label = input()
        if label == ' ':
            word_dict[i]['unsure_past'] += 1
            word_dict[i]['unsure_new'] += 1
        elif label == 'd':
            word_dict[i]['do_not_know_past'] += 1
            word_dict[i]['do_not_know_new'] += 1
            #check_word_meaning_E(i)
            
    print('\nYou have finished List%s test.' %(list_num))
            

    
    print("\nThe unsure words are:")
    for i in word_dict:
        if word_dict[i]['unsure_new'] != 0:
            print(i)
            
    transition = ' '
    while transition != '':
        transition = input('\nEnter return to continue to check meaning')    
    
    print('\nUnsure List: ')
    for i in word_dict:
        if word_dict[i]['unsure_new'] != 0:
            print(i)  
            check = input('Do you want to check meaning? (y/(enter)): ')
            if check == 'y':
                print('')
                print(i)
                check_meaning = i
                check_word_meaning(check_meaning) 
                
    transition = ' '
    while transition != '':
        transition = input('\nEnter return to continue to learn unknown words')     
           
    print("\nThe words you don't know are:")
    for i in word_dict:
        if word_dict[i]['do_not_know_new'] != 0:
            print(i)  
            
    transition = ' '
    while transition != '':
        transition = input('\nEnter return to continue')    
            
    print('\nUnknown List: ')
    
    for i in word_dict:
        if word_dict[i]['do_not_know_new'] != 0:
            print(i)  
            check = input('Do you want to check meaning? (y/(enter)): ')
            if check == 'y':
                print('')
                print(i)
                check_meaning = i
                check_word_meaning(check_meaning)      
    
       
    check_hist = ''
    while check_hist != 'y' and check_hist != 'n':
        check_hist = input('\nDo you want to check the history? (y/n): ')
    
    if check_hist == 'y':
        
        print('\nUnsure list:')
        for i in word_dict:
            if word_dict[i]['unsure_past'] != 0:
                print(i, word_dict[i]['unsure_past'])
        
        print('\nUnsure words check->')
        for i in word_dict:
            if word_dict[i]['unsure_past'] != 0:
                print(i, word_dict[i]['unsure_past'])
                check = input('Do you want to check meaning? (y/(enter)): ')
                if check == 'y':
                    print('')
                    print(i)
                    check_meaning = i
                    check_word_meaning(check_meaning)
                    
        print('\nUnknown list:')
        for i in word_dict:
            if word_dict[i]['do_not_know_past'] != 0:
                print(i, word_dict[i]['do_not_know_past'])        
                
        print('\nUnknown words ->')
        for i in word_dict:
            if word_dict[i]['do_not_know_past'] != 0:
                print(i, word_dict[i]['do_not_know_past'])  
                check = input('Do you want to check meaning? (y/(enter)): ')
                if check == 'y':
                    print('')
                    print(i)
                    check_meaning = i
                    check_word_meaning(check_meaning)                
    
        check_meaning = ''
        while check_meaning != 'n':
            check_meaning = input('\nCheck word (type "n" to quit): \n')
            if check_meaning != 'n':
                check_word_meaning(check_meaning)
                
                
    for i in word_dict:
        word_dict[i]['do_not_know_new'] = 0
        word_dict[i]['unsure_new'] = 0    
                
    with open('list_%s.json' %(list_num), 'w') as f:
        json.dump(word_dict, f)  

    
    print('Data has been stored.')
    print('List%s test finished.' %(list_num))

    return
        
    
    
def unsure_past_test():
    pass
    
def do_not_know_past_test():
    pass
    
    
def check_word_meaning(word):
    url = 'http://dictionary.cambridge.org/dictionary/english-chinese-simplified/' + word

    try:
        word_bsObj = BeautifulSoup(urlopen(url), "lxml")
    except HTTPError:
        return

    
    count = 0
    try:
        word_type = word_bsObj.find('span', {'class': 'posgram ico-bg'}).text
        print('(' + word_type + ')')
    except AttributeError:
        return
    
    #print('\nPart of Speech: ' + word_type + '\n')
    for child in word_bsObj.find('span', {'class': 'sense-body'}).children:
        try:
            if 'def-block' in child.attrs['class']:
                count += 1
                print('%d. ' %(count) + child.b.text) 
                print('   ' + child.find('span', {'class': 'trans'}).text.strip() + '\n') 
                
        except AttributeError:
            pass
        
    return 

 
if __name__ == '__main__':
    
    
    #initiallize_word_list()
    single_word_list_test()
    
    #with open('list_10.json', 'r') as f:
        #a = json.load(f)
    
    
            
    

    
    
    
        
        
