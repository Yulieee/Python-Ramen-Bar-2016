from tkinter import *
from dialogue_manager import parse_sentence, respond, order

class App(Frame):
    
    def __init__(self, master=None):
        
        Frame.__init__(self, master)
        self.master.title("Welcome to the Python Ramen Bar!")
        self.master.minsize(1000, 500)
        self.grid(row = 0)
        self.columnconfigure(1, weight = 1)
        
        self.response = Label(text = "Can I help who's next?")
        self.response.grid(row = 0, column = 0, columnspan = 2, sticky = W+E)
        
        self.sentence_entry = Entry()
        self.sentence_entry.grid(row = 1, column = 0, columnspan = 2, sticky = W+E)
        
        self.menu_image = PhotoImage(file = 'Menu.png')
        self.menu_image_label = Label(image = self.menu_image)
        self.menu_image_label.grid(row = 2, column = 1)
        
        self.order_label = Label(text = 'Nothing ordered yet.')
        self.order_label.grid(row = 2, column = 0, sticky = W+E+N+S)
        
        # This variable holds the sentence that the user typed in.
        self.sentence = StringVar()
        # It's bound to the text displayed in the entry field in the GUI.
        self.sentence_entry['textvariable'] = self.sentence
        
        # When the user hits return, parse the sentence and print the results.
        self.sentence_entry.bind('<Key-Return>', self.manage_sentence)
        
#        print()
#        log_file = open('uuscil_log.txt', 'a')
#        log_file.write('------------------------\n')
#        log_file.close()

    def manage_sentence(self, event):
        user_sentence = self.sentence.get()
        parse_result = parse_sentence(user_sentence)
        self.response['text'] = respond(user_sentence, parse_result)
        order_string = 'Order:\n' + str(order)
        order_string += '\n\nTotal: ${:.2f}'.format(order.price())
        self.order_label['text'] = order_string
        self.sentence.set('')
        print()

root = Tk()
root.columnconfigure(index = 0, weight = 1)
app = App(master = root)
app.mainloop()
root.destroy()
