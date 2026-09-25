# BMWP/Bol (MMAyA 2012), Tabla 1 de Leaño Sanabria y Pérez Barriga (2020), Acta Nova 9(4): 569-591, pp. 573-575. Transcripción 25-09-2026.
BOL = {
10: "Oligoneuriidae Gripopterygidae Perlidae Odontoceridae Psephenidae Athericidae Blephariceridae",
9:  "Calamoceratidae Hydrobiosidae Leptoceridae Xiphocentronidae Ptilodactylidae Leptophlebiidae Euthyplociidae Polymitarcyidae",
8:  "Helicopsychidae Psychomyiidae Glossosomatidae Philopotamidae Polycentropodidae Simuliidae Gomphidae Polythoridae Megapodagrionidae",
7:  "Leptohyphidae Hydraenidae Scirtidae Corydalidae Calopterygidae Limnephilidae Hydroptilidae",
6:  "Aeshnidae Coenagrionidae Libellulidae Ancylidae Corixidae Naucoridae Notonectidae Mesoveliidae Hebridae Dixidae Psychodidae Dryopidae Lutrochidae",
5:  "Baetidae Elmidae Staphylinidae Dytiscidae Noteridae Pyralidae Hydropsychidae Tipulidae Belostomatidae Gerridae Nepidae Veliidae Hydrobiidae Ampullariidae",
4:  "Caenidae Hydrophilidae Haliplidae Heteroceridae Gyrinidae Ceratopogonidae Dolichopodidae Empididae Tabanidae Stratiomyidae Pleidae Gelastocoridae Hydracarina Planorbidae Physidae Lymnaeidae Aeglidae Palaemonidae Sphaeriidae Amphipoda Ostracoda Planariidae Nematoda",
3:  "Muscidae Glossiphoniidae",
2:  "Chironomidae Culicidae Ephydridae Hyriidae",
1:  "Oligochaeta",
}
NOTAS = {"Polymitarcyidae": "original: «Polymitarcydae»", "Hydracarina": "original: «Hidracarina»", "Planorbidae": "original: «Planorbiidae»",
         "Amphipoda": "original: «Amphypoda» (orden, sin familia)", "Ampullariidae": "original: «Ampullaridae»"}
ROWS = [(n, s) for s, names in BOL.items() for n in names.split()]
assert len(ROWS) == 88, len(ROWS)
