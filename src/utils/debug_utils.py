"""
Utility di debugging per l'applicazione MeteoApp.
"""

import logging
import inspect
import os
import traceback

def log_error(error, context=None):
    """
    Registra un errore con informazioni di contesto dettagliate.
    
    Args:
        error: L'eccezione da registrare
        context: Un contesto aggiuntivo da registrare (opzionale)
    """
    # Ottieni il frame chiamante
    caller_frame = inspect.currentframe().f_back
    caller_info = inspect.getframeinfo(caller_frame)
    
    # Recupera nome del file, numero di linea e funzione chiamante
    file_name = os.path.basename(caller_info.filename)
    line_number = caller_info.lineno
    function_name = caller_info.function
    
    # Prepara il messaggio di errore dettagliato
    error_message = f"ERROR in {file_name}:{line_number} (function: {function_name}): {str(error)}"
    if context:
        error_message += f"\nContext: {context}"
    
    # Aggiungi lo stack trace
    error_message += f"\nStack trace:\n{traceback.format_exc()}"
    
    # Registra l'errore
    logging.error(error_message)

def dump_object_info(obj, title=None):
    """
    Stampa informazioni dettagliate su un oggetto per il debugging.
    
    Args:
        obj: L'oggetto da esaminare
        title: Un titolo opzionale da mostrare prima delle informazioni
    """
    if title:
        logging.info(f"--- {title} ---")
    
    # Tipo dell'oggetto
    logging.info(f"Type: {type(obj)}")
    
    # Attributi principali dell'oggetto
    logging.info("Attributes:")
    for attr_name in dir(obj):
        if not attr_name.startswith('__'):
            try:
                attr_value = getattr(obj, attr_name)
                # Evita di stampare callable o oggetti complessi
                if not callable(attr_value):
                    # Limita la lunghezza della rappresentazione dell'attributo
                    value_repr = repr(attr_value)
                    if len(value_repr) > 100:
                        value_repr = value_repr[:100] + "..."
                    logging.info(f"  {attr_name}: {value_repr}")
            except Exception as e:
                logging.info(f"  {attr_name}: <Error getting value: {e}>")
    
    logging.info("---" + "-" * (len(title) if title else 0) + "---")
