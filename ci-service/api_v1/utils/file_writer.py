import os
import json

RESULT_DIR = 'results'


class FileUtil():

    def __init__(self):
        self.APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top

    def create_result(self, file_id, data):
        filename = os.path.join(self.APP_ROOT, RESULT_DIR + '/' + str(file_id))

        temp_file = open(filename, 'w')
        json.dump(data, temp_file)
        temp_file.close()

        result = {
            'file': str(file_id)
        }

        return result

    def get_result_file_location(self, file_id):
        return os.path.join(self.APP_ROOT, RESULT_DIR + '/' + str(file_id))



