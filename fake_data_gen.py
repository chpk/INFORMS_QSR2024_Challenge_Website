import csv

# Define the data for the leaderboard
leaderboard_data = [
    ["1", "Team A", "Random Forest", "0.92", "95%", "0.03", "0.05"],
    ["2", "Team B", "XGBoost", "0.89", "93%", "0.04", "0.07"],
    ["3", "Team C", "SVM", "0.87", "91%", "0.06", "0.09"],
    ["4", "Team D", "Logistic Regression", "0.85", "90%", "0.08", "0.10"],
    ["5", "Team E", "Neural Network", "0.83", "88%", "0.09", "0.12"]
]

# Define the header row for the CSV file
header = ["Serial No", "Name", "Pipeline Description", "F1 Score", "Accuracy %", "Type 1 Error", "Type 2 Error"]

# Create the CSV file and write the data
with open("leaderboard.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(leaderboard_data)

print("Leaderboard CSV file created successfully.")