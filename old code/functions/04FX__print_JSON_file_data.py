import json

def print_JSON_file_data(JSON_file, keyword):
    with open(JSON_file, "r") as file:
        data = json.load(file)
        for academic_year, year_data in data.items():
            print(f"\nAcademic Year: {academic_year}\n------")
            for semester_data in year_data:
                for classes_data in semester_data["classes"]:
                    if keyword in classes_data:
                        print(classes_data[keyword])
