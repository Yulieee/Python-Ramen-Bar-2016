from tkinter import *
from dialogue_manager import parse_sentence, respond, order

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
        self.menu_image_label.grid(row = 2, column = 1)

        # for the list of order
        self.order_label = Label(text = 'Nothing ordered yet.', bg="bisque1")
        self.order_label.grid(row = 2, column = 0, sticky = W+E+N+S)
            
        # This variable holds the sentence that the user typed in.
        self.sentence = StringVar()
        # It's bound to the text displayed in the entry field in the GUI.
        self.sentence_entry['textvariable'] = self.sentence
        
        # When the user hits return, parse the sentence and print the results.
        self.sentence_entry.bind('<Key-Return>', self.manage_sentence)

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
cuter = font.Font(family="Kristen ITC",size=12,weight="normal")
root.option_add("*Font", cuter)
root.columnconfigure(index = 0, weight = 1)
app = App(master = root)
app.mainloop()
root.destroy()
