from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET
import datetime
from xml.etree.ElementTree import fromstring, SubElement, ElementTree


def addNote(inputTopic,inputNoteName,inputNoteText):
    topicList = []
    response = ''

    time = datetime.datetime.now()
    formattedTime = time.strftime('%d/%m/%Y - %H:%M:%S')
    
    xmlTree = ElementTree()
    try:
        xmlTree.parse('db.xml')
    except ET.ParseError:
        #If parsing empty file, creating a new tree
        xmlTree = ElementTree(fromstring('<data></data>'))
    root = xmlTree.getroot()
    
    #Adding all topic names to list so we can check if the topic already exists
    for topic in root:
        topicList.append(topic.attrib['name']) 


    if inputTopic in topicList:
        #Topic already exists, adding new note
        index = topicList.index(inputTopic)
        topicRoot = root.findall('topic')[index]

        newNote = SubElement(topicRoot,'note')
        newNote.set('name',inputNoteName)
        noteText = SubElement(newNote,'text')
        noteText.text = inputNoteText
        noteTimestamp = SubElement(newNote,'timestamp')
        noteTimestamp.text = formattedTime
        response = 'New note added\n'
        
    else:
        #Topic doesn't exist, creating new topic tree
        newTopic = SubElement(root,'topic')
        newTopic.set('name',inputTopic)
        
        note = SubElement(newTopic,'note')
        note.set('name',inputNoteName)
        noteText = SubElement(note,'text')
        noteText.text = inputNoteText

        noteTimestamp = SubElement(note,'timestamp')
        noteTimestamp.text = formattedTime
        response = f"New topic '{inputTopic}' and note created\n"
    
    ET.indent(xmlTree, space='\t',level=0)
    xmlTree.write('db.xml')
    return response

def printTopic(searchTopic):
    topicList = []

    tree = ElementTree()
    try:
        tree.parse('db.xml')
    except ET.ParseError:
        return 'Database empty\n'
    root = tree.getroot()

    #Adding all topic names to list so we can check if the topic already exists
    for topic in root:
        topicList.append(topic.attrib['name']) 
    
    if searchTopic in topicList:
        index = topicList.index(searchTopic)
        topicRoot = root.findall('topic')[index]

        ET.indent(topicRoot, space='\t',level=0)
        topicString = ET.tostring(topicRoot,encoding='utf8')
        return topicString
    else:
        return 'No topic found\n'


server = SimpleXMLRPCServer(('localhost',3000))
server.register_introspection_functions()

server.register_function(addNote,'addnote')
server.register_function(printTopic,'printTopic')
server.serve_forever()