import json
import validators
import pycountry
import re
import awoc

my_world = awoc.AWOC()
continents_data = my_world.get_continents()

def get_test_data(filter_key, filter_value):
    with open('../elastic_data.json', 'r') as file:
        data = json.load(file)
        raw_data_set = data["hits"]["hits"]
        test_data_set = []
        for test_data in raw_data_set:
            value = test_data["_source"].get(filter_key)
            if value == filter_value:
                test_data_set.append(test_data)            
        return test_data_set


class schema_validation():
    def __init__(self):
        self.key_list = []
        with open("template.json", 'r') as f:
            self.tmplate_dict=json.load(f)

    def compare_fun(self, template_data, test_data, compare_type_value):
        """
        :param compare_type_value:if True, compare value, False comapres type
        :param compare_type_value:
        :return: True/False
        """
        if compare_type_value is True:
            if template_data == test_data:
                return True
            else:
                return False, f'the value is different: {template_data}'
        else:
            if type(template_data) == type(test_data):
                return True
            else:
                return False, f'the type is different:{type(template_data)}'

    def compare_item_fun(self, key, template_item, test_item, compare_type_value):
        if test_item == 'key_is_not_exists_!!!':
            return False, f'key:{key} key_is_not_exists!!!'
        elif type(template_item) != type(test_item):
            return False, f'the type is wrong for the value of{key}, {type(template_item)}, {type(test_item)}'
        elif isinstance(template_item, dict):
            result = self.assert_dict(template_item, test_item, compare_type_value, tag=key)
            if result[0] is False:
                return result
        elif isinstance(template_item, list) or isinstance(template_item, tuple):
            if len(template_item) > len(test_item):
                return False, f'the length of value for {key}is less than template'
            for tmp_ii, data_ii,index in zip(template_item, test_item,range(len(template_item))):
                self.key_list[-1].append(str([index]))
                result = self.compare_item_fun(index, tmp_ii, data_ii, compare_type_value)
                if result[0] is False:
                    return result
        else:
            result = self.compare_fun(template_item, test_item, compare_type_value)
            if result[0] is False:
                return result
        if self.key_list[-1]:
            self.key_list[-1].pop()
        return True

    def assert_dict(self, tmplate_dict, data_dict, compare_type_value, tag=None):
        """
        :param tmplate_dict:
        :param data_dict:
        :param compare_type_value:
        :param tag: recursion tag, None for not use recursion
        :return: True/False
        """

        for k, template_data in tmplate_dict.items():
            if tag is None:
                self.key_list.append([str([k])])
            else:
                self.key_list[-1].append(str([k]))
                test_data = data_dict.get(k, 'key_is_not_exists_!!!')
                result = self.compare_item_fun(k, template_data, test_data, compare_type_value)
                if result[0] is False:
                    print(k)
                if tag is None:
                    self.key_list.pop()
        else:
            result = True, 'success'
        return result

    def compare(self, data_dict, compare_type_value=False):
        result, msg = self.assert_dict(self.tmplate_dict, data_dict, compare_type_value)
        if result is True:
            return result
        else:
            key_str = "".join(self.key_list[-1])
            self.key_list.clear()
            return result, f'the key is:{key_str}, {msg}'


def filed_validation(test_data):
    #country iso code.
    country_iso_code = test_data["geoip"]["country_iso_code"]
    assert pycountry.countries.get(alpha_2=country_iso_code) is not None

    #continents name 
    continent_name = test_data["geoip"]["continent_name"]
    continents = [i.get("Continent Name") for i in continents_data]
    assert continent_name in continents



    

    
            