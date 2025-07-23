#!/usr/bin/env python3

import json
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd


class ExportDataService:
    """Servizio per esportare i dati meteorologici in vari formati."""
    
    def __init__(self, storage_path: str = "storage/data/weather_data.json"):
        self.storage_path = storage_path
        self.export_dir = "storage/exports"
        self._ensure_export_directory()
    
    def _ensure_export_directory(self):
        """Assicura che la directory di export esista."""
        os.makedirs(self.export_dir, exist_ok=True)
    
    def _generate_sample_data(self, days: int = 7) -> List[Dict]:
        """Genera dati di esempio per testing."""
        import random
        
        data = []
        base_date = datetime.now() - timedelta(days=days)
        
        for i in range(days * 24):  # Dati orari
            current_time = base_date + timedelta(hours=i)
            
            # Simula dati meteorologici realistici
            base_temp = 20 + 10 * random.random()  # 20-30°C
            humidity = 40 + 40 * random.random()   # 40-80%
            pressure = 1000 + 20 * random.random() # 1000-1020 hPa
            wind_speed = 5 + 15 * random.random()  # 5-20 km/h
            precipitation = random.random() * 5 if random.random() > 0.7 else 0  # 30% chance di pioggia
            
            data.append({
                "timestamp": current_time.isoformat(),
                "date": current_time.strftime("%Y-%m-%d"),
                "time": current_time.strftime("%H:%M"),
                "temperature": round(base_temp, 1),
                "humidity": round(humidity, 1),
                "pressure": round(pressure, 1),
                "wind_speed": round(wind_speed, 1),
                "wind_direction": random.randint(0, 360),
                "precipitation": round(precipitation, 2),
                "visibility": round(8 + 7 * random.random(), 1),  # 8-15 km
                "uv_index": max(0, round(5 + 6 * random.random())),  # 0-11
                "cloud_coverage": round(random.random() * 100, 1)  # 0-100%
            })
        
        return data
    
    def export_to_csv(self, data: List[Dict], filename: str = None, selected_fields: List[str] = None) -> str:
        """Esporta i dati in formato CSV."""
        if not filename:
            filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Filtra i campi se specificato
        if selected_fields and data:
            filtered_data = []
            for record in data:
                filtered_record = {field: record.get(field, '') for field in selected_fields if field in record}
                filtered_data.append(filtered_record)
            data = filtered_data
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if data:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
            
            return filepath
        except Exception as e:
            raise Exception(f"Errore nell'esportazione CSV: {e}")
    
    def export_to_excel(self, data: List[Dict], filename: str = None, selected_fields: List[str] = None) -> str:
        """Esporta i dati in formato Excel."""
        if not filename:
            filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        filepath = os.path.join(self.export_dir, filename)
        
        try:
            df = pd.DataFrame(data)
            
            # Filtra le colonne se specificato
            if selected_fields:
                available_fields = [field for field in selected_fields if field in df.columns]
                df = df[available_fields]
            
            # Salva con pandas
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Weather Data', index=False)
                
                # Aggiungi un foglio con statistiche
                if not df.empty:
                    stats_df = df.describe()
                    stats_df.to_excel(writer, sheet_name='Statistics')
            
            return filepath
        except Exception as e:
            raise Exception(f"Errore nell'esportazione Excel: {e}")
    
    def export_to_json(self, data: List[Dict], filename: str = None, selected_fields: List[str] = None) -> str:
        """Esporta i dati in formato JSON."""
        if not filename:
            filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.export_dir, filename)
        
        # Filtra i campi se specificato
        if selected_fields and data:
            filtered_data = []
            for record in data:
                filtered_record = {field: record.get(field, '') for field in selected_fields if field in record}
                filtered_data.append(filtered_record)
            data = filtered_data
        
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "total_records": len(data),
                "data": data
            }
            
            with open(filepath, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, ensure_ascii=False, indent=2)
            
            return filepath
        except Exception as e:
            raise Exception(f"Errore nell'esportazione JSON: {e}")
    
    def export_to_pdf(self, data: List[Dict], filename: str = None) -> str:
        """Esporta i dati in formato PDF (report)."""
        if not filename:
            filename = f"weather_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.export_dir, filename)
        
        try:
            # Per ora crea un file di testo che simula un PDF
            # In futuro si può usare reportlab o matplotlib per PDF veri
            with open(filepath.replace('.pdf', '.txt'), 'w', encoding='utf-8') as txtfile:
                txtfile.write("WEATHER DATA REPORT\n")
                txtfile.write("=" * 50 + "\n\n")
                txtfile.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                txtfile.write(f"Total Records: {len(data)}\n\n")
                
                if data:
                    # Statistiche di base
                    temperatures = [d.get('temperature', 0) for d in data if d.get('temperature')]
                    if temperatures:
                        txtfile.write(f"Temperature Range: {min(temperatures):.1f}°C - {max(temperatures):.1f}°C\n")
                        txtfile.write(f"Average Temperature: {sum(temperatures)/len(temperatures):.1f}°C\n\n")
                    
                    # Prime 10 righe di dati
                    txtfile.write("SAMPLE DATA (First 10 records):\n")
                    txtfile.write("-" * 50 + "\n")
                    for i, record in enumerate(data[:10]):
                        txtfile.write(f"Record {i+1}:\n")
                        for key, value in record.items():
                            txtfile.write(f"  {key}: {value}\n")
                        txtfile.write("\n")
            
            return filepath.replace('.pdf', '.txt')
        except Exception as e:
            raise Exception(f"Errore nell'esportazione PDF: {e}")
    
    def get_export_data(self, period: str = "week", data_types: List[str] = None) -> List[Dict]:
        """Ottiene i dati da esportare in base al periodo selezionato."""
        
        # Determina il numero di giorni in base al periodo
        days_mapping = {
            "week": 7,
            "month": 30,
            "year": 365,
            "custom": 7  # Default per periodo personalizzato
        }
        
        days = days_mapping.get(period, 7)
        
        # Per ora genera dati di esempio
        # In futuro dovrebbe leggere da un database o file di dati reali
        all_data = self._generate_sample_data(days)
        
        # Filtra per tipi di dati se specificato
        if data_types:
            filtered_data = []
            for record in all_data:
                filtered_record = {"timestamp": record["timestamp"], "date": record["date"], "time": record["time"]}
                
                if "temperature" in data_types:
                    filtered_record["temperature"] = record["temperature"]
                if "humidity" in data_types:
                    filtered_record["humidity"] = record["humidity"]
                if "precipitation" in data_types:
                    filtered_record["precipitation"] = record["precipitation"]
                if "wind" in data_types:
                    filtered_record["wind_speed"] = record["wind_speed"]
                    filtered_record["wind_direction"] = record["wind_direction"]
                if "pressure" in data_types:
                    filtered_record["pressure"] = record["pressure"]
                
                filtered_data.append(filtered_record)
            
            return filtered_data
        
        return all_data
    
    def get_available_formats(self) -> List[Dict]:
        """Ottiene la lista dei formati di esportazione disponibili."""
        return [
            {"value": "csv", "name": "CSV", "description": "File di valori separati da virgola"},
            {"value": "excel", "name": "Excel (.xlsx)", "description": "Foglio di calcolo Excel"},
            {"value": "json", "name": "JSON", "description": "JavaScript Object Notation"},
            {"value": "pdf", "name": "PDF Report", "description": "Report in formato PDF"},
        ]
