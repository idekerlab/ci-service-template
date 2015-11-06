import subprocess

from ciworker.base_worker import BaseWorker


class ShellWorker(BaseWorker):

    def run(self, data):
        """
        Actual service call.

        :param data: dictionary of message.  It should have
         'message' as the key.
        :return:
        """

        cmd = 'curl -l ' \
              '"http://www.ebi.ac.uk/Tools/webservices/psicquic/intact/webservices/current/search/interactor/brca2_human?format=tab27"' \
              ' | csvcut -t -c 1,2 | head'
        ret  =  subprocess.call( ['./mitab_util.sh'], stderr=subprocess.STDOUT )
        p = subprocess.Popen("./mitab_util.sh", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()

        # Return result as object
        return str(output).split('\n')