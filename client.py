import xmlrpc.client

# Set up the client
proxy = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")


# Ask the user for input
topic = input("Enter topic: ")
text = input("Enter note text: ")

# Call the "add_note" function on the server
response = proxy.add_note(topic, text)
print(response)

# Call the "get_notes" function on the server
notes = proxy.get_notes(topic)
if isinstance(notes, str):
    print(notes)
else:
    print(f"Notes for topic '{topic}':")
    for note in notes:
        print(f"{note[0]} ({note[1]})")
