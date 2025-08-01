from pytest import mark


@mark.cities_data
class TestCitiesData:
    
    def test_placeholder(
            self,
            _cities,
        ) -> None:
        assert True
