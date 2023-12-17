import fitz
import re
import os
import random
from question_extractor import QuestionExtractor
import dotenv

# Load env

dotenv.load_dotenv()

exprs = os.environ.get("EXPRS").split(';')


# Get inputs and files

fexpr= "^[^+]+\.pdf$"

qname = input("Enter question sheet filepath: ")

if (not os.path.exists(qname) or re.match(fexpr, qname) == None):
    raise Exception("Invalid file path")

sname = input("Enter solution sheet filepath: ")

if (not os.path.exists(sname) or re.match(fexpr, sname) == None):
    raise Exception("Invalid file path")

qs = fitz.open(qname)
sol = fitz.open(sname)

course = input("Which course is this for: ")

week_no = input("Enter the week number: ")

if (not week_no.isnumeric()):
    raise Exception("Invalid week number")

week_no = int(week_no)

# Create directory

root_dir = "data"
course_dir = f"{root_dir}/{course}"
week_dir = f"{course_dir}/week{week_no}"

if (not os.path.isdir(root_dir)):
    os.mkdir(root_dir)
if (not os.path.isdir(course_dir)):
    os.mkdir(course_dir)
if (not os.path.isdir(week_dir)):
    os.mkdir(week_dir)

# Extract images

qe = QuestionExtractor()
qe.extract(f"{week_dir}/q", qs, exprs)
qe.extract(f"{week_dir}/s", sol, exprs)