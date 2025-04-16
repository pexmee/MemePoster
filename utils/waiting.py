import logging
import random
from datetime import datetime, time, timedelta
from time import sleep
from typing import Protocol

logger = logging.getLogger("pansophical_memes")


class Waiter(Protocol):
    def wait_for_window(self) -> None: ...
    def wait(self, seconds: float, interval: int) -> None: ...


class PlatformWaiter:
    def __init__(self, platform_name: str) -> None:
        self.logger = logging.LoggerAdapter(logger, {"prefix": platform_name})

    def wait_for_window(self) -> None:
        pass

    def wait(self, seconds: float, logging_interval: int) -> None:
        quotient, remainder = divmod(seconds, logging_interval)
        for i in range(logging_interval):
            self.logger.info(f"{(seconds-(i*quotient))+remainder} seconds left to wait")
            sleep(quotient)

        sleep(remainder)
        self.logger.debug(f"Done waiting")


class WindowWaiter(PlatformWaiter):
    def __init__(self, platform_name: str) -> None:
        super().__init__(platform_name)
        self._set_post_window()

    def _set_post_window(self) -> None:
        self.start_time = time(random.randint(8, 10), random.randint(1, 59))
        self.end_time = time(random.randint(21, 22), random.randint(1, 59))

    def _seconds_until_posting_window(self) -> float:
        now = datetime.now()
        current_time = now.time()

        if self.start_time <= current_time <= self.end_time:
            return 0

        if current_time < self.start_time:
            next_start = now.replace(
                hour=self.start_time.hour,
                minute=self.start_time.minute,
                second=0,
                microsecond=0,
            )
        else:
            # current_time > end_time
            next_start = (now + timedelta(days=1)).replace(
                hour=self.start_time.hour,
                minute=self.start_time.minute,
                second=0,
                microsecond=0,
            )

        time_difference = next_start - now
        seconds_left = time_difference.total_seconds()
        self.logger.info(
            f"{seconds_left} until posting window {self.start_time.isoformat()} -> {self.end_time.isoformat()}"
        )
        return seconds_left

    def wait_for_window(self) -> None:
        seconds_left = self._seconds_until_posting_window()
        if seconds_left > 0:
            self.wait(seconds_left, 100)
            # New window for the next round because we want to have random posting windows every day
            # The memes are kept in memory anyway until it's allowed to post.
            self._set_post_window()

        else:
            self.logger.info(
                f"We are within the posting window {self.start_time.isoformat()} -> {self.end_time.isoformat()}"
            )
