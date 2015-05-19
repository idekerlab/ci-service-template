from .. import RESULT_TYPE


class JobUtil():
    @staticmethod
    def get_job_info(job):
        """
        Utility method to create job status object

        :param job: Job object
        :return: human/machine readable job status object.
        """

        result_type = job.meta[RESULT_TYPE]

        job_info = {
            'job_id': job.get_id(),
            'status': job.get_status(),
            'url_result': 'queue/' + job.get_id() + '/result',
            'result_type': result_type
        }

        return job_info

    @staticmethod
    def get_not_found_message(job_id):
        not_found = {
            'message': 'Job ' + job_id + ' does not exist.'
        }
        return not_found, 404
