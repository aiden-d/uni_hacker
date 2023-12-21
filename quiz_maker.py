import img2pdf
import os
import re
import random
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
courses = os.listdir("data")
question_images = {}
solution_images = {}

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
    weeks = sorted(os.listdir(f"data/{course}"))
    for week in weeks:
        if (week == ".DS_Store"):
            continue
        path = f"data/{course}/{week}"
        files = sorted( os.listdir(path), key=get_number)
        # Get a valid question
        qs = []
        ss = []
        #print(files)
        nums = []
        times = 1
        if (course == "ca"):
            times = 5
        while times >= 1:
            max_num = max(map(get_number, files))
            min_num = min(map(get_number, files))
            num = random.randint(min_num, max_num)
            if (num in nums):
                num = random.randint(min_num, max_num)
            nums.append(num)
            qe = f"q_{num}(_|.)"
            se = f"s_{num}(_|.)"
            qs = list(filter(lambda f: re.match(qe, f), files))
            print(qs)
            ss = list(filter(lambda f: re.match(se, f), files))
            if (course not in question_images):
                question_images[course] = []
            if (course not in solution_images):
                solution_images[course] = []
            question_images[course] += [f"{path}/{q}" for q in qs]
            solution_images[course] += [f"{path}/{s}" for s in ss]
            times -= 1

def draw_text(c, text, page_width, y, margin, font_size, is_center):
    # Set title font and size
    title_font = "Helvetica"
    title_size = font_size  # Example size, adjust as needed
    title_text = text

    # Calculate the width of the title text
    title_width = c.stringWidth(title_text, title_font, title_size)

    # Set the title position (centered)
    title_x = (page_width - title_width) / 2
    title_y = y - margin - title_size
    if (not is_center):
        title_x = margin
        title_y = y - margin - title_size

    # Add the title to the first page
    c.setFont(title_font, title_size)
    c.drawString(title_x, title_y, title_text)

    return title_y

def create_pdf(image_map, output_pdf):
    # A4 dimensions and margin
    page_width, page_height = A4
    margin = 0.2 * inch

    # Create a canvas for PDF generation
    c = canvas.Canvas(output_pdf, pagesize=A4)
    
    y = page_height - margin

    # Adjust the starting y-coordinate for images
    y = draw_text(c, "Quiz", page_width, y, margin, 18, True) - margin

    # Process each image in the folder
    for course in image_map:
        images = image_map[course]
        y = draw_text(c, course.upper(), page_width, y, margin, 14, True) - margin
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
        

        
        
        
        
        
