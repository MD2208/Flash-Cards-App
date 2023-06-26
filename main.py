import tkinter
import random
import pandas
BACKGROUND_COLOR = "#B1DDC6"
current_pair={}
word_pairs={}
#---------------- Read File ---------------#
#Catch the error if user using the app for the first time 
#then collect to data from original document.
try:
    data = pandas.read_csv('data/polish-english-to-learn.csv')
except FileNotFoundError:
    data = pandas.read_csv('data/polish-english-original.csv')
    # Convert dataframe to list of dict by keeping key as a column name value as row respectively 
    word_pairs = data.to_dict(orient='records')
else:
    word_pairs = data.to_dict(orient='records')
#--------------- Get Pair From Data ----------#

def get_random_pair():
    global current_pair, translate_timer
    my_window.after_cancel(translate_timer)
    current_pair = random.choice(word_pairs)
    canvas.itemconfig(card_title, text="Polish", fill="black")
    canvas.itemconfig(card_word, text=current_pair['Polish'], fill="black")
    canvas.itemconfig(canvas_img, image=card_front_img)
    translate_timer = my_window.after(3000,translate_card)
#--------- Remove The Known Words From Data -----#
def known_card():
    global current_pair
    word_pairs.remove(current_pair)
    updated_data = pandas.DataFrame(word_pairs)
    updated_data.to_csv("data/polish-english-to-learn.csv",index=False)
    get_random_pair()
#------- Go to next card by keeping unknown words inside data ------- #
def unknown_card():
    get_random_pair()
#--------------- Show Translate ---------------#
def translate_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_pair['English'], fill="white")
    canvas.itemconfig(canvas_img, image=card_back_img)

#---------------- UI -------------------#
my_window = tkinter.Tk()
my_window.config(bg=BACKGROUND_COLOR,padx=50,pady=50)
my_window.title("Flashy")

translate_timer = my_window.after(3000,translate_card)

canvas = tkinter.Canvas(width=800,height=526,bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = tkinter.PhotoImage(file="images/card_front.png")
card_back_img = tkinter.PhotoImage(file="images/card_back.png")
canvas_img = canvas.create_image(400,263,image=card_front_img)
card_title = canvas.create_text(400,150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Ariel",60, "bold"))

canvas.grid(column=0,row=0,columnspan=2)


cross_image = tkinter.PhotoImage(file="images/wrong.png")
right_image = tkinter.PhotoImage(file="images/right.png")

cross_btn = tkinter.Button(image=cross_image, highlightthickness=0, width=100, height=100, command=unknown_card)
cross_btn.grid(column=0,row=1)
right_btn = tkinter.Button(image=right_image, highlightthickness=0, width=100, height=100, command=known_card)
right_btn.grid(column=1,row=1)

get_random_pair()


my_window.mainloop()
