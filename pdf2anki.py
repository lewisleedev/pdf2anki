import pdf2image, genanki, os, sys, shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

"""
            _  __ ___             _    _ 
           | |/ _|__ \           | |  (_)
  _ __   __| | |_   ) |__ _ _ __ | | ___ 
 | '_ \ / _` |  _| / // _` | '_ \| |/ / |
 | |_) | (_| | |  / /| (_| | | | |   <| |
 | .__/ \__,_|_| |____\__,_|_| |_|_|\_\_|
 | |                                     
 |_|                                     

 by @lewisleedev

 I want to leave a quick note to let you know that I won't be maintaining this code beyond its current state.
 As much as I would like to continue improving and updating it, I simply don't have the time to spare. 
 Feel free to use and modify the code as you see fit, but please keep in mind that I won't be available to provide support or make any further changes.

I understand that the GUI part is poorly written. GUI part is 100% written by ChatGPT. I apologize for any inconvenience or frustration it may cause.

 > The hacky code may not be pretty,
 > But it does the job, it's quite witty,
 > Thanks to ChatGPT's helpful hand,
 > pdf2anki now can be grand.

"""


def pdf2anki(original_file: str, deck_name: str, out_file: str, poppler_path: str):
    try:
        pages = pdf2image.convert_from_path(
            original_file, poppler_path=poppler_path
        )
    except:
        raise

    num_pages = len(pages)

    if getattr(sys, "frozen", False):
        temp_dir = os.path.join(sys._MEIPASS, "temp")
    else:
        temp_dir = "temp"

    os.makedirs(temp_dir, exist_ok=True)

    # Write the .apkg file to the temporary directory
    file_path = os.path.join(temp_dir, f"{deck_name}.apkg")

    for idx, page in enumerate(pages):
        page.save(os.path.join(temp_dir, "page" + str(idx) + ".jpg"), "JPEG")

    for page in range(num_pages):
        im = Image.open(os.path.join(temp_dir, r"page" + str(page) + ".jpg"))
        width, height = im.size

        left = 0
        top = 0
        right = width
        bottom = height / 2

        im1 = im.crop((left, top, right, bottom))
        im1 = im1.save(
            os.path.join(temp_dir, deck_name + "-page" + str(page) + "-question.jpg")
        )

        im2 = im.crop((left, height / 2, right, height - 30))
        im2 = im2.save(
            os.path.join(temp_dir, deck_name + "-page" + str(page) + "-answer.jpg")
        )

    for page in range(num_pages):
        os.remove(os.path.join(temp_dir, "page" + str(page) + ".jpg"))

    the_model = genanki.Model(
        1902690281,
        "pdf2anki Model",
        fields=[{"name": "QuestionMedia"}, {"name": "AnswerMedia"}],
        templates=[
            {
                "name": "Card1",
                "qfmt": "{{QuestionMedia}}<br>",
                "afmt": '{{FrontSide}}<hr id="answer">{{AnswerMedia}}',
            }
        ],
    )

    the_deck = genanki.Deck(1564947522, deck_name)

    media_list = []

    for page in range(num_pages):
        my_note = genanki.Note(
            model=the_model,
            fields=[
                f'<img src="{deck_name}-page{str(page)}-question.jpg" />',
                f'<img src="{deck_name}-page{str(page)}-answer.jpg" />',
            ],
        )
        the_deck.add_note(my_note)

    for page in range(num_pages):
        media_list.append(
            os.path.join(temp_dir, deck_name + "-page" + str(page) + "-question.jpg")
        )
        print(temp_dir + deck_name + "-page" + str(page) + "-question.jpg")
        media_list.append(
            os.path.join(temp_dir, deck_name + "-page" + str(page) + "-answer.jpg")
        )

    my_package = genanki.Package(the_deck)
    my_package.media_files = media_list
    my_package.write_to_file(file_path)

    print("Successfully converted to" + file_path)

    desktop_path = out_file

    shutil.copyfile(file_path, os.path.join(desktop_path, f"{deck_name}.apkg"))

    # print("copied to " + desktop_path)


def choose_file():
    file_path = filedialog.askopenfilename()
    original_file_entry.delete(0, tk.END)
    original_file_entry.insert(0, file_path)

def choose_poppler():
    file_path = filedialog.askdirectory(initialdir = "C:/Program Files/")
    poppler_entry.delete(0, tk.END)
    poppler_entry.insert(0, file_path)

def choose_outfile():
    file_path = filedialog.askdirectory()
    out_file_entry.delete(0, tk.END)
    out_file_entry.insert(0, file_path)


def convert():
    original_file = original_file_entry.get()
    out_file = out_file_entry.get()
    deck_name = deck_name_entry.get()
    poppler_dir = poppler_entry.get()
    pdf2anki(original_file, deck_name, out_file, poppler_dir)
    messagebox.showinfo("Success!", "Conversion complete!")


# Only GUI is mostly written by ChatGPT.

# Create the main window
root = tk.Tk()
root.title("PDF to Anki Converter")
root.geometry("800x500")
root.config(bg="#F5F5F5")
# root.withdraw()

# Create the header and subtitle labels
header_label = tk.Label(
    root,
    text="pdf2anki",
    font=("Arial", 24),
    fg="#FFFFFF",
    bg="#3F51B5",
    pady=10,
)
header_label.pack(fill="x")

subtitle_label = tk.Label(
    root,
    text="Convert a PDF document to an Anki deck with image-based flashcards.",
    font=("Arial", 12),
    bg="#F5F5F5",
    pady=10,
)
subtitle_label.pack()

# Create the file selection widgets
file_frame = tk.Frame(root, bg="#F5F5F5", padx=10, pady=10)
file_frame.pack(fill="x")

outfile_frame = tk.Frame(root, bg="#F5F5F5", padx=10, pady=10)
outfile_frame.pack(fill="x")

original_file_label = tk.Label(
    file_frame, text="Select PDF file:", font=("Arial", 12), bg="#F5F5F5"
)
original_file_label.pack(side="left")

original_file_entry = tk.Entry(file_frame, font=("Arial", 12), width=30)
original_file_entry.pack(side="left", padx=10)

choose_file_button = tk.Button(
    file_frame,
    text="Choose",
    font=("Arial", 12),
    bg="#3F51B5",
    fg="#FFFFFF",
    command=choose_file,
)
choose_file_button.pack(side="left")

# Create the deck name entry widget
name_frame = tk.Frame(root, bg="#F5F5F5", padx=10, pady=10)
name_frame.pack(fill="x")

deck_name_label = tk.Label(
    name_frame, text="Enter deck name:", font=("Arial", 12), bg="#F5F5F5"
)
deck_name_label.pack(side="left")

deck_name_entry = tk.Entry(name_frame, font=("Arial", 12), width=30)
deck_name_entry.pack(side="left", padx=10)

out_file_label = tk.Label(
    outfile_frame, text="Output Folder:", font=("Arial", 12), bg="#F5F5F5"
)
out_file_label.pack(side="left")

out_file_entry = tk.Entry(outfile_frame, font=("Arial", 12), width=30)
out_file_entry.pack(side="left", padx=10)

# "C:/Program Files/poppler-0.68.0/bin/"

about_label = tk.Label(root, text="By @lewisleedev", font=("Arial", 9), bg="#F5F5F5")
about_label.pack(side="bottom")

choose_outfile_button = tk.Button(
    outfile_frame,
    text="Choose",
    font=("Arial", 12),
    bg="#3F51B5",
    fg="#FFFFFF",
    command=choose_outfile,
)

choose_outfile_button.pack(side="left")

poppler_frame = tk.Frame(root, bg="#F5F5F5", padx=10, pady=10)
poppler_frame.pack(fill="x")

poppler_label = tk.Label(
    poppler_frame, text="Poppler path:", font=("Arial", 12), bg="#F5F5F5"
)
poppler_label.pack(side="left")

poppler_entry = tk.Entry(poppler_frame, font=("Arial", 12), width=30)
poppler_entry.pack(side="left", padx=10)
poppler_entry.insert(0, "C:/Program Files/poppler-0.68.0/bin/")

choose_poppler_button = tk.Button(
    poppler_frame,
    text="Choose",
    font=("Arial", 12),
    bg="#3F51B5",
    fg="#FFFFFF",
    command=choose_poppler,
)

choose_poppler_button.pack(side="left")

# Create the convert button
button_frame = tk.Frame(root, bg="#F5F5F5", padx=10, pady=10)
button_frame.pack(fill="x")

convert_button = tk.Button(
    button_frame,
    text="Convert",
    font=("Arial", 12),
    bg="#3F51B5",
    fg="#FFFFFF",
    command=convert,
)
convert_button.pack()

# Start the GUI loop

if __name__ == '__main__':
    root.mainloop()
