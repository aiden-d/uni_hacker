import img2pdf
import os
import re
import random
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
courses = os.listdir("data")
question_images = []
solution_images = []

def get_number(s):
    num = ""
    flag = False
    count = 0
    for c in s:
        if (c == "_" or c == "."):
            flag = not flag
            count += 1
            if (count == 2):
                break
        elif (flag):
            num += c
    return int(num)

for course in courses:
    if (course == ".DS_Store"):
        continue
    weeks = os.listdir(f"data/{course}")
    for week in weeks:
        if (week == ".DS_Store"):
            continue
        path = f"data/{course}/{week}"
        files = os.listdir(path)
        # Get a valid question
        qs = []
        ss = []
        #print(files)
        
        max_num = max(map(get_number, files))
        min_num = min(map(get_number, files))
        num = random.randint(min_num, max_num)
        qe = f"q_{num}(_|.)"
        se = f"s_{num}(_|.)"
        qs = list(filter(lambda f: re.match(qe, f), files))
        ss = list(filter(lambda f: re.match(se, f), files))
        question_images += [f"{path}/{q}" for q in qs]
        solution_images += [f"{path}/{s}" for s in ss]

def create_pdf(images, output_pdf):
    # A4 dimensions and margin
    page_width, page_height = A4
    margin = 0.2 * inch

    # Create a canvas for PDF generation
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    y = page_height - margin

    # Set title font and size
    title_font = "Helvetica-Bold"
    title_size = 18  # Example size, adjust as needed
    title_text = "Quiz"

    # Calculate the width of the title text
    title_width = c.stringWidth(title_text, title_font, title_size)

    # Set the title position (centered)
    title_x = (page_width - title_width) / 2
    title_y = page_height - margin - title_size

    # Add the title to the first page
    c.setFont(title_font, title_size)
    c.drawString(title_x, title_y, title_text)

    # Adjust the starting y-coordinate for images
    y = title_y - margin

    # Process each image in the folder
    for image_file in images:
        img = Image.open(image_file)

        # Calculate the new height to maintain the aspect ratio
        aspect_ratio = img.height / img.width
        new_width = page_width - 2 * margin
        new_height = new_width * aspect_ratio

        # Adjust y-coordinate and check if a new page is needed
        y -= new_height
        if y < margin:
            c.showPage()
            y = page_height - margin - new_height

            # Reset the y-coordinate below the title for subsequent pages
            # Remove this block if you want the title on every page
            # if c.getPageNumber() > 1:
            #     y += title_size + margin

        # Draw the image on the canvas
        c.drawImage(image_file, margin, y, width=new_width, height=new_height, preserveAspectRatio=True)

        # Update y-coordinate for the next image
        y -= margin

    # Save the PDF
    c.save()

create_pdf(question_images, "quiz_q.pdf")
create_pdf(solution_images, "quiz_s.pdf")
        

        
        
        
        
        
