def calculate_homework(homework_assignments):
    sum_of_grades = 0
    for grade in homework_assignments.values():
        sum_of_grades += grade

    final_grade = sum_of_grades / len(homework_assignments)
    return round(final_grade, 2)    # Làm tròn 2 chữ số