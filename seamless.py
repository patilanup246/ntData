import re, csv, time, json, requests, unicodedata
import random
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


auth_token = ""


def main():
    jsondata = "[{\"xappid\":\"ff0ccea8\",\"xappkey\":\"605660a17994344157a78f518a111eda\",\"xremoteuserid\":\"26ef87cb-e285-493b-9cda-141731ed3f02\"},{\"xappid\":\"ff0ccea8\",\"xappkey\":\"605660a17994344157a78f518a111eda\",\"xremoteuserid\":\"7a43c5ba-50e7-44fb-b2b4-bbd1b7d22632\"},{\"xappid\":\"e527beec\",\"xappkey\":\"b6b0b0be59e9c60a4e9194119834deca\",\"xremoteuserid\":\"0\"},{\"xappid\":\"240c70ea\",\"xappkey\":\"5b98e8dfb93416ccf82a05f5f5073f72\",\"xremoteuserid\":\"0\"},{\"xappid\":\"428a1f39\",\"xappkey\":\"080f20a722118011a86c2b7f3a32c47a\",\"xremoteuserid\":\"0\"},{\"xappid\":\"6bbdffac\",\"xappkey\":\"66dc95ac590ef97c7de66e82397a3853\",\"xremoteuserid\":\"0\"},{\"xappid\":\"b95d0dcf\",\"xappkey\":\"212cbc851fcb0ee6b51095b5f0ebc49d\",\"xremoteuserid\":\"0\"},{\"xappid\":\"06cffb84\",\"xappkey\":\"72280d9947c1dedad88a5876005e97fe\",\"xremoteuserid\":\"0\"},{\"xappid\":\"d0025a85\",\"xappkey\":\"423e3a386b4a6b7c4ad3eebfea0fa4b9\",\"xremoteuserid\":\"0\"},{\"xappid\":\"d5c29508\",\"xappkey\":\"8b1622b3eaf45a8a90c91da716f1692a\",\"xremoteuserid\":\"0\"},{\"xappid\":\"9a063781\",\"xappkey\":\"2d771b16b3efbe76dfc878be582f890b\",\"xremoteuserid\":\"0\"},{\"xappid\":\"beeef40f\",\"xappkey\":\"cb4cbe72b287f9c795ac894f3ef544fd\",\"xremoteuserid\":\"0\"},{\"xappid\":\"da0a3819\",\"xappkey\":\"2865a994886d0e258357d55037e33f3b\",\"xremoteuserid\":\"0\"},{\"xappid\":\"dbcca75c\",\"xappkey\":\"9fdab229d0876f88bc286ea1590b1d24\",\"xremoteuserid\":\"0\"},{\"xappid\":\"f27d5bae\",\"xappkey\":\"3858e7b7b95259090466bdb18fe5293f\",\"xremoteuserid\":\"0\"},{\"xappid\":\"513fceb775b8dbbc210030a8\",\"xappkey\":\"513fceb775b8dbbc210030a8\",\"xremoteuserid\":\"0\"},{\"xappid\":\"7a8d4678\",\"xappkey\":\"ba736127e4d4e482a9b54760a66f598b\",\"xremoteuserid\":\"0\"},{\"xappid\":\"3295a486\",\"xappkey\":\"bf445d5862ac6c6213485dec89c1a47f\",\"xremoteuserid\":\"0\"},{\"xappid\":\"beeef40f\",\"xappkey\":\"cb4cbe72b287f9c795ac894f3ef544fd\",\"xremoteuserid\":\"0\"},{\"xappid\":\"a85620e6\",\"xappkey\":\"8c8ce17420367ed56bc28cb84ce66315\",\"xremoteuserid\":\"0\"},{\"xappid\":\"b95d0dcf\",\"xappkey\":\"212cbc851fcb0ee6b51095b5f0ebc49d\",\"xremoteuserid\":\"0\"},{\"xappid\":\"9d90687a\",\"xappkey\":\"ce2d2319cdcd23cd6bf1f7cc07da62b9\",\"xremoteuserid\":\"0\"},{\"xappid\":\"f7a22d78\",\"xappkey\":\"5270ade74c71a5ef3b06beeec67164b8\",\"xremoteuserid\":\"0\"}]"
    my_list = []
    relatedkeyvalue = parsedinstant = json.loads(jsondata)
    output_file = 'result_nutritionix.csv'
    data_to_file = open(output_file, 'w', newline='')
    csv_writer = csv.writer(data_to_file, delimiter=",")
    csv_writer.writerow(
        ["Restaurant", "Seamless Food Item Main", "Seamless Food Item Sub", "Nutritionix Food Item", "Serving Size",
         "Calories", "Calories from Fat", "Total Fat", "Saturated Fat",
         "Trans Fat", "Cholesterol", "Sodium", "Total Carbohydrates", "Dietary Fiber", "Sugars", "Proteins",
         "Vitamin A", "Vitamin C", "Calcium", "Iron"
         ])
    global auth_token
    auth_url = "https://api-gtm.grubhub.com/auth"
    auth_payload = {"brand": "GRUBHUB", "client_id": "beta_UmWlpstzQSFmocLy3h1UieYcVST", "device_id": -1512757421,
                    "scope": "anonymous"}
    url = "https://api-gtm.grubhub.com/restaurants/2316?hideChoiceCategories=true&version=4&variationId=rtpFreeItems&orderType=standard&hideUnavailableMenuItems=true&hideMenuItems=false&showMenuItemCoupons=true&includePromos=true&location=POINT(-73.99679566%2040.75337982)&locationMode=delivery"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': auth_token}
    application_json = {'Content-Type': 'application/json'}
    try:
        json_text = json.loads(requests.get(url, headers=headers).text)
    except:
        r = requests.post(auth_url, headers=application_json, data=json.dumps(auth_payload))
        auth_token = "Bearer " + json.loads(r.text)['session_handle']['access_token']
        headers = {'Accept': 'application/json', 'Authorization': auth_token}
        json_text = json.loads(requests.get(url, headers=headers).text)
    numberrecords = 0
    for restaurant in json_text['restaurant']['menu_category_list']:
        for menuname in restaurant['menu_item_list']:
            try:
                name = menuname['name']
                with open('commonfood.csv', newline='') as csvfile:
                    spamwriter = csv.DictReader(csvfile)
                    mostsimilarc = 0
                    mostsimilarn = 0
                    for rowdata in spamwriter:
                        mostsimilarn = fuzz.ratio(rowdata["Food Item"].lower(), name.lower())
                        if mostsimilarn > mostsimilarc:
                            mostsimilarc = mostsimilarn
                            row1 = rowdata

                    numberrecords += 1
                    seamless_Food_ItemmMain = name
                    seamless_Food_ItemmSub = name
                    Restaurant = json_text['restaurant']['name']
                    nutritionix_Food_Item = row1["Food Item"]
                    Serving_Size = row1["Serving Size"]
                    Calories = row1["Calories"]
                    Calories_from_Fat = row1["Calories from Fat"]
                    Total_Fat = row1["Total Fat"]
                    Saturated_Fat = row1["Saturated Fat"]
                    Trans_Fat = row1["Trans Fat"]
                    Cholesterol = row1["Cholesterol"]
                    Sodium = row1["Sodium"]
                    Total_Carbohydrates = row1["Total Carbohydrates"]
                    Dietary_Fiber = row1["Dietary Fiber"]
                    Sugars = row1["Sugars"]
                    Proteins = row1["Proteins"]
                    Vitamin_A = row1["Vitamin A"]
                    Vitamin_C = row1["Vitamin C"]
                    Calcium = row1["Calcium"]
                    Iron = row1["Iron"]
                    csv_writer.writerow(
                        [Restaurant, seamless_Food_ItemmMain, seamless_Food_ItemmSub, nutritionix_Food_Item,
                         Serving_Size, Calories, Calories_from_Fat, Total_Fat,
                         Saturated_Fat,
                         Trans_Fat, Cholesterol, Sodium, Total_Carbohydrates, Dietary_Fiber, Sugars, Proteins,
                         Vitamin_A, Vitamin_C, Calcium, Iron])
                    print(str(numberrecords) + " ]food_name: " + nutritionix_Food_Item)

                with open('commonfood.csv', newline='') as csvfile:
                    spamwriter2 = csv.DictReader(csvfile)
                    spamwriter3 = spamwriter2
                    auth_url1 = "https://api-gtm.grubhub.com/auth"
                    auth_payload1 = {"brand": "GRUBHUB", "client_id": "beta_UmWlpstzQSFmocLy3h1UieYcVST",
                                     "device_id": -1512757421,
                                     "scope": "anonymous"}
                    url1 = "https://api-gtm.grubhub.com/restaurants/2316/menu_items/" + menuname[
                        'id'] + "?time=1568719007454&orderType=standard&version=4"
                    headers1 = {'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Authorization': auth_token}
                    application_json1 = {'Content-Type': 'application/json'}
                    try:
                        json_text1 = json.loads(requests.get(url1, headers=headers1).text)
                    except:
                        r1 = requests.post(auth_url1, headers=application_json1, data=json.dumps(auth_payload1))
                        auth_token1 = "Bearer " + json.loads(r1.text)['session_handle']['access_token']
                        headers1 = {'Accept': 'application/json', 'Authorization': auth_token1}
                        json_text1 = json.loads(requests.get(url1, headers=headers1).text)
                    for _databrand in json_text1["choice_category_list"]:
                        for _category_list in _databrand["choice_option_list"]:
                            try:
                                itemextra = _category_list['description'].replace('Add', '').strip()
                                itemextra = itemextra.replace('Remove', '')
                                itemextra = itemextra.replace('Extra', '')

                                mostsimilarc = 0.0
                                mostsimilarn = 0.0
                                for rowdataItems in spamwriter3:
                                    mostsimilarn =fuzz.ratio(rowdataItems["Food Item"].lower(), itemextra.lower())
                                    if mostsimilarn > mostsimilarc:
                                        mostsimilarc = mostsimilarn
                                        row = rowdataItems

                                numberrecords += 1
                                seamless_Food_ItemmMain = name
                                seamless_Food_ItemmSub = itemextra
                                Restaurant = json_text['restaurant']['name']
                                nutritionix_Food_Item = row["Food Item"]
                                Serving_Size = row["Serving Size"]
                                Calories = row["Calories"]
                                Calories_from_Fat = row["Calories from Fat"]
                                Total_Fat = row["Total Fat"]
                                Saturated_Fat = row["Saturated Fat"]
                                Trans_Fat = row["Trans Fat"]
                                Cholesterol = row["Cholesterol"]
                                Sodium = row["Sodium"]
                                Total_Carbohydrates = row1["Total Carbohydrates"]
                                Dietary_Fiber = row["Dietary Fiber"]
                                Sugars = row["Sugars"]
                                Proteins = row["Proteins"]
                                Vitamin_A = row["Vitamin A"]
                                Vitamin_C = row["Vitamin C"]
                                Calcium = row["Calcium"]
                                Iron = row["Iron"]
                                csv_writer.writerow(
                                    [Restaurant, seamless_Food_ItemmMain, seamless_Food_ItemmSub,
                                     nutritionix_Food_Item, Serving_Size, Calories, Calories_from_Fat, Total_Fat,
                                     Saturated_Fat,
                                     Trans_Fat, Cholesterol, Sodium, Total_Carbohydrates, Dietary_Fiber, Sugars,
                                     Proteins,
                                     Vitamin_A, Vitamin_C, Calcium, Iron])
                                print(str(
                                    numberrecords) + " ]food name Main: " + seamless_Food_ItemmMain + ", #food name sub: " + seamless_Food_ItemmSub)

                            except Exception:
                                print(
                                    str(numberrecords) + " ]food name Main: " + seamless_Food_ItemmMain + ", #food name sub: " + seamless_Food_ItemmSub)

                                pass  # or you could use 'continue'
            except Exception:
                print(
                    str(
                        numberrecords) + " ]food name Main: " + seamless_Food_ItemmMain + ", #food name sub: " + seamless_Food_ItemmSub)

                pass  # or you could use 'continue'
        data_to_file.close()


if __name__ == '__main__':
    main()
