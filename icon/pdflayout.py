# -*- coding: utf-8 -*-
"""
Created on Thu May 16 11:50:50 2024

@author: orlandoaram
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_pdf():
    # Crear un objeto PDF
    doc = SimpleDocTemplate("ejemplo.pdf", pagesize=letter)

    # Crear el contenido del PDF
    content = []

    # Agregar una figura al PDF
    imagen_path = os.path.join(os.getcwd(), "Metrisk_Home.png")
    imagen_width, imagen_height = 2.5 * inch, 2.5 * inch  # Ajustar el tamaño de la imagen
    figura = Image(imagen_path, width=imagen_width, height=imagen_height)
    content.append(figura)

    # Agregar una tabla al PDF
    data = [["Nombre", "Edad", "Género"],
            ["Juan", "30", "Masculino"],
            ["María", "25", "Femenino"],
            ["Carlos", "40", "Masculino"]]
    tabla = Table(data)
    tabla.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    content.append(tabla)

    # Construir el PDF
    doc.build(content)

if __name__ == "__main__":
    create_pdf()
    
#%%


# Crear un diagrama de barras de solo colapsos y tal vez daño extensivo
# las taxonomias agrupadas indepentdientemente del numero de pisos

categorias = ['BQ/MNR/ND','MA/MC/DU','MA/MC/ND','MA/MNR/ND','MA/MPC/ND','MZ/MNR/ND']
Colapsos_no_edis = [11,25,57,388,102,3]
Colapsos_prc = [36.5,47.5,64.4,31.8,61.5,16.2]

# Utilizar el mapa de colores 'plasma' invertido
colors = plt.cm.get_cmap('bone').reversed()(np.linspace(0.2, 1, len(categorias)))

# Crear el diagrama de barras con el nuevo mapa de colores y sin marco
fig, ax = plt.subplots()
fig.set_facecolor('#F2F2F2')
ax.set_facecolor('#F2F2F2')
bars = ax.bar(range(len(categorias)), Colapsos_prc, color=colors)

# Añadir los valores encima de cada barra
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}%', ha='center', va='bottom',fontname='Calibri', fontsize=9)

# Quitar ticks, títulos de los ejes y el marco del gráfico
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Añadir leyendas
ax.legend(bars, categorias,  bbox_to_anchor=(0.5, -0.20), ncol=3, fontsize=9, loc='lower center', frameon=False, handlelength=1, handletextpad=0.4)

plt.show()

#%%

# Crear un diagrama de barras de solo colapsos y tal vez daño extensivo
# las taxonomias agrupadas indepentdientemente del numero de pisos

categorias = ['BQ/MNR/ND','MA/MC/DU','MA/MC/ND','MA/MNR/ND','MA/MPC/ND','MZ/MNR/ND']
Colapsos_no_edis = [11,25,57,388,102,3]
Colapsos_prc = [3.95,20.9,29.6,24.7,40.7,3.5]

# Utilizar el mapa de colores 'plasma' invertido
colors = plt.cm.get_cmap('bone').reversed()(np.linspace(0.2, 1, len(categorias)))

# Crear el diagrama de barras con el nuevo mapa de colores y sin marco
fig, ax = plt.subplots()
fig.set_facecolor('#F2F2F2')
ax.set_facecolor('#F2F2F2')
bars = ax.bar(range(len(categorias)), Colapsos_prc, color=colors)

# Añadir los valores encima de cada barra
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.1f}%', ha='center', va='bottom',fontname='Calibri', fontsize=9)

# Quitar ticks, títulos de los ejes y el marco del gráfico
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Añadir leyendas
ax.legend(bars, categorias,  bbox_to_anchor=(0.5, -0.20), ncol=3, fontsize=9, loc='lower center', frameon=False, handlelength=1, handletextpad=0.4)

plt.show()

#%%
categorias = ['Sin Daño','Leve','Moderado','Extensivo','Colapso']
Colapsos_no_edis = [39.7,24.7,8.6,11.3,15.7]

# Definir el colormap
colors = plt.cm.get_cmap('bone').reversed()(np.linspace(0.1, 0.7, len(categorias)))

# Crear el diagrama circular
fig=plt.figure(figsize=(8, 8))
fig.set_facecolor('#F2F2F2')

wedges, texts, autotexts = plt.pie(Colapsos_no_edis, colors=colors, autopct='%1.1f%%', startangle=140)

# Añadir la leyenda
plt.legend(wedges, categorias, loc="center left", bbox_to_anchor=(0.92, 0.5),fontsize=14, frameon=False, handlelength=1, handletextpad=0.4)
plt.setp(autotexts, size=13, weight="bold")

# Eliminar el título del gráfico
plt.title('')
plt.show()