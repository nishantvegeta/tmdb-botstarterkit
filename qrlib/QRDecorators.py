from qrlib.QRRunItem import QRRunItem
from robot.libraries.BuiltIn import BuiltIn


def run_item_tt(post_success=True, post_error=True):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            queue_item = None
            logger_name = 'quickrpa_default_logger'
            if "queue_item" in kwargs:
                queue_item = kwargs["queue_item"]
            if "logger_name" in kwargs:
                logger_name = kwargs["logger_name"]

            run_item = QRRunItem(
                logger_name=logger_name, is_ticket=True, queue_item=queue_item)

            self.run_item = run_item
            self.notify()

            try:
                value = function(self, *args, **kwargs)
                run_item.set_success()
            except Exception as e:
                run_item.set_error()
                if (post_error):
                    run_item.post()
                raise e
            if (post_success):
                run_item.post()
            run_item.bot_logger.close_logger()
            return value
        return wrapper
    return decorator


def run_item_tf(post_success=False, post_error=True):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            logger_name = 'quickrpa_audit_logger'
            if "logger_name" in kwargs:
                logger_name = kwargs["logger_name"]
            run_item = QRRunItem(logger_name=logger_name, is_ticket=False)

            self.run_item = run_item
            self.notify()

            try:
                value = function(self, *args, **kwargs)
                run_item.set_success()
            except Exception as e:
                run_item.set_error()
                if (post_error):
                    run_item.post()
                raise e
            if (post_success):
                run_item.post()
            run_item.bot_logger.close_logger()
            return value
        return wrapper
    return decorator


def run_item(post_success=True, post_error=True, is_ticket=True):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            queue_item = None
            logger_name = 'quickrpa_default_logger'
            if "queue_item" in kwargs:
                queue_item = kwargs["queue_item"]
            if "logger_name" in kwargs:
                logger_name = kwargs["logger_name"]

            run_item = QRRunItem(
                logger_name=logger_name, is_ticket=is_ticket, queue_item=queue_item)

            self.run_item = run_item
            self.notify()

            try:
                value = function(self, *args, **kwargs)
                run_item.set_success()
            except Exception as e:
                run_item.set_error()
                if (post_error):
                    run_item.post()
                raise e

            if (post_success):
                run_item.post()

            run_item.bot_logger.close_logger()
            return value
        return wrapper
    return decorator
