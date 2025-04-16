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


# def post_forever(controllers: list[RequestController]) -> None:
#     logger_adapter = logging.LoggerAdapter(logger, {"prefix": "scheduler"})
#     with ThreadPoolExecutor(max_workers=len(controllers)) as executor:
#         future_map: dict[Future, RequestController] = {
#             executor.submit(controller.run): controller for controller in controllers
#         }

#         try:
#             while True:
#                 for future in as_completed(future_map):
#                     controller = future_map.pop(future)
#                     logger_adapter.info(f"Future completed for {controller.poster}")
#                     try:
#                         future.result()
#                     except Exception as exc:
#                         logger_adapter.error(
#                             f"Error occured for {controller.poster}: {exc}",
#                             exc_info=exc,
#                             stack_info=True,
#                         )

#                     logger_adapter.info(
#                         f"Finished task for {controller.poster}, running new task"
#                     )
#                     new_future = executor.submit(controller.run)
#                     future_map[new_future] = controller
#                     logger_adapter.info(f"Task re-submitted for {controller.poster}")

#         except KeyboardInterrupt:
#             logger_adapter.info("KeyboardInterrupt received, shutting down..")

#         except Exception as exc:
#             logger_adapter.error(
#                 "Received unexpected exception in main thread",
#                 exc_info=exc,
#                 stack_info=True,
#             )

#         finally:
#             logger_adapter.info("Calling shutdown on executor..")
#             executor.shutdown(wait=False, cancel_futures=True)
#             logger_adapter.info("Executor has been shut down.")
