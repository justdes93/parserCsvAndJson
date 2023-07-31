import json
import difflib
import pandas as pd

def load_csv(file_name):
    dataframe = pd.read_csv(file_name)

    (rows, _columns) = dataframe.shape

    result = []

    for i in range(rows):
        temp = {
          "_id": dataframe["_id"][i],
          "clientId": dataframe["clientId"][i],
          "vendorClientId": dataframe["vendorClientId"][i],
          "vendorId": dataframe["vendorId"][i],
          "status": dataframe["status"][i],
          "contactData": {
            "street": dataframe["contactData.street"][i],
            "houseNumber": dataframe["contactData.houseNumber"][i],
            "zip": dataframe["contactData.zip"][i],
            "city": dataframe["contactData.city"][i],
            "country": dataframe["contactData.country"][i]
          }
        }

        result.append(temp)

    return result


def similarity(s1, s2):
  normalized1 = str(s1).lower()
  normalized2 = str(s2).lower()
  matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
  return matcher.ratio()


def first_filter(one, two):
    if not "contactData" in one or not "contactData" in two:
        return False
    if not "zip" in one["contactData"] or not "zip" in two["contactData"]:
        return False
    if not "street" in one["contactData"] or not "street" in two["contactData"]:
        return False

    if one["contactData"]["zip"] == two["contactData"]["zip"]:
        if similarity(one["contactData"]["street"], two["contactData"]["street"]) >= 0.6:
            return True
    return False


def second_filter(one, two):

    if not "contactData" in one or not "contactData" in two:
        return False

    if not "houseNumber" in one["contactData"] or not "houseNumber" in two["contactData"]:
        return False

    if first_filter(one, two) and one["contactData"]["houseNumber"] == two["contactData"]["houseNumber"]:
        return True
    return False


def remove_collision(data, check):
    result = []

    for i in range(len(data)):
        item = data[i]
        print(item, i)

        if "duplicate" in item:
            continue

        result.append(item)
        item["duplicate"] = True

        for j in range(len(data)):
            temp = data[j]

            if "duplicate" in temp:
                continue

            if check(item, temp):
                temp["duplicate"] = True

    return result


def format(data):
    result = {
        "_id": [],
        "clientId": [],
        "vendorClientId": [],
        "vendorId": [],
        "status": [],
        "street": [],
        "houseNumber": [],
        "zip": [],
        "city": [],
        "country": []
    }

    for item in data:
        if "_id" in item:
            result["_id"].append(item["_id"])
        else:
            result["_id"].append('')

        if "clientId" in item:
            result["clientId"].append(item["clientId"])
        else:
            result["clientId"].append('')

        if "vendorClientId" in item:
            result["vendorClientId"].append(item["vendorClientId"])
        else:
            result["vendorClientId"].append('')

        if "vendorId" in item:
            result["vendorId"].append(item["vendorId"])
        else:
            result["vendorId"].append('')

        if "status" in item:
            result["status"].append(item["status"])
        else:
            result["status"].append('')

        if "contactData" in item:
            if "street" in item["contactData"]:
                result["street"].append(item["contactData"]["street"])
            else:
                result["street"].append('')

            if "houseNumber" in item["contactData"]:
                result["houseNumber"].append(item["contactData"]["houseNumber"])
            else:
                result["houseNumber"].append('')

            if "zip" in item["contactData"]:
                result["zip"].append(item["contactData"]["zip"])
            else:
                result["zip"].append('')

            if "city" in item["contactData"]:
                result["city"].append(item["contactData"]["city"])
            else:
                result["city"].append('')

            if "country" in item["contactData"]:
                result["country"].append(item["contactData"]["country"])
            else:
                result["country"].append('')
        else:
            result["city"].append('')
            result["zip"].append('')
            result["street"].append('')
            result["houseNumber"].append('')
            result["country"].append('')

    return result


def write_file(data, output):
    writer = pd.ExcelWriter(output)
    parse_data = format(data)
    dataframe = pd.DataFrame(data=parse_data)
    dataframe.to_excel(writer, "list_1", index=False)

    writer._save()


def main():
    file_name = "example.json"
    csv_file_name = "example.csv"
    first_output = "output111.xlsx"
    second_output = "output222.xlsx"

    json_data = load_csv(csv_file_name)

    # with open(file_name, "r", encoding="utf-8") as file:
    #     json_data = json.load(file)

    data_first = remove_collision(json_data, first_filter)

    # with open(file_name, "r", encoding="utf-8") as file:
    #     json_data = json.load(file)

    json_data = load_csv(csv_file_name)

    data_second = remove_collision(json_data, second_filter)

    write_file(data_first, first_output)
    write_file(data_second, second_output)


main()
