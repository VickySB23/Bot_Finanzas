import matplotlib
matplotlib.use('Agg') # OBLIGATORIO para evitar cuelgues
import matplotlib.pyplot as plt
import io

def generate_pie_chart(data):
    if not data:
        return None

    # Separar datos
    categories = [x[0] for x in data]
    amounts = [x[1] for x in data]

    # --- DISEÑO MODERNO (DONUT CHART) ---
    
    # 1. Configuración de colores (Paleta "Figma")
    # Colores: Teal, Coral, Purple, Slate, Blue
    colors = ['#2A9D8F', '#E76F51', '#264653', '#E9C46A', '#F4A261']
    
    # 2. Crear figura y ejes
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # 3. Dibujar la torta con "agujero" (Dona)
    wedges, texts, autotexts = ax.pie(
        amounts, 
        labels=categories, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors,
        pctdistance=0.85, # Porcentaje más cerca del borde
        wedgeprops=dict(width=0.3, edgecolor='white') # El width crea el agujero
    )

    # 4. Estilizar textos
    plt.setp(texts, size=12, weight="bold")
    plt.setp(autotexts, size=10, weight="bold", color="white")

    # 5. Título y círculo central
    ax.set_title('Gastos por Categoría', fontsize=14, pad=20)
    
    # Añadir total en el centro
    total = sum(amounts)
    plt.text(0, 0, f"${total:,.0f}", ha='center', va='center', fontsize=12, fontweight='bold')

    # 6. Guardar limpio
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close()
    
    return buf