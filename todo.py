#!python3
# todo.py
# store todo items in a SQL database

import dataset
import tkinter
# connect to the todo database
db = dataset.connect('sqlite:///todo.db')

# define the var items as our table
items = db.create_table('items', primary_id='id', primary_type='Integer')
items = db['items']
listUpdated = False

# DEBUGGING FUNCS
def dropRefresh():
    items.drop()
    items = db.create_table('items', primary_id='id', primary_type='Integer')

# print all items in the table
def debugPrint():
    for item in db['items']:
        print(item['id'], item['node'], sep='. ')

# delete all nodes in table
def deleteAll():
    items.delete()

# insert a new item into our table
def newItem(item):
    items.insert(dict(node=item))


# remove an item from our table
def removeItem(identifier):
    items.delete(id=identifier)

class Todo(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Todo")

        self.todoList = tkinter.Listbox()
        #self.todoList('<<ListboxSelect', self.deleteFromList())
        self.todoList.pack(fill=tkinter.BOTH, expand=0)

        # entry box & button for new todo items
        self.entry = tkinter.Entry()
        self.entry.pack(fill=tkinter.BOTH, expand=0)

        entryButton = tkinter.Button(text="Enter", command=self.addToList)
        entryButton.pack(fill=tkinter.BOTH, expand=0)

        # delete items box & button
        self.deleteOption = tkinter.Entry()
        self.deleteOption.pack(fill=tkinter.BOTH, expand=0)

        deleteButton = tkinter.Button(text="Delete", command=self.deleteFromList)
        deleteButton.pack(fill=tkinter.BOTH, expand=0)

        # update the application on startup with items already
        # in the database
        for items in db['items']:
            item = str(items['id']) + ". " + str(items['node'])
            self.todoList.insert(tkinter.END, str(item))
            self.todoList.update_idletasks()

    def addToList(self):
        # add an item to the database
        newItem(str(self.entry.get()))
        # delete all entries in the list todoList
        self.todoList.delete(0, tkinter.END)
        # update the list
        self.todoList.update_idletasks()
        # delete the text in the box
        self.entry.delete(0, 'end')
        # get all the items back again, refreshing them all
        for items in db['items']:
            item = str(items['id']) + ". " + str(items['node'])
            self.todoList.insert(tkinter.END, str(item))
            self.todoList.update_idletasks()
        debugPrint()

    def deleteFromList(self):
        # deletes an item from the datavase
        removeItem(int(self.deleteOption.get()))
        # deletes everything from the list
        self.todoList.delete(0, tkinter.END)
        # update the list
        self.todoList.update_idletasks()
        # clear the deleteOption entry box
        self.deleteOption.delete(0, 'end')
        # refresh the list by getting them all from the database
        for items in db['items']:
            item = str(items['id']) + ". " + str(items['node'])
            self.todoList.insert(tkinter.END, str(item))
            self.todoList.update_idletasks()
        debugPrint()

if __name__ == "__main__":
    application = Todo()
    application.mainloop()
