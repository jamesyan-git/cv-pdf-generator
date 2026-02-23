import re
#
# def replace_unit_codes(units_enjoyed_most):
#     # match = re.search("[^\(]{1}[A-Za-z]{3}[0-9]{4}[^\)]{1}", units_enjoyed_most)
#     match = re.search("[^\(]?[A-Za-z]{3}[0-9]{4}[^\)]?", units_enjoyed_most)
#
#     match_index = re.finditer("[^\(]?[A-Za-z]{3}[0-9]{4}[^\)]?", units_enjoyed_most)
#     if match is not None:
#         print(match)
#         print(match.group())
#         return match.group()

    # else:
    #     print("No Match")

    # testdict = {"a":"b", 1:"butt"}

def get_codes(units_enjoyed_most):
    code_dict = {"FIT1045": "Algorithms and programming fundamentals in python",
                 "FIT1008": "Introduction to computer science",
                 "MTH1030": "Techniques for modelling",
                 "MTH2010": "Multivariable calculus",
                 "FIT1043": "Introduction to data science",
                 "FIT2085": "Introduction to computer science for engineers",
                 "ENG2005": "Advanced engineering mathematics",
                 "ENG1060": "Computing for engineers",
                 "ENG1003": "Engineering mobile apps",
                 "FIT1053": "Algorithms and programming in python (advanced)",
                 "ECC1000": "Principles of microeconomics",
                 "FIT2004": "Algorithms and data structures",
                 "ECE3141": "Information and networks",
                 "FIT2002": "IT project management",
                 "FIT1051": "Programming fundamentals in java",
                 "FIT1048": "Fundamentals of C++",
                 "FIT1047": "Introduction to computer systems, networks and security",
                 "ATS2139": "ATS2139 - Song writing: How to write a popular song",
                 "ATS1001": "ATS1001 - Chinese introductory 1",
                 "FIT1049": "IT professional practice",
                 "FIT2094": "Databases",
                 "ETF1100": "Business statistics",
                 "LAW1112": "Public law and statutory interpretation",
                 "FIT2100": "Operating systems",
                 "MAT1841": "Continuous mathematics for computer science",
                 "MTH1020": "Analysis of change",
                 "MIC2011": "Introduction to microbiology and microbial biotechnology",
                 "FIT2001": "Systems development",
                 "FIT1013": "Digital futures: IT for business",
                 "ECF1100": "Microeconomics",
                 "BFF2140": "Corporate finance 1",
                 "FIT1006": "Business information analysis",
                 "FIT2101": "Software engineering process and management",
                 "FIT2107": "Software quality and testing",
                 "ACC1200": "Accounting for managers",
                 "ENG1005": "Engineering mathematics",
                 "ENG1001": "Engineering design: Lighter, Faster, Stronger",
                 "MAT1830": "Discrete mathematics for computer science",
                 "FIT1054": "Computer science (advanced)",
                 "FIT2095": "e-Business software technologies",
                 "ACC1100": "Introduction to financial accounting",
                 "ACC2100": "Financial accounting",
                 "ETC1000": "Business and economic statistics",
                 "ECE2131": "Electrical circuits",
                 "FIT1060": "Computing for engineers",
                 "FIT1003": "IT in organisations",
                 "FIT2099": "Object oriented design and implementation",
                 "FIT2086": "Modelling for data analysis",
                 "BTC1110": "Commercial law",
                 "FIT2014": "Theory of computation",
                 "FIT2073": "Game design studio 1",
                 "FIT1046": "Interactive media foundations",
                 "FIT2081": "Mobile application development"
                 }

    if "(" not in units_enjoyed_most and "-" not in units_enjoyed_most:
        # match_indices =  [(m.start(0), m.end(0)) for m in re.finditer("[^\(]?[A-Za-z]{3}[0-9]{4}[^\)]?", units_enjoyed_most)]
        match_indices =  [(m.start(0), m.end(0)) for m in re.finditer("[A-Za-z]{3}[0-9]{4}", units_enjoyed_most)]

        if match_indices:
            new_str = units_enjoyed_most[:match_indices[0][0]]
            for i in range(1, len(match_indices) -1):
                start = match_indices[i][0]
                end = start + 7
                match = units_enjoyed_most[start:end]
                print(match)
                # Todo: split up and replace string
                # first_half = units_enjoyed_most[:start]
                # second_half = units_enjoyed_most[end:]
                unit_title = code_dict[match]
                new_str += unit_title + units_enjoyed_most[end: match_indices[i+1][0]]
                print(new_str)

            new_str += code_dict[units_enjoyed_most[match_indices[-1][0]:match_indices[-1][0] + 7]] + units_enjoyed_most[match_indices[-1][0] + 7:]
            print(new_str)
            return(new_str)


def write_dict():
    code_file = open("unit_codes.csv")
    text = "{"
    for line in code_file:
        line = line.split(',')
        text = text + "\"" + line[0] + "\":\"" + line[1].strip() + "\",\n"
    text = text + "}"
    print(text)

# write_dict()


def main():
    pass

    # get_codes(code_dict, "example")

# done: replace unit codes with unit names (make sure to not be redundant (as in "i liked fit 1045 (intro algorithms)"
# Todo: images
# done: some text has weird square characters
# Todo: some text is too long
# Todo: go over every one


# match = re.search("[A-Za-z]{3}[0-9]{4}", "FIT1053, MAT1830, MTH1030")
# print(match.groups())

if __name__ == "__main__":
    main()