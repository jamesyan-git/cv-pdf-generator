from dataclasses import dataclass


@dataclass
class Student:
    ibl_id: str
    last_name: str
    first_name: str
    preferred_name: str
    degree: str
    major: str
    specialisation: str
    ibl_placement_interest: str
    units_enjoyed: str
    employment_history: str
    career_interests: str
    other_interests: str
    photo: str

    def __post_init__(self):
        self.ibl_id = f"{int(self.ibl_id):03d}"
