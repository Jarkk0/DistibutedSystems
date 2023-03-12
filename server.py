from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import datetime

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    # Mock database implementation
    root = ET.Element('notes')
    tree = ET.ElementTree(root)
    tree.write('notes.xml')
    root = tree.getroot()

    def print_topics():
        tree = ET.parse('notes.xml')
        root = tree.getroot()

        topics = set()
        for elem in root.findall('note'):
            topic = elem.find('topic').text
            if topic:
                topics.add(topic)

        print("Available topics:")
        for topic in topics:
            print(topic)

    # Implement the "add_note" function
    def add_note(topic, text):
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if the topic exists in the database
        found = False
        for elem in root.findall('note'):
            if elem.find('topic').text == topic:
                found = True
                # Add the new note to the existing topic
                note_elem = ET.SubElement(elem, 'note')
                ET.SubElement(note_elem, 'text').text = text
                ET.SubElement(note_elem, 'timestamp').text = timestamp
                tree.write('notes.xml')
                return f"Added note to existing topic '{topic}'"

        # If the topic does not exist, add it to the database
        if not found:
            note_elem = ET.SubElement(root, 'note')
            ET.SubElement(note_elem, 'topic').text = topic
            note_elem = ET.SubElement(note_elem, 'note')
            ET.SubElement(note_elem, 'text').text = text
            ET.SubElement(note_elem, 'timestamp').text = timestamp
            tree.write('notes.xml')
            return f"Added new topic '{topic}' with note"

    # Implement the "get_notes" function
    def get_notes(topic):
        notes = []
        for elem in root.findall('note'):
            if elem.find('topic').text == topic:
                for note_elem in elem.findall('note'):
                    text = note_elem.find('text').text
                    timestamp = note_elem.find('timestamp').text
                    notes.append((text, timestamp))
                return notes
        return "No notes found for topic"

    # Register functions with the server
    server.register_function(add_note, 'add_note')
    server.register_function(get_notes, 'get_notes')

    # Run the server
    server.serve_forever()
