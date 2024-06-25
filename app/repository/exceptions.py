class ModelNotFoundException(Exception):
    def __init__(self):
        super().__init__('Model not found')
