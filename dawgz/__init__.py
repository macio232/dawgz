r"""Directed Acyclic Workflow Graph Scheduling"""

__version__ = '0.1.8'


from functools import partial
from typing import Callable, Union

from .schedulers import schedule
from .workflow import Job, leafs


def job(f: Callable = None, /, **kwargs) -> Union[Callable, Job]:
    if f is None:
        return partial(job, **kwargs)
    else:
        return Job(f, **kwargs)


def after(*deps, status: str = 'success') -> Callable:
    def decorator(self: Job) -> Job:
        self.after(*deps, status=status)
        return self

    return decorator


def waitfor(mode: str) -> Callable:
    def decorator(self: Job) -> Job:
        self.waitfor = mode
        return self

    return decorator


def ensure(condition: Callable, when: str = 'after') -> Callable:
    def decorator(self: Job) -> Job:
        self.ensure(condition, when)
        return self

    return decorator


def empty(self: Job) -> Job:
    self.f = None
    return self
