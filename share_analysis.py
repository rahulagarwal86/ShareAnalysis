import csv
import os
from collections import OrderedDict
import unittest


#Function to find max share price for each company with year and month details
def get_share_data(file_path=None):
    if not file_path:
        file_path = raw_input("\nEnter your file path: ")
        #File Validation Check
        #1. Check if file exist
        #2. Check the format of file
        try:
            fo = open(file_path,"r",1)
        except IOError:
            print "No such file or directory"
        extension = os.path.splitext(file_path)[1]
        if extension != '.csv':
            print 'Incorrect File format'
            exit(0)

    #Performing operation over file to get highest share value for each company.
    with open(file_path, 'rb') as csv_file:
        data_file = csv.reader(csv_file)
        data_dict = OrderedDict()
        company_names = next(data_file)[2:]
        for name in company_names:
            data_dict[name] = {'price': 0, 'year': 'year', 'month': 'month'}
        for row in data_file:
            year, month = row[:2]
            for name, price in zip(company_names, map(int, row[2:])):
                if data_dict[name]['price'] < price:
                    data_dict[name] = {'price': price, 'year': year, 'month': month}

    #Print the desired result
    result =  '\nCompany Name\tYear\tMonth\tMax.Price\n\n'
    for company_name, analysis_dict in data_dict.items():
        result += '%s\t\t%s\t%s\t%d\n' % (company_name, analysis_dict['year'], analysis_dict['month'], analysis_dict['price'])
    return result


if __name__ == "__main__":
    print get_share_data()