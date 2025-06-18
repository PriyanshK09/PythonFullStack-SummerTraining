with open("18-6-25/textfiles/example.txt", "r") as file:
    content = file.read()
    print(content)
    
with open("18-6-25/textfiles/example.txt", "w") as file:
    file.write("This is a new line of text.\n")
    file.write("Appending another line.\n")
    
with open("18-6-25/textfiles/example.txt", "a") as file:
    file.write("Appending yet another line.\n")
    file.write("Final line added.\n")
    
with open("18-6-25/textfiles/example.txt", "r") as file:
    content = file.read()
    print("Updated content of the file:")
    print(content)