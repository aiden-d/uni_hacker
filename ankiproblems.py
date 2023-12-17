import fitz
import re
import os
import random
from question_extractor import QuestionExtractor
import dotenv

# Read and validate inputs
dotenv.load_dotenv()

fexpr= "^[^+]+\.pdf$"

qname = input("Enter question sheet filepath: ")

if (not os.path.exists(qname) or re.match(fexpr, qname) == None):
    raise Exception("Invalid file path")

sname = input("Enter solution sheet filepath: ")

if (not os.path.exists(sname) or re.match(fexpr, sname) == None):
    raise Exception("Invalid file path")

out = input("Enter anki filename prefix: ")

# Expressions for matching questions / solution

exprs = os.environ.get("EXPRS").split(';')

# The last question number on the sheet
max_question_num = 0


# Extract data from the pdf and generate images

# Create the anki file and clean up images
def gen_anki(q_prefix, s_prefix):
    global out
    print(f"Generating anki file...")
    my_model = genanki.Model(
    100000000,
    'Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'QMedia'},
        {'name': 'AMedia'},                                    # ADD THIS
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': '{{Question}}<br>{{QMedia}}',              # AND THIS
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}<br>{{AMedia}}',
        },
    ])

    my_deck = genanki.Deck(
        random.randint(100000000, 999999999),
        out)
    

    media = []
    for i in range(1, max_question_num + 1):
        q_img = ""
        s_img = ""
        if (os.path.exists(f"{q_prefix}_{i}.png")):
            media.append(f"{q_prefix}_{i}.png")
            q_img = f"<img src=\"{q_prefix}_{i}.png\">"
        elif (os.path.exists(f"{q_prefix}_{i}_1.png") and os.path.exists(f"{q_prefix}_{i}_2.png")):
            media.append(f"{q_prefix}_{i}_1.png")
            media.append(f"{q_prefix}_{i}_2.png")
            q_img = f"<img src=\"{q_prefix}_{i}_1.png\"><br><img src=\"{q_prefix}_{i}_2.png\">"

        if (os.path.exists(f"{s_prefix}_{i}.png")):
            media.append(f"{s_prefix}_{i}.png")
            s_img = f"<img src=\"{s_prefix}_{i}.png\">"
        elif (os.path.exists(f"{s_prefix}_{i}_1.png") and os.path.exists(f"{s_prefix}_{i}_2.png")):
            media.append(f"{s_prefix}_{i}_1.png")
            media.append(f"{s_prefix}_{i}_2.png")
            s_img = f"<img src=\"{s_prefix}_{i}_1.png\"><br><img src=\"{s_prefix}_{i}_2.png\">"

        my_note = genanki.Note(model=my_model, fields=[f'Question {i}', f'Answer {i}', q_img, s_img])
        my_deck.add_note(my_note)
    
    my_package = genanki.Package(my_deck)
    my_package.media_files = media
    my_package.write_to_file(f'{out}.apkg')
    print(f'File written: {out}.apkg')
    print(f'Cleaning up...')
    # Clean up
    for f in media:
        os.remove(f)



qe = QuestionExtractor()
qs = fitz.open(qname)

qe.extract("question", qs, exprs)

sol = fitz.open(sname)
qe.extract("solution", sol, exprs)

gen_anki("question", "solution")
print("Done.")


            
