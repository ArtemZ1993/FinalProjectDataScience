
import time
from selenium import webdriver
import csv
from datetime import datetime

def main():

    flag = True
    driver = webdriver.Chrome()
    driver.get("https://www.yad2.co.il/realestate/forsale?city=6600")
    time.sleep(3)
    print("*")

    page = 1
    l1 = ["חדרים","קומה",'מ"ר']
    l2 = ['מטבח כשר', 'משופצת', 'ממ"ד', 'דלתות פנדור', 'מזגן תדיראן', 'ריהוט', 'גישה לנכים', 'מיזוג', 'מעלית', 'מחסן','סורגים']
    l3 = ['חניות', 'מרפסות', 'קומות בבנין', 'מצב הנכס']

    while(True):

        try:
            all_feeditem_table = driver.find_elements_by_class_name("feeditem.table")
        except:
            try:
                all_feeditem_table = driver.find_elements_by_class_name("feeditem.table")
            except Exception as e:
                print(e,"\nwhile(True):")
                continue

        try:
            for item_feeditem_table in all_feeditem_table:

                D = {"מטבח כשר": None, "משופצת": None, 'ממ"ד': None, "דלתות פנדור": None, "מזגן תדיראן": None,
                     "ריהוט": None,
                     "גישה לנכים": None, "מיזוג": None, "מעלית": None, "מחסן": None, "סורגים": None, 'חניות': None,
                     'מרפסות': None, 'קומות בבנין': None, 'מצב הנכס': None, "סוג נכס": None, "עיר": None, "שכונה": None}

                time.sleep(2)

                try:
                    item_feeditem_table.click()
                except Exception as e:
                    print(e)
                    try:
                        item_feeditem_table.click()
                    except:
                        print(e)
                        continue


                try:
                    time.sleep(2)
                    info_feature_delete = item_feeditem_table.find_elements_by_class_name("info_feature.delete")
                    time.sleep(2)
                except:
                    pass

                try:
                    tamp1 = []
                    for i in info_feature_delete:
                        if str(i.text) in l2:
                            D[str(i.text)] = 0
                            tamp1.append(i.text)

                    info_feature = item_feeditem_table.find_elements_by_class_name("info_feature")
                    time.sleep(2)

                    for i in info_feature:
                        if str(i.text) in l2 and D.get(str(i.text)) != 0 and str(i.text) not in tamp1:
                            D[str(i.text)] = 1
                except:
                    pass


                try:
                    item_feeditem_table.find_element_by_class_name("agencyName")
                    time.sleep(2)
                    D["תיווך"] = 1
                except:
                    D["תיווך"] = 0
                    pass

                try:
                    info_items = item_feeditem_table.find_elements_by_class_name("info_item")

                    for i in info_items:
                        h = str(i.text).split("\n")
                        if h[0] in l3:
                            D[h[0]] = h[1]
                except:
                    pass

                try:
                    rating_val = item_feeditem_table.find_element_by_class_name("rating-val")
                    time.sleep(2)
                    score = str(rating_val.text)
                    D["ציון"] = score[0:3]
                except:
                    pass


                time.sleep(2)

                try:
                    subtitle = item_feeditem_table.find_element_by_class_name("subtitle")
                    string_subtitle = str(subtitle.text)
                    string_subtitle = string_subtitle.split(",")
                    D["סוג נכס"] = string_subtitle[0]
                    D["שכונה"] = string_subtitle[1:-1]
                    D["עיר"] = string_subtitle[-1]

                except:
                    pass

                try:
                    time.sleep(2)
                    y = item_feeditem_table.find_elements_by_class_name("data")
                    time.sleep(2)

                    for g in y:
                        g = str(g.text)
                        g = g.split("\n")
                        if g[1] in l1:
                            D[g[1]] = g[0]
                except:
                    pass

                time.sleep(2)
                try:
                    y = item_feeditem_table.find_element_by_class_name("price")
                    D["מחיר"] = str(y.text)
                except:
                    D["מחיר"] = None

                time.sleep(2)

                l = ['מטבח כשר','משופצת','ממ"ד','דלתות פנדור','מזגן תדיראן','ריהוט','גישה לנכים','מיזוג','מעלית','מחסן','סורגים','חניות','מרפסות','קומות בבנין','מצב הנכס','סוג נכס','עיר','שכונה','תיווך','ציון','חדרים','קומה','מ"ר','מחיר']
                O = []

                # print(l)
                # print(len(l))

                for i in l:
                    if i not in D.keys():
                        O.append(i)

                if len(O) > 0:
                    print("Missing categories: ",O)
                    for i in O:
                        D[i] = None

                if flag:
                    with open('innovators.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(D.keys())

                    flag = False

                with open('innovators.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(D.values())

        except Exception as e:
            print("Erorr in -> for")
            print(e)
            page -= 1


        print("page: {}".format(page))

        if page > 49:
            break

        page += 1
        driver.get("https://www.yad2.co.il/realestate/forsale?city=6600&page={}".format(page))

    driver.close()







if  __name__ == "__main__":
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    main()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
