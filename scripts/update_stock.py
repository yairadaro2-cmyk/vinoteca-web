#!/usr/bin/env python3
import gspread
import json
import os
import sys
from google.oauth2.service_account import Credentials

def main():
    try:
        # Cargar credenciales de Google desde variable de entorno
        creds_json = os.environ.get('GOOGLE_CREDS')
        if not creds_json:
            print("❌ Error: GOOGLE_CREDS no está configurado")
            sys.exit(1)
        
        creds_dict = json.loads(creds_json)
        
        # Autenticar con Google Sheets API
        scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        gc = gspread.authorize(creds)
        
        # Abrir el Google Sheet
        print("📖 Abriendo Google Sheet...")
        sheet_id = '1WDRxwXoyLc_sMuhvog3mYErRABo6Os0w5IijExdOS1U'
        spreadsheet = gc.open_by_key(sheet_id)
        worksheet = spreadsheet.sheet1
        
        # Obtener todos los registros
        print("📥 Descargando datos...")
        rows = worksheet.get_all_records()
        print(f"   Total de filas: {len(rows)}")
        
        # Procesar productos
        productos = []
        agotados = 0
        
        for idx, row in enumerate(rows):
            try:
                stock = int(row.get('STOCK', 0))
                
                if stock > 0:
                    # Parsear precio
                    precio_str = str(row.get('PRECIO_VENTA', '0')).replace('.', '').replace(',', '.')
                    precio = float(precio_str)
                    
                    producto = {
                        'id': str(row.get('', '')).strip(),
                        'nombre': str(row.get('ARTÍCULO', '')).strip(),
                        'marca': str(row.get('MARCA', '')).strip(),
                        'precio': precio,
                        'rubro': str(row.get('RUBRO', '')).strip(),
                        'subrubro': str(row.get('SUBRUBRO', '')).strip(),
                        'stock': stock
                    }
                    productos.append(producto)
                else:
                    agotados += 1
            except Exception as e:
                print(f"   ⚠️  Fila {idx + 1}: Error procesando - {e}")
                continue
        
        # Guardar JSON
        output_file = 'productos.json'
        print(f"\n💾 Guardando {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(productos, f, ensure_ascii=False, indent=2)
        
        # Resumen
        print(f"\n✅ Actualización completada:")
        print(f"   • Productos disponibles: {len(productos)}")
        print(f"   • Productos agotados: {agotados}")
        print(f"   • Total: {len(productos) + agotados}")
        print(f"   • Archivo: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
