from sys import exit

recietlist = list()
price_dict = dict()
order_dict = dict()
productname_dict = dict()


def parseproductline(productline, column):
    columns = productline.split("\t")
    return columns[column - 1]


def parseproductfile():
    with open("products.txt", "r") as parsefile:
        for line in parsefile:
            line = line.replace("\n", "")
            productcode = parseproductline(line, 1)
            productname = parseproductline(line, 2)
            productprice = parseproductline(line, 3)
            if productcode != "GTIN - 8":
                price_dict[productcode] = float(productprice)
            productname_dict[productcode] = productname


def final_write(stocknumber, ordernumber, code):
    f = open("stockfile.txt", "r+")
    d = f.readlines()
    f.seek(0)
    for i in d:
        if i != str(code) + "    " + str(int(stocknumber) + ordernumber) + "\n":
            f.write(i)
    f.truncate()
    f.close()
    with open("stockfile.txt", "a") as myfile:
        myfile.write(str(code) + "    " + str(stocknumber) + "\n")


def reciet(productname, ordernumber, printatend):
    if printatend is True:

        total = 0
        for code in order_dict.keys():
            print(code + "    " + productname_dict[code] + "    £" +
                  str(price_dict[code]) + "    " + str(order_dict[code]))
            total += price_dict[code] * order_dict[code]
        print("Total: £ " + str(total))


def should_continue(carryon):
    if carryon == "Y" or carryon == "y":
        reciet(productname, ordernumber, False)
        return True

    else:
        print("---------------RECIET---------------")
        reciet(productname, ordernumber, True)
        exit()


parseproductfile()
while True:
    while True:
        code = input("Please enter your GTIN-8 tag:")

        codelist = list(code)
        if len(codelist) != 8:
            print("Your tag has to be 8 digits long")

        times = 0
        for x in range(0, 7, 1):
            if x % 2 == 0:
                times += (3 * int(codelist[x]))
            else:
                times += (1 * int(codelist[x]))

        print("The sum of the first 7 digits is " + str(times))
        finalnum = (10-(times % 10)) % 10
        print("The check digit of this tag should be " + str(finalnum))

        if int(codelist[7]) == finalnum:
            print("This GTIN-8 tag is valid.")
            with open('products.txt', 'r') as searchfile:
                for line in searchfile:
                    if code in line:
                        print("GTIN-8            Product       Price")
                        productname = line
                        print(productname)

                        with open('stockfile.txt', 'r') as searchfile:
                            for line in searchfile:
                                if code in line:
                                    stocknumber = line[12:]
                                    print("Amount of " + code + " in stock: " + stocknumber)
                                    whattodo = input("What would you like to do with the stock? order / restock: ")

                                    if whattodo == "order":
                                            ordernumber = int(input("How many would you like to order? :"))
                                            stocknumber = int(stocknumber) - ordernumber
                                            print("You have " + str(stocknumber) + " left in sotck")

                                            final_write(stocknumber, ordernumber, code)
                                            if code in order_dict:
                                                ordernumber += order_dict[code]
                                            order_dict[code] = ordernumber

                                            should_continue(input("Would you like to order more items? Y/N: "))

                                    elif whattodo == "restock":
                                        ordernumber = input("How many would you like to restock? :")
                                        stocknumber = int(stocknumber) + int(ordernumber)
                                        print("You have " + str(stocknumber) + " left in sotck")
                                        final_write(stocknumber, -1*int(ordernumber), code)
                                        should_continue(input("Would you like to order more items? Y/N: "))
                                    else:
                                        print("We dont recognise that")
                                        should_continue(input("Would you like to order more items? Y/N: "))
        continue
    else:
        print("This GTIN-8 tag is invalid.")
        continue
