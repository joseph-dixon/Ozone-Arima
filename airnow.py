import requests
from datetime import datetime, timedelta
import pandas as pd
import time

dataset = [["DateObserved","Ozone","PM2.5","PM10"]]
current_date = str(datetime.today()).split()[0]
to_subtract = 0

while current_date != '2009-12-31' :


    to_subtract += 1
    to_add = [current_date]
    current_date = str(datetime.today() - timedelta(to_subtract)).split()[0]
    url = 'https://www.airnowapi.org/aq/observation/zipCode/historical/?format=text/csv&zipCode=80211&date=' + current_date + 'T00-0000&distance=25&API_KEY=96D376A4-F6D3-492E-B307-7663C073795D'
    r = requests.get(url)

    try:
        if r.status_code == 429 :
            print('Stopped at: '+str(current_date))
            while r.status_code == 429 :
                time.sleep(60)
                url = 'https://www.airnowapi.org/aq/observation/zipCode/historical/?format=text/csv&zipCode=80211&date=' + current_date + 'T00-0000&distance=25&API_KEY=96D376A4-F6D3-492E-B307-7663C073795D'
                r = requests.get(url)

            print('Resuming with date: ' + str(current_date))
            url = 'https://www.airnowapi.org/aq/observation/zipCode/historical/?format=text/csv&zipCode=80211&date=' + current_date + 'T00-0000&distance=25&API_KEY=96D376A4-F6D3-492E-B307-7663C073795D'
            r = requests.get(url)
            lines = r.text.split('\n')
            for line in lines[1:4]:
                row = line.split(',')
                to_add.append(int(row[8].strip('\"')))
            dataset.append(to_add)
            print('Appending for '+str(current_date) + ': ' + str(to_add[1:]))

        else:
            lines = r.text.split('\n')
            for line in lines[1:4]:
                row = line.split(',')
                to_add.append(int(row[8].strip('\"')))
            dataset.append(to_add)
            print('Appending for '+str(current_date) + ': ' + str(to_add[1:]))

    except:
        print("Error at: %s, with addition %s" % (current_date,to_add))



df = pd.DataFrame(dataset)
df.to_csv('/Users/josephdixon/Desktop/airnow_data.csv')
