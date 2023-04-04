import pandas as pd
import re
from fuzzywuzzy import process
import Test


def getCalories(labels):
    # Importing csv file
    data = pd.read_csv('Food and Calories - Sheet1.csv')

    # load string from text file
    with open('category.txt', 'r') as f:
        categories = f.read()

    # split string into list with newline as separator
    categories = categories.splitlines()

    # Lower each category in list
    categories = [category.lower() for category in categories]

    desiredCategories = data['Food'].tolist()

    # lower each category in desiredCategories
    desiredCategories = [category.lower() for category in desiredCategories]

    commonCategories = []
    missing_categories = []
    # for every missing category in missing categories extractOne from data['food'] if score is greater than 90 add to common categories
    for category in categories:
        if process.extractOne(category, desiredCategories)[1] >= 75:
            # append matched from desiredCategories to commonCategories
            commonCategories.append(desiredCategories[process.extractOne(category, desiredCategories)[2]])
        else:
            # append category to missing categories
            missing_categories.append(category)

    # # for every missing category in missing categories extractOne from data['food']
    # i=1
    # for category in missing_categories:
    #     print(i,' ',category,' ', process.extractOne(category, data['Food']))
    #     i+=1

    # print common categories length
    print(len(commonCategories))

    # print missing categories length
    print(len(missing_categories))

    keys_to_remove = []
    #check if label is in missing categories
    for label in labels.keys():
        if process.extractOne(label, missing_categories)[1] >= 90 and label not in commonCategories:
            print(label, 'not found')
            keys_to_remove.append(label)

    for key in keys_to_remove:
        labels.pop(key)
        
    # print labels
    print(labels)

    # Estimation Equation
    total_calories = 0
    for label in labels.keys():
        calories = data.loc[data['Food'] == label, 'Calories'].values[0]
        calories = int((int, re.findall(r'\d+', calories))[1][0])

        serving = data.loc[data['Food'] == label, 'Serving'].values[0]
        serving = int((int, re.findall(r'\d+', serving))[1][1])

        # Estimation Equation
        estimated_calories = calories * labels[label] / serving
        total_calories += estimated_calories

    # print estimated_calories with 1 decimal places
    print(f'Estimated calories: {total_calories:.1f}')

    # create json object that contains estimated calories and label keys
    json = {
        'Ingredients': list(labels.keys()),
        'Calories': total_calories
    }

    return json
