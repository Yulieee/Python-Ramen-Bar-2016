from tkinter import *
from dialogue_manager import parse_sentence, respond, order
log_file_name = 'testing_log.txt'

class App(Frame):
   
    def __init__(self, master=None, *pargs):
        
        Frame.__init__(self, master, *pargs)
        self.master.title("Welcome to the Python Ramen Bar!")
        self.master.minsize(1000, 500)
        self.grid(row = 0)
        self.columnconfigure(1, weight = 1)               
        self.response = Label(text = "Can I help who's next?", bg="bisque1")
        self.response.grid(row = 0, column = 0, columnspan = 2, sticky = W+E)

        self.master.configure(bg = 'bisque1')

        # for the entry bar
        self.sentence_entry = Entry(bg="DarkOrange2", justify='center')
        self.sentence_entry.grid(row = 1, column = 0, columnspan = 2, sticky = W+E)

        # for the menu
        #self.menu = PIL.Image.open('menu.gif')

        self.menu_image = PhotoImage(file = 'menu.gif')
        self.menu_copy = self.menu_image.copy().subsample(2)
        
        self.menu_image_label = Label(master, image = self.menu_copy)
        self.menu_image_label.grid(row = 2, column = 1, rowspan=2)

        # for the list of order
        self.order_label = Label(text = 'Nothing ordered yet.', bg="bisque1")
        self.order_label.grid(row = 2, column = 0, sticky = W+E+N+S)

        # button for removing items
        self.delete_button = Button(text = 'Remove last item.', bg="tomato", fg="white")
        self.delete_button.grid(row = 3 , column = 0)
        self.delete_button.bind('<Button-1>',self.delete_item)
            
        # This variable holds the sentence that the user typed in.
        self.sentence = StringVar()

        #text field initial output
        self.sentence.set('(Enter text here)')
        
        # It's bound to the text displayed in the entry field in the GUI.
        self.sentence_entry['textvariable'] = self.sentence

        # clear the text entry when they click on it
        self.sentence_entry.bind('<Button-1>',self.clear_field)
        
        # When the user hits return, parse the sentence and print the results.
        self.sentence_entry.bind('<Key-Return>', self.manage_sentence)

        print()
        log_file = open(log_file_name, 'a')
        log_file.write('------------------------\n')
        log_file.close()

    def clear_field(self,event):
        self.sentence.set('')
        
    def manage_sentence(self, event):
        user_sentence = self.sentence.get()
        log_file = open(log_file_name, 'a')
        log_file.write(user_sentence)
        log_file.write('\n')
        log_file.close()
        parse_result = parse_sentence(user_sentence)
        self.response['text'] = respond(user_sentence, parse_result)
        order_string = 'Order:\n' + str(order)
        order_string += '\n\nTotal: ${:.2f}'.format(order.price())
        self.order_label['text'] = order_string
        self.sentence.set('')
        
    def delete_item(self,event):
        if len(order.items)>0:
            order.items.pop()
            order_string = 'Order:\n' + str(order)
            order_string += '\n\nTotal: ${:.2f}'.format(order.price())
            self.order_label['text'] = order_string
            self.sentence.set('')
                
root = Tk()
cuter = font.Font(family="Comic Sans MS",size=12,weight="normal")
root.option_add("*Font", cuter)
root.columnconfigure(index = 0, weight = 1)
app = App(master = root)
app.mainloop()
root.destroy()
