
import fitz
import re

class QuestionExtractor:

    # Check if a given string is an integer
    def is_integer(self, a):
        try:
            int(a)
            return True
        except ValueError:
            return False

    # Get the irect clip for generating an image
    def get_clip(self, bound, cloc, nloc):
        (cx_0, cy_0, cx_1, cy_1) = cloc
        (nx_0, ny_0, nx_1, ny_1) =  nloc
        x_0 = bound.x0
        x_1 =  bound.x1
        y_0 =  round(cy_0)
        y_1 =  round(ny_0)
        return fitz.IRect(x_0, y_0, x_1, y_1)

    
    def extract(self, prefix, doc, exprs):
        question_md = {} # number : (page , (x0, y0, x1, y1))

        max_question_num = None
        min_question_num = None

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
                        if self.is_integer(c):
                            n.append(c)
                    if (n):
                        num = int(''.join(n))
                        if (num in question_md):
                            continue
                        if (min_question_num == None or num < min_question_num):
                            min_question_num = num
                        if (max_question_num == None or num > max_question_num):
                            max_question_num = num
                        question_md[num] = (page_no, (x0, y0, x1, y1))
                        max_question_num = num
        
        print(f"Generating {prefix} images...")
        for i in range(min_question_num, max_question_num + 1):
            if i in question_md:
                (page_no, (x0, y0, x1, y1)) = question_md[i]
                page = doc.load_page(page_no)
                clip = None
                bound = page.bound()
                # Case 1: Last question
                if (i == max_question_num):
                    clip = self.get_clip(bound, (x0, y0, x1, y1), (bound.x0, bound.y1, bound.x1, bound.y1))
                elif (i+1 not in question_md):
                    print(f"Error: Question {i+1} not found for question {i}")
                    break
                # Case 2: Bth on same page
                elif (page_no == question_md[i+1][0]):
                    clip = self.get_clip(bound, (x0, y0, x1, y1), question_md[i+1][1])
                # Case 3: On next page
                else:
                    clip1 = self.get_clip(bound, (x0, y0, x1, y1), (bound.x0, bound.y1, bound.x1, bound.y1))
                    clip2 = self.get_clip(bound, (bound.x0, bound.y0, bound.x1, bound.y1), question_md[i+1][1])
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
