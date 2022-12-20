import csv
import json
from collections import defaultdict as df

data = dict(df())

with open("data/flight.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    var = []

    for row in reader:
        if not len(var):
            var = list(row.keys())
        data[row["Time"]] = {i: row[i] for i in var[1:-1]}

with open("data/data.json", "w") as file:
    json.dump(data, file, indent=2)
