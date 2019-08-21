import json
import requests
import schedule
import time
import datetime

# x = datetime.datetime.now()

# print(x.year)
# print(x.strftime("%A")


webhook_url = 'https://outlook.office.com/webhook/cfafe822-a683-482f-9fc5-7090bea57b4b@3928808b-8a46-426b-8f87-051a36bb2f91/IncomingWebhook/dedbfa6c22a043f7acb5d57d7615abcc/2d48d6b7-9201-4514-8d19-0d400a3a22e8'
slack_data = {'text': "Its Dj's turn."}
current_person = 5
No_of_Employee = 5
holidays = ["01/15/19", "05/01/19", "06/05/19", "08/15/19", "09/02/19", "10/02/19", "10/08/19", "10/28/19", "11/01/19", "12/25/19"]

def PostRequest(message):
    response = requests.post(
        webhook_url, data=json.dumps({'text': message}),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to team returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )

def reminder():

    global current_person
    global No_of_Employee
    x = datetime.datetime.now()
    date = x.strftime("%x")
    day  = x.strftime("%A")
    curr_time = x.strftime("%X")

    # print(date)
    # print(day)
    # print(curr_time)

    if(day =="Sunday" or day =="Saturday"):
        PostRequest("Its a weekend!")
    elif(date in holidays):
        PostRequest("Its a holiday!")
    else:
        flag=0
        with open('employee.json') as json_file:
            data = json.load(json_file)
        for p in data['people']:
            if(p['Status']=="0" and p["PresenceStatus"]=="1"):
                current_person = p['name']
                p['Status']="1"         
                flag=1
                break
        if(flag==0):
            for p in data['people']:
                p['Status']='0'
            for p in data['people']:
                if(p['Status']=="0" and p["PresenceStatus"]=="1"):
                    current_person = p['name']
                    p['Status'] = "1"
                    break
                
        with open('employee.json', 'w') as outfile:
            json.dump(data, outfile)
        PostRequest("Hello, Its " + current_person + "'s turn.")

    

# schedule.every(10).seconds.do(reminder)
schedule.every().day.at("14:40").do(reminder)

while True: 
  
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(10) 