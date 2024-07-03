from model.model import Model

myModel = Model()
myModel._crea_grafo("circle", 2014)
print(myModel.get_dettagli_grafo())
top_5 = myModel.get_top_citta_adiacenti()
for t in top_5:
    print(t)
print()
path, distanza, n_citta = myModel._handle_path("austin", 20, 3)
print("Distanza: ", distanza)
print("N città: ", n_citta)
for p in path:
    print(p)
