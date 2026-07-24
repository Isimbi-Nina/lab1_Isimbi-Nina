import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print(f"Error: The file '{filename}' is empty or not a valid CSV.")
                sys.exit(1)

            required_fields = {'assignment', 'group', 'score', 'weight'}
            if not required_fields.issubset(reader.fieldnames):
                print(f"Error: The CSV file must contain the following columns: {', '.join(required_fields)}")
                sys.exit(1)

            for row_num, row in enumerate(reader, start=2):
                if not any(row.values()):
                    continue
 
                assignment = row.get('assignment', '').strip()
                group = row.get('group', '').strip()
                raw_score = row.get('score', '').strip()
                raw_weight = row.get('weight', '').strip()

                if not assignment or not group or raw_score == '' or raw_weight == '':
                    print(f"Warning: Skipping row {row_num} — missing required field(s).")
                    continue
 
                try:
                    score = float(raw_score)
                    weight = float(raw_weight)
                except ValueError:
                    print(f"Warning: Skipping row {row_num} — score/weight not numeric.")
                    continue
 
                if group not in ('Formative', 'Summative'):
                    print(f"Warning: Skipping row {row_num} — unknown group '{group}'.")
                    continue

                assignments.append({
                    'assignment': assignment,
                    'group': group,
                    'score': score,
                    'weight': weight
                })
 
        if not assignments:
            print("Error: No valid assignment records were found in the CSV.")
            sys.exit(1)



        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
   
    print("\n--- Processing Grades ---")

    # Grade range validation: 
    invalid_scores = [a for a in data if not (0 <= a['score'] <= 100)]
    if invalid_scores:
        print("Error: The following assignments have scores outside the 0-100 range:")
        for a in invalid_scores:
            print(f"  - {a['assignment']}: {a['score']}")
        sys.exit(1)
 
    # Weight validation
    total_weight = sum(a['weight'] for a in data)
    formative = [a for a in data if a['group'] == 'Formative']
    summative = [a for a in data if a['group'] == 'Summative']
    formative_weight = sum(a['weight'] for a in formative)
    summative_weight = sum(a['weight'] for a in summative)
 
    errors = []
    if round(total_weight, 2) != 100:
        errors.append(f"Total weight is {total_weight}, expected: 100.")
    if round(formative_weight, 2) != 60:
        errors.append(f"Formative weight is {formative_weight}, expected: 60.")
    if round(summative_weight, 2) != 40:
        errors.append(f"Summative weight is {summative_weight}, expected: 40.")
 
    if errors:
        print("Error: Weight validation failed:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
 
    # Calculate Final Grade and GPA
    total_grade = sum((a['score'] * a['weight']) / 100 for a in data)
    gpa = (total_grade / 100) * 5.0
 
    # Category percentages
    formative_percentage = (sum(a['score'] * a['weight'] for a in formative) / (formative_weight * 100)) * 100
    summative_percentage = (sum(a['score'] * a['weight'] for a in summative) / (summative_weight * 100)) * 100
 
    # Pass or Fail
    passed = formative_percentage >= 50 and summative_percentage >= 50
    if passed:
        status = "PASSED"
    else:
        status = "FAILED"
 
    # Resubmission logic
    failed_formatives = [a for a in formative if a['score'] < 50]
    resubmission_list = []
    if failed_formatives:
        highest_weight = max(a['weight'] for a in failed_formatives)
        resubmission_list = [a for a in failed_formatives if a['weight'] == highest_weight]
 
    # Print results
    print(f"\nTotal Grade: {total_grade:.2f}/100")
    print(f"Final GPA: {gpa:.2f} / 5.0")
    print(f"Final Status: {status}")
 
    if failed_formatives:
        print("\nResubmission assignments:")
        for a in resubmission_list:
            print(f"  - {a['assignment']} (score: {a['score']}, weight: {a['weight']})")
    else:
        print("\nNo formative assignments require resubmission.")
 
    


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)