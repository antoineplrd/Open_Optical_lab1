class Line:

    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = dict()

    @staticmethod
    def latency_generation():
        SpeedLight = 299792458
        latency_result = 2 / 3 * SpeedLight

        return latency_result

    def noise_generation(self, signal_power):
        return 0.00000001 * signal_power * self._length

    def propagate(self, signal_information):
        noise_power = self.noise_generation(signal_information.signal_power)
        latency = self.latency_generation()
        path = signal_information.path
        next_node = path[0]
        next_node_instance = self._successive[next_node]
        signal_information.update_noise_power(noise_power)
        signal_information.UpdateLatency(latency)
        next_node_instance.propagate(signal_information)
