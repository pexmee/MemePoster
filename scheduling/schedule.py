import logging
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from contextlib import suppress

from interface.control import RequestController
from utils.logs import setup_logger

logger = setup_logger()


class Scheduler:
    def __init__(self, controllers: list[RequestController]):
        self.controllers = controllers
        self.logger = logging.LoggerAdapter(logger, {"prefix": "scheduler"})

    def start(self) -> None:
        with ThreadPoolExecutor(max_workers=len(self.controllers)) as executor:
            futures: dict[Future, RequestController] = {
                executor.submit(controller.run): controller
                for controller in self.controllers
            }
            try:
                while True:
                    for future in as_completed(futures):
                        controller = futures.pop(future)
                        self.logger.info(f"Task completed for {controller}")
                        with suppress(Exception):
                            future.result()
                        futures[executor.submit(controller.run)] = controller

            except KeyboardInterrupt:
                self.logger.info("Shutting down due to KeyboardInterrupt")
                executor.shutdown(wait=False, cancel_futures=True)
                self.logger.info("Executor shut down")
