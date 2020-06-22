import csv
import re
import pymongo
import datetime


def read_data(csv_file, db):
    with open(csv_file, encoding='utf8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            day, month = map(int, line['Дата'].split('.'))
            event = {'artist': line['Исполнитель'],
                     'price': int(line['Цена']),
                     'place': line['Место'],
                     'date': datetime.datetime(year=2020, month=month, day=day),
                     }
            db.event.insert_one(event)


def find_cheapest(db):
    sorted_by_price = db.event.find().sort('price')
    return [(event['artist'], f"{event['price']}", event['place'], str(event['date']))
            for event in sorted_by_price]


def find_by_name(name, db):
    regex = re.compile(f'.*{name}.*', re.IGNORECASE)
    search_by_name = db.event.find({'artist': regex}).sort('price')
    return [(event['artist'], f"{event['price']}", event['place'], str(event['date']))
            for event in search_by_name]


def find_earlist(db):
    sorted_by_date = db['event'].find().sort('date')
    return [(event['artist'], f"{event['price']}", event['place'], str(event['date']))
            for event in sorted_by_date]


if __name__ == '__main__':
    with pymongo.MongoClient() as client:
        db = client['netology']

        read_data('artists.csv', db)

        print('---sort by price---')
        print(*find_cheapest(db), sep='\n')
        part_of_name = 'on'
        print(f'---search by "{part_of_name}"---')
        print(*find_by_name(part_of_name, db), sep='\n')
        print('---sort by date---')
        print(*find_earlist(db), sep='\n')
    
    