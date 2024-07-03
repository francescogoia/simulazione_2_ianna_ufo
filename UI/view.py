import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # button for the "hello" reply
        self._title = ft.Text("UFO Sighting", color="blue", size=24)
        self._page.controls.append(self._title)


        # row1
        self._DD_shape = ft.Dropdown(label="Shape")
        self._DD_anno = ft.Dropdown(label="Anno")
        self._controller.fillDDShapes()
        self._controller.fillDDAnno()
        self._btn_grafo = ft.ElevatedButton(text="Grafo", on_click=self._controller.handleGrafo)
        row1 = ft.Row([ft.Container(self._DD_shape, width=300), ft.Container(self._DD_anno, width=300), ft.Container(self._btn_grafo, width=150)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)
        self.txt_result1 = ft.ListView(expand=1, spacing=10, padding=20)
        self._page.controls.append(self.txt_result1)

        self._DD_citta_partenza = ft.Dropdown(label="Città partenza", disabled=True)
        self._txtIn_max_distanza = ft.TextField(label="Max distanza", disabled=True)
        self._txtIn_min_citta = ft.TextField(label="Min numero città", disabled=True)
        self._btn_percorso = ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handlePercorso, disabled=True)
        row2 = ft.Row([ft.Container(self._DD_citta_partenza, width=300), ft.Container(self._txtIn_max_distanza, width=150),
                       ft.Container(self._txtIn_min_citta, width=150),
                       ft.Container(self._btn_percorso, width=150)], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.txt_result2 = ft.ListView(expand=1, spacing=10, padding=20)
        self._page.controls.append(self.txt_result2)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
