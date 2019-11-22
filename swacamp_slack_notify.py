import requests
import json
import datetime
from urllib import quote
import sys
import time

schedule_file = sys.argv[1]
slack_hook_url = sys.argv[2]

def calculateTimeToLookForInSchedule(date):
    minute = date.minute
    hour = date.hour

    roundedMinute = 5 - (minute % 5) + minute
    if minute != 0 and roundedMinute == 0:
        hour += 1

    return formatTime(hour, roundedMinute)


def sendNotificationToSlackFor(entries, day, time):
    text = reduce(lambda x, y: x + '\n' + y,
                  map(lambda x: x['loc'][0] + ": " + x['title'], entries)
                  )
    text = "@channel *Now starting " + day + " " + time + "*\n" + text
    r = requests.post(slack_hook_url,
                      data='{"text":"' + text.encode('utf-8') + '"}')


def formatTime(hour, minute):
    return '{num:02d}'.format(num=hour) + ':' + '{num:02d}'.format(num=minute)


def tick(schedule_file, slack_hook_url):
    now = datetime.datetime.now()

    with open(schedule_file, 'r') as myfile:
        content = myfile.read()
    content = content.replace("callback(", "")[:-1]

    minute = now.minute
    timeToLookFor = calculateTimeToLookForInSchedule(now)
    dateToLookFor = str(datetime.date.today())
    print "Notify entries of {dateToLookFor} {timeToLookFor}"
    jsonContent = json.loads(content)

    forDay = filter(lambda x: x['date'] == dateToLookFor, jsonContent)
    forTime = filter(lambda x: x['time'] == timeToLookFor, forDay)

    if len(forTime) > 0:
        sendNotificationToSlackFor(forTime, dateToLookFor, timeToLookFor)



while (True):
    time.sleep(70)
    tick(schedule_file, slack_hook_url)






