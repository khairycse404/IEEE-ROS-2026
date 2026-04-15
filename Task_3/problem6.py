def analyze_grades(grades):
    return {
        "average": sum(grades) / len(grades),
        "highest": max(grades),
        "lowest": min(grades)
    }

print(analyze_grades([70, 80, 90, 60]))