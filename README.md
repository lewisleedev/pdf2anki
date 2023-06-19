# pdf2anki

Ever wanted to handwrite your own deck for anki?

pdf2anki is a Python program that converts PDF files to Anki decks. **The program cuts each pages in a pdf file in half for handwritten questions and answers.** The program uses the following libraries:

- pdf2image to convert PDF pages to images
- genanki to create Anki decks
- Tkinter to create the graphical user interface (GUI)

*Note: The program requires Poppler to be installed on your system in order to work. It was tested with poppler-0.68.0.*

## How to use
- Install Poppler on your system by following the instructions for your operating system.
- Use the GUI. Note that it may take significant time to convert large pdf files (even more than few minutes!)

## How it works
- Select the PDF file you want to convert using the "Browse" button.
- Select the path you want your .apkg file to be.
- Choose a name for your Anki deck and enter it into the "Deck name" field.
- Select the path for poppler binary. (...poppler-x.xx.x/bin/)
- Click the "Convert" button to start the conversion process.
- Once the conversion is complete, the program will generate an Anki deck file with the same name as your deck, which you can import into Anki.

Inside the template folder there's an example template pdf file I made for question/answer. It was made with Powerpoint in like 3 min. **Note that any pdf files will work the same and you can create your own pdf template as you wish.** Just make sure that top side will be the question size and the bottom side will be the answer side and that they are the same height.

## Limitation
This is nowhere near a perfect solution. I simply wrote this for my personal use as I study. I can only say for sure that it works for me. 

## Credits
pdf2anki was created by [@lewisleedev](https://github.com/lewisleedev/) using the following libraries:

 - pdf2image
 - genanki
 - Tkinter

The GUI part of the program was 100% written by ChatGPT, and I understand that it may not be the best code out there. I apologize for any inconvenience or frustration it may cause, and I encourage anyone who is interested in contributing to the project to improve the GUI code as well.
