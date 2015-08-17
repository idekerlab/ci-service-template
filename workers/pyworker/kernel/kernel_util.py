
class KernelUtil:

    def kernel_multiply_one(self, vector, kernel, labels):
        """
            Multiply the specified kernel by the supplied input heat vector.

            Input:
                vector: A hash mapping gene labels to floating point values
                kernel: a single index for a specific kernel

            Returns:
                A hash of diffused heats, indexed by the same names as the
                input vector
        """

        # Have to convert to ordered array format for the input vector
        # TODO: Use NumPy array?
        array1 = []
        for label in labels:
            # Input heats may not actually be in the network.
            # Check and initialize to zero if not
            if label in vector:
                array1.append(vector[label])
            else:
                array1.append(0)

        # take the dot product
        value = kernel * array1

        # Convert back to a hash and return diffused heats
        return_vec = {}
        idx = 0
        for label in labels:
            return_vec[label] = float(value[idx])
            idx += 1

        return return_vec
