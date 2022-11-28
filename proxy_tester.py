import requests
import csv
import sys

# untested_proxies = []
# working_proxies = ["110.78.138.31:8080","110.78.138.31:8080"]

# with open("untested_proxies.csv", "r") as file:
#     reader = csv.reader(file)
#     for row in reader:
#         untested_proxies.append(str(row[0]))

# for proxy in untested_proxies:
#     try:
#         r = requests.get("https://www.lazada.sg/catalog/?spm=a2o42.home.search.1.654346b5IWz0ht&q=apple%20airpods%20pro%20(2nd%20generation)&_keyori=ss&from=search_history&sugg=apple%20airpods%20pro%20%282nd%20generation%29_0_1", proxies={'http':proxy,'https': proxy}, timeout=2)
#         print(r.status_code, f"{proxy} WORKING")
#         working_proxies.append(proxy)
#     except:
#         print(f"error with {proxy}")

# print("done with testing")

# with open("tested_proxies.csv", "a") as file :
#     for row in working_proxies:
#         file.write(f"{row}\n")


def test_proxy(proxy, website):
    try:
        r = requests.get(f"{website}", proxies={'http':proxy,'https': proxy}, timeout=2)
        print(r.status_code, f"{proxy} WORKING")
        return proxy
    except:
        print(f"error with {proxy}")
        return None

def test_proxy_production(proxy, website):
    try:
        r = requests.get(f"{website}", proxies={'http':proxy,'https': proxy}, timeout=3)
        print(r.status_code, f"{proxy} WORKING")
        return proxy
    except:
        print(f"error with {proxy}")
        return None


def get_response(proxy, website):
    try:
        r = requests.get(f"{website}", proxies={'http':proxy,'https': proxy}, timeout=3)
        print(r.status_code, f"{proxy} WORKING")
        return r
    except:
        print(f"error with {proxy}")
        return None

def reading_proxy(file):
    untested_proxies = []
    with open(file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            untested_proxies.append(str(row[0]))
    return untested_proxies

def writing_proxies(file, tested_proxies):
    with open(file, "w") as file :
        for row in tested_proxies:
            file.write(f"{row}\n")

def appending_proxies(file, tested_proxies):
    with open(file, "a") as file :
        for row in tested_proxies:
            file.write(f"{row}\n")

def main():
    if len(sys.argv) == 2:
        tested_proxies = []
        for proxy in reading_proxy("untested_proxies.csv"):
            if test_proxy(proxy, "https://lazada.sg/")is not None:
                tested_proxies.append(proxy)
        if sys.argv[1] == "w":
            writing_proxies("tested_proxies.csv", tested_proxies)
        else:
            appending_proxies("tested_proxies.csv", tested_proxies)

if __name__ == "__main__":
    main()