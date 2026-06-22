import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        generi = self._model.get_all_generi()  # 👈 CAMBIA: metodo del Model
        for g in generi:
            self._view._ddGenre.options.append(  # 👈 CAMBIA: nome dropdown
                ft.dropdown.Option(key=g.GenreId, text=g.Name)
            )
        self._view.update_page()



    def handleCreaGrafo(self,e):
        pass

    def handleCreaGrafo(self, e):
        if self._view._ddGenre.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserisci un genere.", color="red"))
            self._view.update_page()
        else:
            self._model.buildGrafo(self._view._ddGenre.value)
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
            self._view.txt_result.controls.append(ft.Text(f"Il grafo è costituito da {self._model.get_numnodi()} nodi."))
            self._view.txt_result.controls.append(ft.Text(f"Il grafo è costituito da {self._model.get_numarchi()} archi."))
            self._view.update_page()

    def handleCammino(self,e):
        pass