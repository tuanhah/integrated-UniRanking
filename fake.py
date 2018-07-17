import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UniRanking.settings")
django.setup()

from UniRanking.random import fake_university

if __name__ == '__main__':
    # while True:  
    #     university_id = input("Enter university id : ") 
    #     if university_id.isdigit(): 
    #         university_id = int(university_id)
    #         break
    
    # fake_university(university_id)
    # print("Completed")
    
    while True:  
        start = input("Start at : ") 
        end = input("End at : ")
        if start.isdigit() or end.isdigit(): 
            start = int(start)
            end = int(end)
            break
    
    
    for i in range(start, end):    
        fake_university(i)
        print("Completed " + str(i))
        