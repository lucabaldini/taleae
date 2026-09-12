# Contribuire a UniPico

Chiunque abbia del materiale che si allinei con le idee di base del
progetto è benvenuto&mdash;l'unico modo per avere veramente visibilità
è raggiungere la massa critica.

Il modello che abbiamo in mente è semplice: *ciascun nuovo progetto nel
catalogo corrisponde ad un repositorio separato nell'organizzazione
[unipico](https://codeberg.org/unipico) su codeberg.*
All'interno di ciascun repositorio, i proprietari hanno piena autonomia
di struttura e contenuti. La parola d'ordine è *elasticità*.


## Requisiti minimi

Ci sono due semplici cose che ci sentiamo di richiedere in modo non
negoziabile:

1. il materiale deve essere rilasciato sotto una licenza ben identificabile
   che, oltre alla consultazione, permetta la modifica e la
   redistribuzione&mdash;[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) e [GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html)
   sono due scelte ovvie (ma non le uniche);
2. il repositorio non deve contenere file in formati proprietari,
   o che non siano leggibili con strumenti *liberi*.

Da questo punto di vista un repositorio con un singolo file pdf è
perfettamente accettabile, purché il testo soddisfi la condizione 1. qui
sopra.

Le informazioni minime che richiediamo per popolare il catalogo sono:

* titolo ed autore;
* lingua (e.g., italiano, inglese);
* licenza;
* tecnologia utilizzata (e.g., [LaTeX](https://latex3.github.io/),
  [LibreOffice](https://www.libreoffice.org/),
  [quarto](https://quarto.org/),
  [MkDocs](https://www.mkdocs.org/));
* link al repositorio.


## Buone pratiche

Detto questo, il nostro progetto punta ad essere molto di più di una
semplice collezione di file pdf. Queste sono le raccomandazioni per massimizzare
impatto e ri-usabilità:

1. se il materiale nella sua forma finale è ottenuto processando file
   sorgente di tipo diverso (e.g., LaTeX, o markup), allora raccomandiamo che
   questi ultimi siano inclusi nel repositorio con licenza opportuna;
2. se il prodotto finale contiene grafici e figure, raccomandiamo che
   queste siano incluse separatamente nel repositorio in una versione ad alta
   risoluzione (e, ove possibile, in formato vettoriale);
3. se le figure sono generate programmaticamente, raccomandiamo che il codice sorgente
   per la loro generazione, ove possibile, sia incluso nel repositorio con licenza
   opportuna;
4. se il processo di generazione del prodotto finale non è del tutto banale,
   allora idealmente raccomandiamo un minimo sforzo di documentazione per
   permettere all'utente di riprodurlo.

Capiamo perfettamente che ciascuna di queste raccomandazioni implica un carico
di lavoro aggiuntivo sull'autore, e tuttavia riteniamo che, ove praticamente
possibile, questo sforzo addizionale sia più che bilanciato dall'impatto
positivo sulla comunità.

[Vai alle guide pratiche](tutorials.md){ .md-button .md-button }
