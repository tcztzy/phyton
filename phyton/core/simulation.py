"""
Simulation for phyton
"""

import datetime
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass
class DailyState:
    """Daily state for phyton"""

    date: datetime.date
    evaluated: bool = False

    def evaluate(self):
        """Evaluate the daily state"""
        self.evaluated = True


def date_index(item: Any) -> datetime.date:
    """Covert item to index

    :param item: item to be converted
    :return: date
    """
    if isinstance(item, datetime.date):
        return item
    if isinstance(item, str):
        return datetime.date.fromisoformat(item)
    raise TypeError(f"indices must be ISO format str or date, not {type(item)}")


def timedelta_step(step: Any) -> datetime.timedelta:
    """Covert step to timedelta
    :param step: step to be converted
    :return: timedelta
    """
    if isinstance(step, datetime.timedelta):
        return step
    if isinstance(step, int):
        return datetime.timedelta(days=step)
    raise TypeError(f"step must be integers or timedelta, not {type(step)}")


@dataclass
class Simulation:
    """Simulation for phyton"""

    start_date: datetime.date
    stop_date: datetime.date
    states: list[DailyState] = field(default_factory=list)

    def __post_init__(self):
        if self.stop_date < self.start_date:
            raise ValueError
        self.states.append(DailyState(self.start_date))

    def run(self):
        """Run the simulation"""
        for state in self:
            state.evaluate()
            if len(self.states) <= (self.stop_date - self.start_date).days:
                next_state = deepcopy(state)
                next_state.date += datetime.timedelta(days=1)
                next_state.evaluated = False
                self.states.append(next_state)

    def __getitem__(
        self, item: Union[datetime.date, str, slice]
    ) -> Optional[Union[DailyState, list[DailyState]]]:
        if isinstance(item, slice):
            start = (
                (date_index(item.start) - self.start_date).days
                if item.start is not None
                else None
            )
            stop = (
                (date_index(item.stop) - self.start_date).days
                if item.stop is not None
                else None
            )
            step = timedelta_step(item.step).days if item.step is not None else None
            return self.states[start:stop:step]
        index = date_index(item)
        if index < self.start_date or index > self.stop_date:
            raise IndexError("Simulation index out of range")
        try:
            return self.states[(index - self.start_date).days]
        except IndexError:
            return None

    def __iter__(self):
        return iter(self.states)
