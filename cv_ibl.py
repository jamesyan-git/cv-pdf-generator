#!/usr/bin/env python
# coding=utf-8

import csv
from pathlib import Path
from pypdf import PdfWriter
from reportlab.pdfgen import canvas

from models import Student
import regex_stuff

"""
generate_student_data expects a CSV with a header row corresponding to the form questions,
and each subsequent row corresponding to individual responses.

PLEASE NOTE: It is important to replace newline characters in the csv before reading in here.
This can be done in many ways in Excel, Libreoffice Calc, and possible Google Sheets,
just look it up if you don't already have your own method, wont be hard but it is necessary.

for LibreOffice
tools > find & replace > more options > check 'regular expression' > search '\n' > replace with empty string
"""

"""
Available fonts:
standardFonts = (
    'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',
    'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique',
    'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic',
    'Symbol','ZapfDingbats')
"""

# In Typography, a point is defined as 1/72 inch.
point = 1
inch = 72
# A4 imperial standards:
PAGEWIDTH = 8.267 * inch
PAGEHEIGHT = 11.692 * inch

# Paths
IMAGES_DIR = Path("images") / "resized"
OUTPUT_DIR = Path("out")
CSV_PATH = Path("student_responses.csv")
LOGO_PATH = Path("fit_logo.png")
OUTPUT_PDF = Path("output_jan_2020.pdf")


def make_resume(student: Student):
    IBL_ID = student.ibl_id  # already zero-padded to 3 digits by Student.__post_init__
    Last_name = student.last_name
    First_name = student.first_name
    Preferred_name = student.preferred_name
    degree = student.degree
    major = student.major
    specialisation = student.specialisation
    ibl_placement_interest = student.ibl_placement_interest
    fav_subjects = student.units_enjoyed
    employment_history = student.employment_history
    career_interests = student.career_interests
    other_interests = student.other_interests
    photo = student.photo

    output_filename = OUTPUT_DIR / "{}_{}.pdf".format(
        str(Last_name).replace(' ', '_'), First_name.replace(' ', '_')
    )

    print(f"Creating: {output_filename}")

    c = canvas.Canvas(str(output_filename), pagesize=(PAGEWIDTH, PAGEHEIGHT))
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)

    student_name = First_name.strip(" ").capitalize() + " " + Last_name.replace("'", "_").strip(" ").capitalize()
    alternative_name = "***"
    if len(Preferred_name) > 1:
        alternative_name = Preferred_name.strip(" ").capitalize() + " " + Last_name.replace("'", "_").strip(" ").capitalize()
    print(student_name)

    try:
        for img_path in IMAGES_DIR.iterdir():
            file_name = img_path.name
            if student_name.lower() in file_name.lower():
                c.drawImage(str(img_path), 1 * inch, 10.8 * inch - 110)
                # break
            elif alternative_name.lower() in file_name.lower():
                print("HELLO ALTERNATIVE NAME")
                c.drawImage(str(img_path), 1 * inch, 10.8 * inch - 110)
                # break
            elif len(First_name.strip().split(' ')) >= 2:
                possible_name_1 = First_name.strip().split(' ')[0] + " " + Last_name
                possible_name_2 = First_name.strip().split(' ')[1] + " " + Last_name
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage(str(img_path), 1 * inch, 10.8 * inch - 110)
            elif len(First_name.strip().split('-')) >= 2:
                possible_name_1 = First_name.strip().split('-')[0] + " " + Last_name
                possible_name_2 = First_name.strip().split('-')[1] + " " + Last_name
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage(str(img_path), 1 * inch, 10.8 * inch - 110)
            elif len(Last_name.strip().split(' ')) >= 2:
                possible_name_1 = First_name + " " + Last_name.strip().split(' ')[0]
                possible_name_2 = First_name + " " + Last_name.strip().split(' ')[1]
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage(str(img_path), 1 * inch, 10.8 * inch - 110)
            elif len(Last_name.strip().split('-')) >= 2:
                possible_name_1 = First_name + " " + Last_name.strip().split('-')[0]
                possible_name_2 = First_name + " " + Last_name.strip().split('-')[1]
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage(str(img_path), 1 * inch, 10.8 * inch - 110)
    except OSError as e:
        print("Error: ", e)

    c.setFont("Helvetica-Bold", 36 * point)

    """
    Write Name
    """
    if Preferred_name == '' or Preferred_name == 'n/a':
        name_string = "{} {}".format(First_name, Last_name.upper())
    else:
        name_string = "{} {}".format(Preferred_name, Last_name.upper())
        First_name = "{} ({})".format(First_name, Preferred_name)

    v = 11 * inch
    # Write Header
    if len(Preferred_name + Last_name) + 4 >= 25:
        print(name_string, "***")
        c.setFont("Helvetica-Bold", 20 * point)
    else:
        c.setFont("Helvetica-Bold", 24 * point)
    c.drawString(1 * inch, v, "CV: {}".format(name_string))
    v = 758

    """
    WRITE STUDENT DETAILS
    """
    spaces_required = [70, 60, 48, 125, 40]
    detail_section = ["First Name: ", "Surname: ", "Degree: "]
    print(degree)

    detail_response = [First_name, Last_name, degree]
    for i, field in enumerate(detail_section):
        c.setFont("Helvetica-Bold", 12 * point)
        line_text = field
        c.drawString(1 * inch + 120, v, line_text)
        c.setFont("Helvetica", 12 * point)
        if detail_response[i] == "Bachelor of Information Technology (Business Information Systems)":
            c.setFont("Helvetica", 11.5 * point)
            c.drawString(1 * inch + 120 + spaces_required[i], v, detail_response[i])
        elif detail_response[i] == "Bachelor of Business/Business Specialist/Commerce/Commerce Specialist and Bachelor of Information Technology":
            degree1 = "Bachelor of Business/Business Specialist/"
            degree2 = "Commerce/Commerce Specialist and Bachelor of Information Technology"
            c.drawString(1 * inch + 120 + spaces_required[i], v, degree1)
            v -= 14 * point
            c.drawString(1 * inch + 120, v, degree2)
        elif len(detail_response[i]) >= 64 and detail_section[i] == "Degree: ":
            new_word = detail_response[i].split(" ")
            first_half = ""
            second_half = ""
            prefix = ""
            for word in new_word[:len(new_word)//2]:
                first_half += prefix + word
                prefix = " "
            prefix = ""
            for word in new_word[len(new_word)//2:]:
                second_half += prefix + word
                prefix = " "

            c.setFont("Helvetica", 11.5 * point)
            c.drawString(1 * inch + 120 + spaces_required[i], v, first_half)
            v -= 14 * point
            c.drawString(1 * inch + 120, v, second_half)
        else:
            c.drawString(1 * inch + 120 + spaces_required[i], v, detail_response[i])
        v -= 14 * point

    # END student details section
    if specialisation != "":
        print(specialisation)
        c.setFont("Helvetica-Bold", 11.5 * point)
        c.drawString(1 * inch + 120, v, "Specialisation: ")
        c.setFont("Helvetica", 11.5 * point)
        c.drawString(1 * inch + 120 + 85, v, specialisation)
        v -= 14 * point
    elif major != "":
        print(major)
        c.setFont("Helvetica-Bold", 11.5 * point)
        c.drawString(1 * inch + 120, v, "Major: ")
        c.setFont("Helvetica", 11.5 * point)
        c.drawString(1 * inch + 120 + 38, v, major)
        v -= 14 * point

    """
    BODY TEXT
    ####################
    """
    # IBL Placement Interests
    v = 645

    c.setFont("Helvetica-Bold", 12 * point)
    c.drawString(1 * inch, v, "IBL Placement Interests")
    v -= 12 * point

    c.setFont("Helvetica", 8 * point)
    v = draw_paragraph(c, v, ibl_placement_interest)

    v -= 10 * point

    # Employment history
    if employment_history != "":
        c.setFont("Helvetica-Bold", 12 * point)
        c.drawString(1 * inch, v, "Employment History")
        v -= 12 * point

        c.setFont("Helvetica", 8 * point)

        split_history = employment_history.split("|")
        if len(split_history) > 1:
            for entry in split_history:
                v = draw_paragraph(c, v, entry)
        else:
            v = draw_paragraph(c, v, employment_history)

        v -= 10 * point

    # Career interests
    c.setFont("Helvetica-Bold", 12 * point)
    c.drawString(1 * inch, v, "Career Interests")
    v -= 12 * point

    c.setFont("Helvetica", 8 * point)
    v = draw_paragraph(c, v, career_interests)

    v -= 10 * point

    # Other interests
    c.setFont("Helvetica-Bold", 12 * point)
    c.drawString(1 * inch, v, "Other Interests")
    v -= 12 * point

    c.setFont("Helvetica", 8 * point)
    v = draw_paragraph(c, v, other_interests)

    v -= 10 * point

    temp = regex_stuff.get_codes(fav_subjects)
    if temp is not None:
        fav_subjects = temp

    # Units most enjoyed
    c.setFont("Helvetica-Bold", 12 * point)
    c.drawString(1 * inch, v, "Most Enjoyed Units")
    v -= 12 * point

    c.setFont("Helvetica", 8 * point)
    v = draw_paragraph(c, v, fav_subjects)

    v -= 10 * point

    draw_footer(c, v)

    # SAVE & EXPORT
    c.showPage()
    c.save()
    print(f"Saved as: {output_filename}")


def draw_footer(c, v):
    v = .6 * inch
    c.drawImage(str(LOGO_PATH), inch, .4 * inch)


def draw_paragraph(c, v, text):
    current_word_start_index = 0
    end_of_last_line = 0
    max_letters_in_line = 120
    for i, char in enumerate(text):
        if char == ' ':
            current_word_start_index = i + 1
        if i % max_letters_in_line == 0:
            c.drawString(1 * inch, v, text[end_of_last_line:current_word_start_index])
            end_of_last_line = current_word_start_index
            if i != 0:
                v -= 12 * point
        elif i == len(text) - 1:
            c.drawString(1 * inch, v, text[end_of_last_line:])
            v -= 12 * point
    return v


def read_students_from_csv(csv_path: Path = CSV_PATH) -> list[Student]:
    students = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items() if k is not None}
            students.append(Student(
                ibl_id=row["IBL_ID"],
                last_name=row["Family Name"],
                first_name=row["Given Names"],
                preferred_name=row["Preferred name"],
                degree=row["Degree"],
                major=row["Major"],
                specialisation=row["Specialisation"],
                ibl_placement_interest=row["IBL Placement Interest"],
                units_enjoyed=row["Units enjoyed"],
                employment_history=row["employment_history"],
                career_interests=row["Career_interests"],
                other_interests=row["other_interests"],
                photo=row["photo"],
            ))
    return students


def main():
    students = read_students_from_csv()
    for student in students:
        make_resume(student)

    # Merge individual PDFs into one combined file
    with PdfWriter() as writer:
        for pdf_path in sorted(OUTPUT_DIR.iterdir()):
            print(pdf_path.name)
            writer.append(str(pdf_path))
        with open(OUTPUT_PDF, "wb") as output_all:
            writer.write(output_all)


if __name__ == "__main__":
    main()
