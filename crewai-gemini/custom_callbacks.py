from litellm.integrations.custom_logger import CustomLogger
from yaml import dump
import litellm

class MyCustomHandler(CustomLogger):
    def log_pre_api_call(self, model, messages, kwargs): 
        print("========================================")
        print("Request")
        print(dump(messages))
        print("----------------------------------------")
    
    async def async_log_success_event(self, kwargs, response_obj, start_time, end_time):
        print("----------------------------------------")
        print("Response")
        print(dump(response_obj["choices"][0]["message"]["content"]))
        print("========================================")

proxy_handler_instance = MyCustomHandler()