import urllib2
import csv
import json
import sys
import time

target_file = sys.argv[1]
google_spreadsheet_url = sys.argv[2]

def minutes_from(value):
    return int(value[:-3]) * 60 + int(value[-2:])


class Entry:
    def __init__(self, row):
        self.id = row['id'].rstrip()
        self.title = row['title'].rstrip()
        self.date = row['date'].rstrip()
        self.start = row['start'].rstrip()
        self.end = row['end'].rstrip()
        self.room = row['room'].rstrip()
        if self.end and self.start:
            self.duration = self.__duration()

    def __duration(self):
        return minutes_from(self.end) - minutes_from(self.start)

    def isValid(self):
        return self.id and self.title and self.date and self.start and self.end and self.room and self.duration


def load_content():
    response = urllib2.urlopen(google_spreadsheet_url)
    reader = csv.DictReader(response)
    rows = []
    for row in reader:
        try:
            rows.append(Entry(row))
        except:
            print 'cannot parse ' + str(row)

    nonEmptyRows = filter(lambda row: row.isValid(), rows)
    return map(lambda row: {
        'id': row.id,
        'title': row.title,
        'date': row.date,
        'time': row.start,
        'mins': row.duration,
        'loc': [row.room],
        'desc': ''
    }, nonEmptyRows)


def as_file_content(content):
    return 'callback(' + json.dumps(content, ensure_ascii=False) + ')'


def write_file(content, file):
    f = open(file, "w")
    f.write(content)


def update():
    print 'updating...'
    to_write = as_file_content(load_content())
    write_file(to_write, target_file)


while (True):
    time.sleep(5)
    update()
