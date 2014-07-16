import unittest
import random
import os
import csv
import share_analysis


# Best way to test is have 'Randomize' file for testcases
class RandomCSVFile(unittest.TestCase):
    """ Base class to generate Randomized csv test file """

    def setUp(self):
        self.start_year = random.randint(1990, 2000)  #Random Start Year
        self.end_year = random.randint(2001, 2013)  #Random End Year
        self.years = range(self.start_year, self.end_year)
        self.months = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.share_values = range(100, 1000)
        self.no_companies = random.randint(1, 10)  #Random Company Number
        self.no_entries = (self.end_year - self.start_year) * 12
        self.csv_header = ['Year', 'Month']
        self.test_dict = {}

        # Construct the data of CSV file
        for i in range(self.no_companies):
            self.csv_header.append('Comp%s' % str(i + 1))
            self.test_dict['Comp%s' % str(i + 1)] = {'price': 0, 'year': 'year', 'month': 'month'}
        with open('test.csv', 'wb') as data_file:
            data_writer = csv.writer(data_file, csv.excel)
            data_writer.writerow(self.csv_header)

            year = self.start_year
            while year <= self.end_year:
                for i in self.months:
                    data_row = [year, i]
                    for j in range(self.no_companies):
                        share_val = random.choice(self.share_values)
                        data_row.append(share_val)
                        if self.test_dict['Comp%s' % str(j + 1)]['price'] < share_val:
                            self.test_dict['Comp%s' % str(j + 1)] = {'price': share_val, 'year': year, 'month': i}
                    data_writer.writerow(data_row)
                year += 1

        self.csv_rand_input = 'test.csv'


class BadCSVExtension(RandomCSVFile):
    #Test case to test File extension Type
    def test_file_type(self):
        extension = os.path.splitext(self.csv_rand_input)[1]
        self.assertEqual(extension, '.csv')


class ValidateResult(RandomCSVFile):
    #Test Output Result for each Company
    def test_results(self):
        ret_val = share_analysis.get_share_data(self.csv_rand_input)
        for company_info in ret_val.split('\n')[1:]:
            if company_info:
                company_name, year, month, price = company_info.split('\t')
                self.assertEqual(str(year), str(self.test_dict[company_name]['year']))
                self.assertEqual(str(month), str(self.test_dict[company_name]['month']))
                self.assertEqual(str(price), str(self.test_dict[company_name]['price']))

    #Test All Companies listed in Output
    def test_all_companies(self):
        ret_val = share_analysis.get_share_data(self.csv_rand_input)
        self.assertTrue(not 'Critical' in ret_val)
        for key in self.test_dict:
            self.assertTrue(key in ret_val)


if __name__ == "__main__":
    unittest.main()