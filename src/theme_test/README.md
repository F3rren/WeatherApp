# ThemeHandler Test

Questa cartella contiene un esempio minimale e indipendente per testare la logica di ThemeHandler e il cambio tema in Flet.

## File principali
- `theme_handler.py`: gestore centralizzato dei colori tema.
- `test_app.py`: piccola app Flet con un componente di test che mostra testo principale, secondario e un bottone per cambiare tema.

## Come usare
1. Assicurati che `utils/config.py` sia accessibile dal path di import (puoi copiare il file o aggiungere il path al PYTHONPATH).
2. Avvia `test_app.py`:
   ```bash
   python theme_test/test_app.py
   ```
3. Prova il bottone "Cambia tema" e verifica che i colori cambino correttamente.

Puoi modificare/estendere questi file per testare altri ruoli colore o logiche di tema.
