import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

def generate_bar_chart(data):
    if not data:
        return None

    # Ordenar datos de mayor a menor para que se vea bonito
    data.sort(key=lambda x: x[1], reverse=False) # Orden inverso para barras horizontales

    categories = [x[0].capitalize() for x in data]
    amounts = [x[1] for x in data]

    # Configuración de colores (Gradiente teal/azul)
    colors = ['#2A9D8F' for _ in amounts] 

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(8, 5)) # Más ancho que alto
    
    # Barras horizontales (barh)
    bars = ax.barh(categories, amounts, color=colors, height=0.6)

    # Estilo Minimalista
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    
    # Líneas de guía verticales
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    
    # Añadir el monto al final de cada barra
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + (max(amounts) * 0.02) # Un poquito a la derecha
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'${width:,.0f}', 
                va='center', fontsize=10, fontweight='bold', color='#333333')

    plt.title('Gastos por Categoría', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    # Guardar
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    plt.close()
    
    return buf