import time

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selected_year = None
        self._selected_shape = None
        self._selected_citta = None

    def fillDDShapes(self):
        shapes = self._model._shapes
        for s in shapes:
            self._view._DD_shape.options.append(ft.dropdown.Option(data=s, text=s, on_click=self._choice_shape))
        self._view.update_page()

    def fillDDAnno(self):
        years = self._model._years
        for y in years:
            self._view._DD_anno.options.append(ft.dropdown.Option(data=y, text=y, on_click=self._choice_year))
        self._view.update_page()

    def _choice_shape(self, e):
        if e.control.data is None:
            self._selected_shape = None
        else:
            self._selected_shape = e.control.data

    def _choice_year(self, e):
        if e.control.data is None:
            self._selected_year = None
        else:
            self._selected_year = e.control.data

    def handleGrafo(self, e):
        if self._selected_year != None and self._selected_shape != None:
            self._model._crea_grafo(self._selected_shape, self._selected_year)
            nNodi, nArchi = self._model.get_dettagli_grafo()
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(ft.Text(f"Grafo correttamente creato.\n"
                                                           f"Il grafo ha {nNodi} vertici e {nArchi} spigoli."))
            top_5 = self._model.get_top_citta_adiacenti()
            self._view.txt_result1.controls.append(ft.Text(f"Top 5 vertici con peso maggiore:"))
            for t in top_5:
                self._view.txt_result1.controls.append(ft.Text(f"{t[0]}, peso: {t[1]}"))
            self._view._DD_citta_partenza.disabled = False
            self._view._txtIn_max_distanza.disabled = False
            self._view._btn_percorso.disabled = False
            self._view._txtIn_min_citta.disabled = False
            self._fillDD_citta_partenza()
        else:
            self._view.txt_result1.controls.append(ft.Text(f"Errore, selezionare 'Anno' e 'Forma'."))
            self._view.update_page()
            return

        self._view.update_page()

    def _fillDD_citta_partenza(self):
        citta = self._model._nodes
        for c in citta:
            self._view._DD_citta_partenza.options.append(ft.dropdown.Option(data=c, text=c, on_click=self._choice_citta))
        self._view.update_page()

    def _choice_citta(self, e):
        if e.control.data is None:
            self._selected_citta = None
        else:
            self._selected_citta = e.control.data

    def handlePercorso(self, e):
        max_distanza = self._view._txtIn_max_distanza.value
        min_num_citta = self._view._txtIn_min_citta.value
        try:
            int_max_distanza = int(max_distanza)
            int_min_num_citta = int(min_num_citta)
        except ValueError:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(ft.Text(f"Errore, inserire dei valori interi in 'Max distanza' e 'Min num città'."))
            self._view.update_page()
            return
        percorso, distanza, num_citta = self._model._handle_path(self._selected_citta, int_max_distanza, int_min_num_citta)
        self._view.txt_result2.controls.clear()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato percorso di distanza (somma peso archi) = {distanza} "
                                                       f"di che attraversa {num_citta} città."))
        for p in percorso:
            self._view.txt_result2.controls.append(ft.Text(f"{p[0]} --> {p[1]}, peso {p[2]}"))
        self._view.update_page()


