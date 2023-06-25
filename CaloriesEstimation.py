import pandas as pd
import re
from fuzzywuzzy import process
import Test
import json


def getCalories(labels):
    # Importing csv file
    data = pd.read_csv('Food_Model/foodcalories.csv')
    data['Food'] = data['Food'].str.lower()
    labels = {key.lower(): value for key, value in labels.items()}

    cal_map = {}
    total_calories, total_protein, total_fat, total_carb = 0, 0, 0, 0
    for label in labels.keys():
        calories_series = data.loc[data['Food'] == label, 'Calories']
        if calories_series.empty:
            label = process.extractOne(label, data['Food'].tolist())[0]
            calories_series = data.loc[data['Food'] == label, 'Calories']

        calories = int((int, re.findall(r'\d+', calories_series.values[0]))[1][0])

        serving_series = data.loc[data['Food'] == label, 'Serving']
        serving = int((int, re.findall(r'\d+', serving_series.values[0]))[1][1])

    # Estimation Equation
        estimated_calories = calories * labels[label] / serving
        total_calories += estimated_calories
        cal_map[label] = estimated_calories

        protein_series = data.loc[data['Food'] == label, 'Protein (g)']
        protein = float(protein_series.values[0])

        fat_series = data.loc[data['Food'] == label, 'Fat (g)']
        fat = float(fat_series.values[0])

        carb_series = data.loc[data['Food'] == label, 'Carbohydrates (g)']
        carb = float(carb_series.values[0])

        estimated_protein = protein * labels[label] / serving
        estimated_fat = fat * labels[label] / serving
        estimated_carb = carb * labels[label] / serving

        total_protein += estimated_protein
        total_fat += estimated_fat
        total_carb += estimated_carb


    # print estimated_calories with 1 decimal places
    print(f'Estimated calories: {total_calories:.1f}')

    json = {}
    for key, value in cal_map.items():
        json[key] = int(value)

    json['total_protein'] = float(total_protein)
    json['total_fat'] = float(total_fat)
    json['total_carb'] = float(total_carb)

    return json
