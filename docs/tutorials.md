# Guide pratiche

Uno degli scopi del progetto è quello di facilitare il percorso di rilascio di
materiale, nuovo o già esistente, in una forma che sia compatibile con i nostri
obiettivi.

Questa sezione raccoglie link a materiale utile per creare un nuovo repositorio
o per migrare materiale già esistente nella forma di un repositorio su
Codeberg.


## Cosa è un repositorio?

In termini semplici, un repositorio è lo spazio digitale in cui sono archiviati 
tutti i file del tuo progetto didattico o editoriale (testi, immagini, codici 
sorgente, file di configurazione).

A differenza di una semplice cartella su computer o su servizi cloud tradizionali, 
un repositorio gestito tramite il [sistema Git](https://git-scm.com/) (come quelli ospitati su Codeberg) 
funziona come uno storico intelligente che registra ogni modifica apportata nel tempo.

Se ti stai domaando perché dovresti tenere traccia delle modifiche a questo modo,
delle rispost possibili sono perchè

1. Ogni volta che salvi una versione importante dei tuoi file (operazione chiamata _commit_), 
   Git crea una "fotografia" del progetto. Questo significa che puoi esplorare l'evoluzione 
   del tuo lavoro e, se necessario, tornare indietro a qualsiasi versione precedente 
   senza correre il rischio di perdere materiale.

2. Più autori o contributori possono lavorare allo stesso progetto contemporaneamente. 
   Git gestisce l'unione dei contributi e permette di revisionare le modifiche altrui 
   prima di integrarle nel testo finale.

3. Nei progetti Tālĕae, il repositorio non serve solo a conservare i file sorgente 
   (es. in Markdown, Quarto o LaTeX). Tramite Codeberg, ogni volta che aggiorni il repositorio, 
   il sistema può generare e pubblicare automaticamente la versione finale stampabile (PDF) 
   o consultabile online (HTML).

### Alcuni concetti chiave

Nonostante Git sia [nato nel mondo della programmazione](https://git-scm.com/book/it/v2/Per-Iniziare-Una-Breve-Storia-di-Git),
non serve essere realmente dei programmatori per usare un repositorio Git, ti basta prendere 
confidenza con poche operazioni fondamentali:

- Il repositorio remoto è la versione del progetto ospitata su Codeberg. Il repositorio 
  locale è la copia del progetto che risiede sul tuo computer, su cui lavori quotidianamente.

- **Clonare** È l'operazione iniziale per scaricare una copia completa del repositorio 
   da Codeberg sul tuo computer.

- **Commit** È il salvataggio di una serie di modifiche nel tuo repositorio locale, accompagnato 
  da un breve messaggio descrittivo (es. "Aggiunto materiale per la Lezione 2 del corso").

- **Push** È l'atto di "caricare" e inviare i tuoi commit dal tuo computer a Codeberg, 
  rendendo le tue modifiche visibili agli altri e aggiornando il progetto online.

- **Pull** È l'operazione opposta al push: scarica sul tuo computer gli ultimi aggiornamenti 
  che altri collaboratori o collaboratrici hanno caricato su Codeberg.

Negli esempi di seguito è illustrato come sfruttare Git insieme ad altri strumenti _liberi_
per produrre delle dispense e del materiale didattico.

#### Git tramite terminale

Per iniziare a usare Git tramite terminale, ti basta seguire pochi passaggi fondamentali. 
Per prima cosa, configura la tua identità eseguendo da terminale: 
```bash 
git config --global user.name "Il Tuo Nome"` 
git config --global user.email "tua.email@esempio.com" 
```
Una volta fatto questo, puoi scaricare una copia del progetto sul tuo computer usando 
il comando 
```bash
git clone <URL_DEL_REPOSITORY>
```
(copiando l'indirizzo HTTPS da Codeberg) ed entrare nella cartella creata con `cd nome-cartella`.

Ad **esempio**, se vuoi vedere come sono costruite queste pagine web puoi eseguire:
```bash
git clone https://codeberg.org/taleae/pages.git
```
Durante il tuo lavoro di scrittura o modifica dei file, il ciclo quotidiano si basa 
su tre comandi principali: 

- digita `git status` per controllare quali file hai modificato, 

- `git add .` per selezionare tutte le modifiche e prepararle al salvataggio, e 

- `git commit -m "Messaggio descrittivo"` per creare una "fotografia" ufficiale del lavoro sul tuo computer. 

- Infine, per sincronizzare il tuo computer con Codeberg, usa `git push` per caricare online 
le tue modifiche salvate, oppure `git pull` per scaricare e integrare eventuali aggiornamenti 
fatti da altri collaboratori o collaboratrici.

Una guida completa di Git è disponibile [qui](https://git-scm.com/docs), oppure sulla 
[documentazione ufficiale di Codeberg](https://docs.codeberg.org/).

#### Git tramite interfaccia grafica

Se preferisci evitare il terminale, puoi gestire il tuo repositorio e interagire con Git 
tramite un'interfaccia grafica (GUI) o un'interfaccia testuale interattiva (TUI) che semplificano 
notevolmente operazioni quotidiane come il _commit_, il _push_ e il _pull_. Esistono diversi 
strumenti liberi e intuitivi che puoi utilizzare, tra cui 

- **[SourceGit](https://sourcegit-scm.github.io/)**, un client grafico leggero e ricco di funzionalità per visualizzare la cronologia dei commit; 

- **[Gitnuro](https://gitnuro.com/)**, un'applicazione desktop moderna, veloce e pulita per la gestione del codice; oppure 

- **[lazygit](https://lazygit.dev/)**, un'interfaccia a terminale (TUI) estremamente efficiente e semplice da usare direttamente dalla riga di comando.

## Strumenti e template

Questa sezione contiene una breve lista di strumenti liberi che possono
essere utili per la preparazione di materiale didattico. La lista, va da sé, non
è esaustiva, e può evolvere nel tempo.

---

### Quarto

[quarto](https://quarto.org/) è un sistema di impaginazione e grafica, molto
adatto per le applicazioni scientifiche e tecniche, basato su un linguaggio
di markup, e che supporta diversi tipi di output, tra cui html e pdf.

Link al [template quarto](https://codeberg.org/taleae/quarto_template).

Link alla guida:
[html](https://taleae.codeberg.page/quarto_guide/),
[pdf](https://taleae.codeberg.page/quarto_guide/quarto_guide.pdf),
[repo](https://codeberg.org/taleae/quarto_guide).

---

### LaTeX

[LaTeX](https://latex3.github.io/) è un linguaggio di markup per la preparazione di
documenti, fortemente orientato alla matematica ed alle materie tecniche
(ma non per questo inadatto a documenti non tecnici, specialmente se complessi.)
Il formato tipico del prodotto finale è il pdf.

Link al [template LaTeX](https://codeberg.org/taleae/latex_template).

Link alla guida:
[pdf](https://taleae.codeberg.page/latex_guide/latex_guide.pdf),
[repo](https://codeberg.org/taleae/latex_guide).


---


### Jupyter Book

[Jupyter Book](https://jupyterbook.org/) è un sistema basato su un linguaggio di
markup, ed orientato alle applicazioni tecniche.

---

### MkDocs e Material

[MkDocs](https://www.mkdocs.org/) è di nuovo un sistema di composizione basato
su un linguaggio di markup orientato alla creazione di siti html statici.
Questa pagina web è stata realizzata con questa tecnologia.

---

### typst

[typst](https://typst.app/) è uno dei candidati successori di LaTeX, con un
compilatore open source che supporta la creazione di file pdf e pagine web.