from ursina import *

from ursina.prefabs.dropdown_menu import DropdownMenu
from ursina.prefabs.dropdown_menu import DropdownMenuButton as MenuButton

DropdownMenu(
    name = 'file',
    content = (
        MenuButton('New'),
        MenuButton('Open'),
        MenuButton('Save'),
        MenuButton('Save as...'),
        MenuButton('Save as...'),
        MenuButton('Exit', on_click='application.quit'),
        )
)
if __name__ == '__main__':
    app = Ursina()

    app.run()
