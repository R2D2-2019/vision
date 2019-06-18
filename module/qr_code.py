class QrCode:
    def __init__(self, code):
        self.data = self.parse_data(code.data.decode("utf-8"))
        self.type = code.type
        self.rect = code.rect
        self.polygon = code.polygon
        self.distance = None

    def calculate_distance(self, camera_properties, frame_height):
        try:
            distance_to_object = (camera_properties.get_focal_length() * self.get_height() * frame_height) / (self.rect.height * camera_properties.get_sensor_height())
            self.distance = distance_to_object
        except ZeroDivisionError:
            return None

    def get_height(self):
        try:
            return int(self.data["Height"])
        except ValueError:
            return None

    def parse_data(self, unrefined_data):
        data_dict = dict()
        data_splits = unrefined_data.split(",")
        for data_split in data_splits:
            data = data_split.split(":")
            data_dict[data[0]] = data[1]
        return data_dict
