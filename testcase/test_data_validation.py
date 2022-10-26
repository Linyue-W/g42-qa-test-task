import pytest
from utils import schema_validation, get_test_data, filed_validation

class TestDataValidation:

    @pytest.mark.parametrize("test_data", get_test_data("customer_gender", "MALE"))
    def test_data_validation_by_group(self, test_data):
      # schema validation test
      schema = schema_validation().compare(test_data["_source"])
      assert schema is True
      
      #specific filed value validation test
      filed_validation(test_data["_source"])

      



    
