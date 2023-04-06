import requests, json
import time
import pandas as pd
# import csv
rows = []

# for dev
#url = "http://3.12.166.251:8080/infer"

# for prod
url = "http://3.145.164.197:8080/infer"

test_sport = ["baseball","football","basketball"]

text_file_dict = {
    "baseball":"text_file/baseball.txt",
    "football":"text_file/football.txt",
    "basketball":"text_file/basketball.txt",
    # "magic":"text_file/magic.txt",
    # "hockey":"text_file/hockey.txt"
    }

csv_file_dict = {
    "baseball":"text_file/baseball.csv",
    "football":"text_file/football.csv",
    "basketball":"text_file/basketball.csv",
    # "magic":"text_file/magic.csv",
    # "hockey":"text_file/hockey.csv"
    }


incorrect_dict = {}
c=0
for sport in test_sport:
    list1 = []
    correct_count = 0
    incorrect_count = 0
    with open(text_file_dict[sport],'r') as f:
        lines = f.readlines()
    
    csv_path = csv_file_dict[sport]
    df = pd.read_csv(csv_path,header=None)
    toplist = df.values.tolist()
    csv_dict1 = {}
    csv_dict2 = {}
    
    for x in toplist:
        csv_dict1[x[0]] = x[1]
        csv_dict2[x[0]] = x[2]

    for line in lines:
        imgurl = line.split('\n')[0]
        imgname = imgurl.split("/")[-1]
 
        message = {
            "path": imgurl,
            "scan_id": f"bigvision-nitin-test-scan-{sport}-{c}",
            "user_selection": sport,
            "response_url": "https://cs-dev-v2.ludex.com/scans/complete",
        }
        data_dict = json.dumps(message)
        c+=1
        resp = requests.post(url=url, data=data_dict)
        result = resp.json()["Result"]
        x = json.loads(result)["class"]
        y = json.loads(result)["par11k"][0]
        if csv_dict1[imgurl] == x and csv_dict2[imgurl] == y:
            correct_count = correct_count +1
        else:
            list1.append(imgurl)
            print(imgurl)
            print(x)
            print(y)
            incorrect_count = incorrect_count +1
    print("Sport : ",sport)
    print("  Correct : ",correct_count)
    print("  Incorrect : ",incorrect_count)
    
    incorrect_dict[sport] = list1
print("Incorrect Cards")
print(incorrect_dict)
    
