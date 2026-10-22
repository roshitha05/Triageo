import csv
import re


def extract_field(text, field):
    pattern = rf"{field}:\s*(.*?)(?=\s+(?:Category|Priority|Summary|Suggested Action):|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    if match:
        return match.group(1).strip()

    return ""


with open("data/results.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))


versions = ["V1", "V2", "V3"]

scores = {
    version: {
        "priority_correct": 0,
        "category_correct": 0,
        "total": len(rows)
    }
    for version in versions
}


for row in rows:
    expected_priority = row["expected_priority"].strip().lower()
    expected_category = row["expected_category"].strip().lower()

    for version in versions:
        output = row[f"{version}_output"]

        priority = extract_field(output, "Priority").lower()
        category = extract_field(output, "Category").lower()

        if priority == expected_priority:
            scores[version]["priority_correct"] += 1

        if category == expected_category:
            scores[version]["category_correct"] += 1


print("\nTriageo Prompt Evaluation\n")

for version in versions:
    total = scores[version]["total"]

    priority_accuracy = (
        scores[version]["priority_correct"] / total * 100
    )

    category_accuracy = (
        scores[version]["category_correct"] / total * 100
    )

    print(version)
    print(f"Priority accuracy: {priority_accuracy:.1f}%")
    print(f"Category accuracy: {category_accuracy:.1f}%")
    print()
