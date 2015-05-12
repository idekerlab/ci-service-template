import os
import json

RESULT_DIR = 'results'

# Flask root directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top


class FileUtil():
    """
    Utility to generate results
    """

    @staticmethod
    def create_result(file_id, data):
        filename = os.path.join(APP_ROOT, RESULT_DIR + '/' + str(file_id))

        temp_file = open(filename, 'w')
        json.dump(data, temp_file)
        temp_file.close()

        result = {
            'file': str(file_id)
        }

        return result

    @staticmethod
    def get_result_file_location(file_id):
        return os.path.join(APP_ROOT, RESULT_DIR + '/' + str(file_id))
