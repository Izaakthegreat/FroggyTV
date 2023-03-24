from froggytv.triggers import Noop, Periodic
import pytest


class CountingTriggerable():
    def __init__(self):
        self.count = 0

    def trigger(self, _tick):
        self.count += 1


class TestNoop:
    def test_noop_does_nothing(self):
        assert Noop().trigger(0) is None


class TestPeriodic:
    @pytest.fixture
    def triggerable(self):
        return CountingTriggerable()

    @pytest.mark.parametrize("resolution, mult, trigger_count, expected", [
        (24, 1, 0, 0),
        (24, 1, 24, 1),
        (24, 1, 25, 2),
        (24, 2, 24, 2),
        (24, 2, 25, 3),
        (24, 2, 36, 3),
        (24, 2, 37, 4),
        (24, 0.5, 48, 1),
        (24, 0.5, 49, 2),
    ])
    def test_periodic(
        self,
        triggerable,
        resolution,
        mult,
        trigger_count,
        expected
    ):
        periodic = Periodic(resolution, triggerable, mult=mult)
        tick = 0

        for _ in range(trigger_count):
            periodic.trigger(tick)
            tick += 1
            if tick == resolution:
                tick = 0

        assert triggerable.count == expected
