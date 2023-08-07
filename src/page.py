
class Page:

    def __init__(self) -> None:
        self.current_page = 'home'
    
    def change_page(self, to_page):
        self.current_page = to_page