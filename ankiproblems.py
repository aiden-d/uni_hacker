import fitz
import re
import genanki
import os
import random

# Read and validate inputs

fexpr= "^[^+]+\.pdf$"

qname = input("Enter question sheet filepath: ")

if (not os.path.exists(qname) or re.match(fexpr, qname) == None):
    raise Exception("Invalid file path")

sname = input("Enter solution sheet filepath: ")

if (not os.path.exists(sname) or re.match(fexpr, sname) == None):
    raise Exception("Invalid file path")

out = input("Enter anki filename prefix: ")

# Expressions for matching questions / solution
exprs = ["^[ ]*[*]+[ ]*[0-9]+[.][ ]*([\\][n]|[\n])", "^[ ]*([Q]|[S])+[ ]*[0-9]+[.][ ]*([\\][n]|[\n])"]

# The last question number on the sheet
max_question_num = 0

# Check if a given string is an integer
def is_integer(a):
    try:
        int(a)
        return True
    except ValueError:
        return False

# Get the irect clip for generating an image
def get_clip(bound, cloc, nloc):
    (cx_0, cy_0, cx_1, cy_1) = cloc
    (nx_0, ny_0, nx_1, ny_1) =  nloc
    x_0 = bound.x0
    x_1 =  bound.x1
    y_0 =  round(cy_0)
    y_1 =  round(ny_0)
    return fitz.IRect(x_0, y_0, x_1, y_1)

# Extract data from the pdf and generate images
def extract(prefix, doc):
    global exprs
    question_md = {} # number : (page , (x0, y0, x1, y1))

    global max_question_num

    print(f"Generating {prefix} metadata...")

    for page_no, page in enumerate(doc):
        output = page.get_text("blocks")
        for block in output:
            (x0, y0, x1, y1, words, _, _) = block
            match = None
            for e in exprs:
                m = re.match(e, words)
                if (m != None):
                    match = m
                    break
            if (match):
                w = m.group()
                n = []
                for c in w:
                    if is_integer(c):
                        n.append(c)
                if (n):
                    num = int(''.join(n))
                    question_md[num] = (page_no, (x0, y0, x1, y1))
                    max_question_num = num
    
    print(f"Generating {prefix} images...")
    for i in range(max_question_num + 1):
        if i in question_md:
            (page_no, (x0, y0, x1, y1)) = question_md[i]
            page = doc.load_page(page_no)
            clip = None
            bound = page.bound()
            # Case 1: Last question
            if (i == max_question_num):
                clip = get_clip(bound, (x0, y0, x1, y1), (bound.x0, bound.y1, bound.x1, bound.y1))
            # Case 2: Bth on same page
            elif (page_no == question_md[i+1][0]):
                clip = get_clip(bound, (x0, y0, x1, y1), question_md[i+1][1])
            # Case 3: On next page
            else:
                clip1 = get_clip(bound, (x0, y0, x1, y1), (bound.x0, bound.y1, bound.x1, bound.y1))
                clip2 = get_clip(bound, (bound.x0, bound.y0, bound.x1, bound.y1), question_md[i+1][1])
                pix = page.get_pixmap(dpi=300, clip=clip1)
                output = prefix + "_" + str(i) + "_1" + ".png"
                pix.save(output)
                page = doc.load_page(page_no + 1)
                pix = page.get_pixmap(dpi=300, clip=clip2)
                output = prefix + "_" + str(i) + "_2" + ".png"
                pix.save(output)
            if (clip):
                pix = page.get_pixmap(dpi=300, clip=clip)
                output = prefix + "_" + str(i) + ".png"
                pix.save(output)

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


qs = fitz.open(qname)
extract("question", qs)
sol = fitz.open(sname)
extract("solution", sol)
gen_anki("question", "solution")
print("Done.")


            
