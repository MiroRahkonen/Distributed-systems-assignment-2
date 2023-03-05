import xmlrpc.client
import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring, SubElement, ElementTree

server = xmlrpc.client.ServerProxy('http://localhost:3000')

def main():
    while(1>0):
        print('Select one of the following options: ')
        print('1) Print topic')
        print('2) Add new entry')
        print('0) Stop')
        option = int(input('Your choice: '))
        if(option == 1):
            printTopic()
        elif(option == 2):
            createEntry()
        elif(option == 0):
            print('Stopping...')
            break
        else:
            print('\nInvalid input\n')
    return


def createEntry():
    topic = input('Topic: ')
    noteName = input('Name of note: ')
    noteText = input('Enter text: ')
    time = datetime.datetime.now()
    formattedTime = time.strftime('%d/%m/%Y - %H:%M:%S')
    data = str(server.addnote(topic,noteName,noteText,formattedTime))
    print(data)
    return


def printTopic():
    i = 1

    topic = input('Input topic: ')
    data = str(server.printTopic(topic))
    if(data == '\nNo topic found\n'):
        #No such topic exists, printing response
        print(data)
        return

    xmlTree = ET.ElementTree(ET.fromstring(data))
    root = xmlTree.getroot()
    
    for note in root:
        noteText = note.find('text')
        noteTimestamp = note.find('timestamp')

        print(f'\n*Note {i}*')
        print('Name: '+note.get('name'))
        print('Note: '+noteText.text)
        print('Time added: '+noteTimestamp.text)
        i += 1
    print()
    return
    
main()