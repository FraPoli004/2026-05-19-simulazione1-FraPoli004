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
            return

        self._model.buildGrafo(self._view._ddGenre.value)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.get_numnodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.get_numarchi()}"))

        artista, influenza = self._model.get_artista_piu_influente()
        self._view.txt_result.controls.append(
            ft.Text(f"Artista più influente: {artista}, con influenza: {influenza}")
        )

        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for u, v, peso in self._model.get_top5_archi():
            self._view.txt_result.controls.append(ft.Text(f"{u} -> {v} : {peso}"))

        self._view.update_page()

    def handleCammino(self,e):
        pass