import urllib.request
import argparse
import datetime
import logging
import sys

#1 As per request, logging level set to Error
LOG_FILENAME = 'errors.log'
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.ERROR,
)

with open(LOG_FILENAME, 'rt') as f:
    body = f.read()

#2 Request data via URL and decode them with 'utf-8'.
def downloadData(self):
    with urllib.request.urlopen(self) as response:
        html = response.read().decode('utf-8')
    Data = html.split('\n')
    return Data

#3 Pop out the header and footer
def processData(Data):

    Data.pop(0)
    Data.pop(len(Data)-1)

#4 create individual record in a list and put into the newlist
    newlist=[]
    for i in Data:
        newlist.append(i.split(','))

    ID = []
    Name = []
    Date = []
    birthday = []
    temp = []
    formatting =[]

#5 extracted ID, Name, and Date from the newlist
    for item in newlist:
        ID.append(item[0])
        Name.append(item[1])
        Date.append(item[2])

#6 removed special character from all records and put them in to temp list
    for position in Date:

            temp = position.replace("/", '')
            temp = temp.replace("-", '')
            temp = temp.replace("*", '')
            temp = temp.replace("//", '/')
            formatting.append(temp)

#7 Try to converter string into correct format and catach the exception with their index
#To prevent the datetime mododule filtered the unconvertable data, I assigned a None value to each exception record to maintain data integrity

    index = 0
    for i in formatting:

        try:
            birthday.append(datetime.datetime.strptime(i, '%d%m%Y').strftime("%Y-%m-%d"))
            index +=1

        except Exception as e:
            index +=1
            #print(i, index)
            logging.error("This is a incorrect datetime format")
            birthday.insert(index, None)

#8 Convert 3 lists in to Dict
    return dict(zip(ID, zip(Name, birthday)))

#Accept user input and display the result in IDE or Command line
def displayPerson(id, personData):
    print(personData[str(id)])

if __name__ == '__main__':
#9 Use argparse module to accepet parameter from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="enter an url")
    args = parser.parse_args()
    print("Your didn't provide an URL. Status: " + str(args.url))
    csvData = downloadData(args.url)
    personData = processData(csvData)

    #10 url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'

    try:
        id = int(input("Enter an ID number: "))

        if id <= 0:
            print("Program Exited.")
            # program will exit when user enter ID number <=0
            sys.exit()
        elif id <= 100:
            displayPerson(id, personData)
        elif id >100:
            #program will exit when uer enter ID number > 100
            print("User ID doesn't exist")
            sys.exit()
    except ValueError:
        print("User doesn't exist. Please enter a number between 1 to 100")import urllib.request