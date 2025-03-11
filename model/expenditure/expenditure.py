import datetime

# Precios por 1000 tokens en USD
# Ojo, este es el precio de Claude 3.5 sonnet
PRICE_PER_1000_INPUT = 0.003  # Precio por 1000 tokens de entrada
PRICE_PER_1000_OUTPUT = 0.015  # Precio por 1000 tokens de salida

def calculate_cost(input_tokens, output_tokens):
    # Cálculo del costo
    cost_input = (input_tokens / 1000) * PRICE_PER_1000_INPUT
    cost_output = (output_tokens / 1000) * PRICE_PER_1000_OUTPUT
    total_cost = cost_input + cost_output
    
    return cost_input, cost_output, total_cost

def update_expenditure(input_tokens, output_tokens):
    date_today = datetime.date.today().strftime("%d/%m/%Y")
    
    # Variables para almacenar datos históricos
    all_data = {}  # Diccionario para almacenar datos por fecha
    total_tokens = 0
    total_spent = 0.0
    
    # Intentar leer el archivo existente
    try:
        with open("expenditure.txt", "r") as file:
            lines = file.readlines()
            
            current_date = None
            i = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # Si encontramos una fecha
                if line and not line.startswith("INPUT") and not line.startswith("OUTPUT") and not line.startswith("TOTAL"):
                    if line != "-" * 50 and not line.startswith("TOTAL USAGE"):
                        current_date = line
                        all_data[current_date] = {"input_tokens": 0, "output_tokens": 0, "input_cost": 0, "output_cost": 0}
                
                # Procesar líneas de datos
                elif line.startswith("INPUT") and current_date:
                    parts = line.split("|")
                    if len(parts) >= 3:
                        tokens_part = parts[1].strip()
                        cost_part = parts[2].strip()
                        
                        input_tokens_existing = int(tokens_part.split(":")[1].strip())
                        input_cost_existing = float(cost_part.split("$")[1].strip())
                        
                        all_data[current_date]["input_tokens"] = input_tokens_existing
                        all_data[current_date]["input_cost"] = input_cost_existing
                
                elif line.startswith("OUTPUT") and current_date:
                    parts = line.split("|")
                    if len(parts) >= 3:
                        tokens_part = parts[1].strip()
                        cost_part = parts[2].strip()
                        
                        output_tokens_existing = int(tokens_part.split(":")[1].strip())
                        output_cost_existing = float(cost_part.split("$")[1].strip())
                        
                        all_data[current_date]["output_tokens"] = output_tokens_existing
                        all_data[current_date]["output_cost"] = output_cost_existing
                
                # Línea de TOTAL USAGE para calcular totales generales
                elif line.startswith("TOTAL USAGE"):
                    parts = line.split("|")
                    if len(parts) >= 3:
                        tokens_part = parts[1].strip()
                        cost_part = parts[2].strip()
                        
                        total_tokens = int(tokens_part.split(":")[1].strip())
                        total_spent = float(cost_part.split("$")[1].strip())
                
                i += 1
                
    except FileNotFoundError:
        pass  # El archivo no existe, comenzaremos uno nuevo
    
    # Calcular costos para los nuevos tokens
    cost_input, cost_output, total_cost = calculate_cost(input_tokens, output_tokens)
    
    # Actualizar o agregar entrada para hoy
    if date_today in all_data:
        all_data[date_today]["input_tokens"] += input_tokens
        all_data[date_today]["output_tokens"] += output_tokens
        all_data[date_today]["input_cost"] += cost_input
        all_data[date_today]["output_cost"] += cost_output
    else:
        all_data[date_today] = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost": cost_input,
            "output_cost": cost_output
        }
    
    # Recalcular totales
    total_tokens = 0
    total_spent = 0.0
    
    for date_data in all_data.values():
        total_tokens += date_data["input_tokens"] + date_data["output_tokens"]
        total_spent += date_data["input_cost"] + date_data["output_cost"]
    
    # Escribir los datos formateados con tabuladores
    with open("expenditure.txt", "w") as file:
        for date, data in all_data.items():
            # Calcular totales por día
            day_total_tokens = data["input_tokens"] + data["output_tokens"]
            day_total_cost = data["input_cost"] + data["output_cost"]
            
            file.write(f"{date}\n")
            file.write(f"INPUT\t| Tokens: {data['input_tokens']}\t| Cost: ${data['input_cost']:.7f}\n")
            file.write(f"OUTPUT\t| Tokens: {data['output_tokens']}\t| Cost: ${data['output_cost']:.7f}\n")
            file.write(f"TOTAL\t| Tokens: {day_total_tokens}\t| Cost: ${day_total_cost:.7f}\n\n")
        
        # Línea separadora
        file.write("-" * 50 + "\n")
        
        # Totales generales
        file.write(f"TOTAL USAGE\t| Tokens: {total_tokens}\t| Cost: ${total_spent:.7f}\n")

if __name__ == "__main__":
    # Ejemplo de uso
    update_expenditure(input_tokens=10, output_tokens=0)