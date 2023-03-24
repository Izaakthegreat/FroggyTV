from froggytv.bpm import Bpm
from froggytv.triggers import Noop


class CountingTriggerable():
    def __init__(self):
        self.count = 0

    def trigger(self, _tick):
        self.count += 1


class ImmediateBPM():
    def __init__(self, resolution=Bpm.DEFAULT_RESOLUTION):
        self.resolution = resolution
        self._tick = 0

    def update(self, _now, triggerable=Noop()):
        self._tick += 1
        if self._tick == self.resolution:
            self._tick = 0

        triggerable.trigger(self._tick)
