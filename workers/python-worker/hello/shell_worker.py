import subprocess
from ciworker.base_worker import BaseWorker


class ShellWorker(BaseWorker):
    """
    Sample worker to call external shell script.
    """

    def run(self, data):

        # Extract query gene ID from the 'data' dict
        gene_id = data['gene_id']

        # Run a shell script
        out = subprocess.check_output(['./mitab_util.sh', gene_id],
                                        stderr=subprocess.STDOUT,
                                      universal_newlines=True)

        return out
