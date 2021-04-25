from processor import Dictionary
import os
import logging

DB_ENGINE = os.environ.get("DB_ENGINE")
DB_ENGINE = DB_ENGINE.lower()
# DB_ENGINE = 'mysql'

logging.basicConfig(filename='dictionary_log.log', level=logging.INFO,\
    format='%(asctime)s ----- %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
eng = Dictionary(DB_ENGINE)

if __name__ == "__main__":
    word = "a"
    while word != "\\end":
        word = input("Please enter a word or \\end to exit: ")
        word = word.lower()
        if DB_ENGINE == 'mysql':
            results = eng.db_query_mysql(word)
            if type(results) == list:
                for result in results:
                    print(result[0])
            else:
                print(results)
            
            
            
            

