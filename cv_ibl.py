#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from reportlab.pdfgen import canvas
import os
import re
import regex_stuff
import codecs

"""
PATH: "/home/james/cvProject/cv_ibl_2018_s2/ibl/###"
DATA ABSOLUTE: "/home/james/cvProject/cv_ibl_2018_s2/ibl/###"
DARA RELATIVE: "data/responses_2018_s2.csv"
"""

"""
Available fonts:
standardFonts = (
    'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',
    'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique',
    'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic',
    'Symbol','ZapfDingbats')
"""



"""
generate_student_data expects a CSV with a header row corresponding to the form questions,
and each subsequent row corresponding to individual responses.

PLEASE NOTE: It is important to replace newline characters in the csv before reading in here.
This can be done in many ways in Excel, Libreoffice Calc, and possible Google Sheets, 
just look it up if you don't already have your own method, wont be hard but it is necessary.

for LibreOffice
tools > find & replace > more options > check 'regular expression' > search '\n' > replace with empty string

"""
# In Typography, a point is defined as 1/72 inch.
# So 1 1 point = 72 inches
point = 1
inch = 72
# A4 imperial standards:
PAGEWIDTH = 8.267 * inch
PAGEHEIGHT = 11.692 * inch
# str = unicode(str, errors='ignore')


# def replace_unit_codes(units_enjoyed_most):
#     match = re.search("[A-Za-z]{3}[0-9]{4}", units_enjoyed_most)
#     print(match)
#

def make_resume(student_details):
    # Setup
    v = 10.8 * inch

    IBL_ID = student_details[0]
    Last_name = student_details[1]
    First_name = student_details[2]
    Preferred_name = student_details[3]
    degree = student_details[4]
    major = student_details[5]
    specialisation = student_details[6]
    ibl_placement_interest = student_details[7]
    fav_subjects = student_details[8]
    employment_history = student_details[9]
    career_interests = student_details[10]
    other_interests = student_details[11]
    photo = student_details[12]

    ibl_id = "{:03d}".format(int(IBL_ID))
    IBL_ID = str(ibl_id)

    output_filename = "out/{}_{}.pdf".format(str(Last_name).replace(' ','_'), First_name.replace(' ','_'))

    print("Creating: " + output_filename)
    """
    Create Canvas
    """
    c = canvas.Canvas(output_filename, pagesize=(PAGEWIDTH, PAGEHEIGHT))
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)

    """
    END
    TEMPORARY PLACEHOLDER IMAGE
    """

    student_name = First_name.strip(" ").capitalize() + " " + Last_name.replace("'", "_").strip(" ").capitalize()
    alternative_name = "***"
    if len(Preferred_name) > 1:
        alternative_name = Preferred_name.strip(" ").capitalize() + " " + Last_name.replace("'", "_").strip(" ").capitalize()
    print(student_name)

    path = "images/resized/"

    try:
        for file_name in os.listdir(path):
            if student_name.lower() in file_name.lower():
                c.drawImage("images/resized/{}".format(file_name), 1 * inch, 10.8 * inch - 110)
                # break
            elif alternative_name.lower() in file_name.lower():
                print("HELLO ALTERNATIVE NAME")
                c.drawImage("images/resized/{}".format(file_name), 1 * inch, 10.8 * inch - 110)
                # break
            elif len(First_name.strip().split(' ')) >= 2:
                possible_name_1 = First_name.strip().split(' ')[0] + " " + Last_name
                possible_name_2 = First_name.strip().split(' ')[1] + " " + Last_name
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage("images/resized/{}".format(file_name), 1 * inch, 10.8 * inch - 110)
            elif len(First_name.strip().split('-')) >= 2:
                possible_name_1 = First_name.strip().split('-')[0] + " " + Last_name
                possible_name_2 = First_name.strip().split('-')[1] + " " + Last_name
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage("images/resized/{}".format(file_name), 1 * inch, 10.8 * inch - 110)
            elif len(Last_name.strip().split(' ')) >= 2:
                possible_name_1 = First_name + " " + Last_name.strip().split(' ')[0]
                possible_name_2 = First_name + " " + Last_name.strip().split(' ')[1]
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage("images/resized/{}".format(file_name), 1 * inch, 10.8 * inch - 110)
            elif len(Last_name.strip().split('-')) >= 2:
                possible_name_1 = First_name + " " + Last_name.strip().split('-')[0]
                possible_name_2 = First_name + " " + Last_name.strip().split('-')[1]
                if possible_name_1.lower() in file_name.lower() or possible_name_2.lower() in file_name.lower():
                    c.drawImage("images/resized/{}".format(file_name), 1 * inch, 10.8 * inch - 110)
    except OSError as e:
        print("Error: ", e)
    # Insert IBL ID
    id = student_details[0]
    if id[0] == '0':
        id = id[1]
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
    detail_section = ["First Name: ", "Surname: ","Degree: "]
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



        elif len(detail_response[i]) >= 64 and detail_section[i]=="Degree: ":
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
    # IBL Placement Interets
    v = 645

    c.setFont("Helvetica-Bold", 12 * point)
    c.drawString(1 * inch, v, "IBL Placement Interests")
    v -= 12 * point

    c.setFont("Helvetica", 8 * point)
    v = draw_paragraph(c, v, ibl_placement_interest)

    v -= 10 * point

    # employment history
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

    #Career interests
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
    print("Saved as: " + output_filename)


def draw_footer(c, v):
    v = .6 * inch
    c.drawImage("fit_logo.png", inch, .4 * inch)


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


def read_data_from_csv():
    responses = []
    questions = []
    student_details_file = open("student_responses.csv")
    for i, line in enumerate(student_details_file):
        if i != 0:
            responses.append(line.strip().split(','))
        else:
            questions = line.strip().split(',')

    student_details_file.close()
    return responses, questions


def replace_commas(all_responses):
    for i, student_response in enumerate(all_responses):
        for j, section in enumerate(student_response):
            if '$' in section:
                all_responses[i][j] = section.replace('$', ',')
    return all_responses

def main():

    responses = []
    questions = []

    responses, questions = read_data_from_csv()

    responses = replace_commas(responses)
    for response in responses:
        (make_resume(response))


    # group output
    # output_all_pdf = PdfFileMerger()
    # output_all_list = []

    # pdfs_path = 'C:/Users/User/projects/cv_ibl_2020_jan/out/'
    # filenames = []
    # for file_name in os.listdir(pdfs_path):
    #     # output_all_pdf.append(open("output_smaller_3/" + file_name))
    #     filenames.append(file_name)
    # filenames.sort()
    # for file_name in filenames:
    #     print(file_name)
    #     temp = "C:/Users/User/projects/cv_ibl_2020_jan/out" + file_name
    #     output_all_pdf.append(open(temp, 'rb'))
    # output_all = open("C:/Users/User/projects/cv_ibl_2020_jan", "wb")
    # output_all_pdf.write(output_all)

main()