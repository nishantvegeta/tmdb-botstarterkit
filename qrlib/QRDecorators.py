from QRRunItem import QRRunItem

def run_item_tt(post_success=True, post_error=True):
    def decorator(function):
        def wrapper(self, *args, **kwargs):
            queue = None
            queue_item = None
            logger_name = 'quickrpa_default_logger'
            if "queue" in kwargs:
                queue = kwargs["queue"]
            if "queue_item" in kwargs:
                queue_item = kwargs["queue_item"]
            if "logger_name" in kwargs:
                logger_name = kwargs["logger_name"]

            run_item= QRRunItem(logger_name=logger_name, is_ticket=True, queue=queue, queue_item=queue_item)
            
            self.run_item = run_item
            self.update_component_run_item()
            
            kwargs['run_item'] = run_item
            
            try:
                value = function(self, *args, **kwargs)
                run_item.success()
            except Exception as e:
                run_item.error()
                if(post_error):
                    run_item.post()
                raise e
            if(post_success):
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
            run_item= QRRunItem(logger_name=logger_name, is_ticket=False)

            self.run_item = run_item
            self.update_component_run_item()

            kwargs['run_item'] = run_item
            try:
                value = function(self, *args, **kwargs)
                run_item.success()
            except Exception as e:
                run_item.error()
                if(post_error):
                    run_item.post()
                raise e
            if(post_success):
                run_item.post()
            run_item.bot_logger.close_logger()
            return value
        return wrapper
    return decorator