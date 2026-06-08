
import numpy as np
from typing import Any, Optional, Tuple, TypeVar, Iterable
from gymnasium import error

RandomNumberGenerator = np.random.Generator
T = TypeVar("T")

class Random:
    seed = 0
    initialized = False
    np_random = None

    @classmethod
    def initialize(cls):
        if cls.initialized:
            return

        cls.set_seed(0)
        cls.initialized = True

    @classmethod
    def set_seed(cls,seed):
        cls.seed = seed

        seed_seq = np.random.SeedSequence(seed)
        rng = RandomNumberGenerator(np.random.PCG64(seed_seq))
        cls.np_random = rng

    @classmethod
    def rand_int(cls, low: int, high: int) -> int:
        """
        Generate random integer in [low,high[
        """

        return cls.np_random.integers(low, high)

    @classmethod
    def rand_float(cls, low: float, high: float) -> float:
        """
        Generate random float in [low,high[
        """

        return cls.np_random.uniform(low, high)

    @classmethod
    def rand_bool(cls) -> bool:
        """
        Generate random boolean value
        """

        return cls.np_random.integers(0, 2) == 0

    @classmethod
    def rand_elem(cls, iterable: Iterable[T]) -> T:
        """
        Pick a random element in a list
        """

        lst = list(iterable)
        idx = cls.rand_int(0, len(lst))
        return lst[idx]

    @classmethod
    def rand_subset(cls, iterable: Iterable[T], num_elems: int) -> list[T]:
        """
        Sample a random subset of distinct elements of a list
        """

        lst = list(iterable)
        assert num_elems <= len(lst)

        out: list[T] = []

        while len(out) < num_elems:
            elem = cls.rand_elem(lst)
            lst.remove(elem)
            out.append(elem)

        return out

    # @classmethod
    # def _rand_color(cls) -> str:
    #     """
    #     Generate a random color name (string)
    #     """
    #
    #     return cls._rand_elem(COLOR_NAMES)

    @classmethod
    def rand_pos(
        cls, x_low: int, x_high: int, y_low: int, y_high: int
    ) -> tuple[int, int]:
        """
        Generate a random (x,y) position tuple
        """

        return (
            cls.np_random.integers(x_low, x_high),
            cls.np_random.integers(y_low, y_high),
        )
