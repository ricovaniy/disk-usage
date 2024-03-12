import unittest
from datetime import datetime
from diskanalyser import DiskAnalyser


class TestTest(unittest.TestCase):
    def test_calculator(self):
        self.assertEqual(6, len(DiskAnalyser.count_files("test folder")[1]))
        self.assertEqual(3, len(DiskAnalyser.count_files("test folder/next folder")[1]))

    def test_calc_nested(self):
        self.assertEqual(2, DiskAnalyser.calc_nested_level('test folder/next folder/second_level.txt'))
        self.assertEqual(1, DiskAnalyser.calc_nested_level('test folder/first_level.txt'))

    def test_calc_with_max_size_filter(self):
        analyser = DiskAnalyser(max_size = 20)
        self.assertEqual(16, analyser.calc_with_filters('test folder'))

    def test_calc_with_min_size_filter(self):
        analyser = DiskAnalyser(min_size = 20)
        self.assertEqual(47714, analyser.calc_with_filters('test folder'))

    def test_calc_with_extension_filter(self):
        analyser = DiskAnalyser(extension = '.txt')
        self.assertEqual(16, analyser.calc_with_filters('test folder'))
        analyser = DiskAnalyser(extension = '.docx')
        self.assertEqual(47714, analyser.calc_with_filters('test folder'))

    def test_calc_with_date_filter(self):
        analyser = DiskAnalyser(date = datetime.strptime("14-10-2023", "%d-%m-%Y"))
        self.assertEqual(16, analyser.calc_with_filters('test folder'))
        analyser = DiskAnalyser(date = datetime.strptime("14-03-2023", "%d-%m-%Y"))
        self.assertEqual(47714, analyser.calc_with_filters('test folder'))

    def test_calc_with_nested_level_filter(self):
        analyser = DiskAnalyser(nested_level = 2)
        self.assertEqual(33982, analyser.calc_with_filters('test folder'))
        analyser = DiskAnalyser(nested_level = 1)
        self.assertEqual(13748, analyser.calc_with_filters('test folder'))

    def test_calc_with_multi_filter(self):
        analyser = DiskAnalyser(nested_level = 2, date = datetime.strptime('14-10-2023', "%d-%m-%Y"))
        self.assertEqual(8, analyser.calc_with_filters('test folder'))
        analyser = DiskAnalyser(nested_level = 1, min_size = 300, extension = '.docx')
        self.assertEqual(13740, analyser.calc_with_filters('test folder'))


if __name__ == "__main__":
    unittest.main()
