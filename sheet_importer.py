import fitz
import re
import os
import random
from question_extractor import QuestionExtractor
import dotenv

# Load env

dotenv.load_dotenv()

exprs = os.environ.get("EXPRS").split(';')

# Init folder
root_dir = "data"
if (not os.path.isdir(root_dir)):
    os.mkdir(root_dir)

# Get inputs files

if (not os.path.exists("input")):
    raise Exception("Input folder non-existent")

inputs = os.listdir("input")
expr = "^[A-Za-z]+_[0-9]+_(q|s).pdf"
inputs = list(filter(lambda f: re.match(expr, f), inputs))

q_inputs = list(filter(lambda f: f.endswith("q.pdf"), inputs))
s_inputs = list(filter(lambda f: f.endswith("s.pdf"), inputs))
print(inputs)
qe = QuestionExtractor()

def process_input(fi, prefix):
    md = fi.split("_")
    course = md[0]
    week_no = int(md[1])
    course_dir = f"{root_dir}/{course}"
    week_dir = f"{course_dir}/week{week_no}"
    if (not os.path.isdir(course_dir)):
        os.mkdir(course_dir)
    if (not os.path.isdir(week_dir)):
        os.mkdir(week_dir)

    input_dir = f"input/{fi}"
    f = fitz.open(input_dir)
    qe.extract(f"{week_dir}/{prefix}", f, exprs)


for q in q_inputs:
    process_input(q, "q")

for s in s_inputs:
    process_input(s, "s")