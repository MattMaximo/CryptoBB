from functools import wraps

# Initialize an empty WIDGETS dictionary here instead of importing from widgets.py
WIDGETS = {}

def register_widget(widget_config):
    """
    Decorator that registers a widget configuration in the WIDGETS dictionary.
    
    Args:
        widget_config (dict): The widget configuration to add to the WIDGETS 
            dictionary. This should follow the same structure as other entries 
            in WIDGETS.
    
    Returns:
        function: The decorated function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Call the original function
            return await func(*args, **kwargs)
        
        # Extract the endpoint from the widget_config
        endpoint = widget_config.get("endpoint")
        if endpoint:
            # Add the widget configuration to the WIDGETS dictionary
            WIDGETS[endpoint.replace("/", "_")] = widget_config
        
        return wrapper
    return decorator 