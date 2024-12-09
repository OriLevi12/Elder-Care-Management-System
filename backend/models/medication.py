from typing import List

class Medication:
    medications: List["Medication"] = []
    medication_id = 1

    def __init__(self, name: str, dosage: str, frequency: str):
        self.id = Medication.medication_id
        self.name = name
        self.dosage = dosage
        self.frequency = frequency

        Medication.medication_id += 1

    @classmethod
    def add_medication(cls, name: str, dosage: str, frequency: str):
        if cls.is_duplicate(name):
            return None
        medication = cls(name, dosage, frequency)
        cls.medications.append(medication)
        return medication

    @classmethod
    def is_duplicate(cls, name: str):
        return any(med.name == name for med in cls.medications)

    @classmethod
    def delete_medication(cls, id: int):
        for i, med in enumerate(cls.medications):
            if med.id == id:
                return cls.medications.pop(i)
        return None

    @classmethod
    def get_all_medications(cls):
        return [med.__dict__ for med in cls.medications]

