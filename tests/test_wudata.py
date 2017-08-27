from src.weather_updates.wu_data import WU

class WU_Test:
    def __init__():
        self.wu = WU()

    def test_astronomy_response(self):
        response = self.wu.get_astronomy().status_code
        assert response >= 200
        assert response < 300
