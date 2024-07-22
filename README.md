# MetRisk: A Post-Processing Application for OpenQuake Risk Analysis

## Introduction
MetRisk is a powerful offline application designed to enhance the post-processing capabilities of the OpenQuake platform. OpenQuake is a state-of-the-art open-source platform for modeling and analyzing earthquake hazards and risks. However, the available post-processing tools are limited. MetRisk addresses this gap by providing a graphical interface for risk scenario analysis, enabling users to produce risk maps, compute hazard exceedance curves, and assess simulation convergence.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)

## Features
- **Risk Maps**: Generate visual representations of risk scenarios.
- **Hazard Exceedance Curves**: Compute and visualize hazard exceedance probabilities.
- **Simulation Convergence Assessment**: Evaluate the convergence of stochastic risk scenarios.
- **Interactive Interface**: User-friendly interface built with Tkinter for easy navigation and data visualization.

## Requirements
To run MetRisk offline, you need a Python environment capable of executing Python scripts and visualizing the Tkinter-based interface. We recommend using Spyder, which can be easily downloaded from the official website.

### Required Python Libraries
Before running MetRisk, ensure the following libraries are installed:
\```python
# Tkinter Library
import tkinter as tk
from tkinter import ttk, filedialog, Toplevel, messagebox

# Graphics TKinter Library
from PIL import Image, ImageTk
import matplotlib.ticker as ticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Directory Library
import os
import glob
import zipfile
import io

# Data Processing Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

# Summary Tables Libraries
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side

# Geographic Data Libraries
import geopandas as gpd
import contextily as ctx
from matplotlib.colors import Normalize
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import ListedColormap
from matplotlib import cm
import matplotlib.offsetbox as offsetbox
from matplotlib.patches import Rectangle
import re

# File Dialog and Message Box
from tkinter import filedialog, messagebox as tk_messagebox

# PDF Generation Libraries
from reportlab.pdfgen import canvas
import PyPDF2

# HDF5 Libraries
import h5py
import json
\```

## Installation
1. **Clone the repository:**
   \```bash
   git clone https://github.com/yourusername/MetRisk.git
   \```
2. **Navigate to the project directory:**
   \```bash
   cd MetRisk
   \```
3. **Install the required libraries:**
   \```bash
   pip install -r requirements.txt
   \```
4. **Run the application:**
   \```bash
   python InterfaceLayout.py
   \```

## Software Description

### 2.1. Software Architecture
The application operates offline, featuring an interactive interface developed with Tkinter. This interface facilitates the visualization and manipulation of data associated with stochastic events and their analysis.

#### 2.1.1. Application Core: InterfaceLayout
- **Library Importation**: Lists all necessary libraries for optimal operation, including Tkinter for the graphical interface and other specialized libraries for data processing and analysis.
- **Window Colors**: Defines a color palette used throughout the application, allowing customization.
- **Tab Management**: Handles the logic for showing or hiding tab content based on user selection. Each tab includes variables for title, text, buttons, images, canvas, and rectangles. Essential functions for interaction between tabs include:
  - `Show_(Tab Name)`: Shows the content of the selected tab.
  - `Hide_(Tab Name)`: Hides the content of the selected tab.
  - `Select_Show_(Tab Name)`: Generates an animation when the tab is selected.
  - `Unselect_Show_(Tab Name)`: Generates an animation when another tab is selected.
- **Tab Elements**: Displays results based on user-provided files or algorithm execution.
- **Navigation Functions**: Essential functions for navigation, displaying messages, selecting folders, etc.
- **Main Window**: Configures the main interface, specifying size, element arrangement, and behavior.

#### 2.1.2. Content-Specific Modules
- **Home**: `Home.py` generates the initial content visible to the user.
- **Stochastic Events**: `CalibrationStochasticEvents.py` and `DispersionStochasticEvents.py` process and display the calibration and dispersion of stochastic events. `StochasticEvents.py` configures the page within the interface.
- **Losses and Damages**: `LossesANDDamage.py` and submodules like `Damage.py` and `Losses.py` handle the visualization and analysis of losses and damages.
- **Geographic Maps**: `MapsGenerator.py` generates geographic risk and damage maps based on probabilistic and deterministic events.
- **Generator**: `Generator.py` obtains all risk and damage results based on probabilistic or deterministic events, exporting geographic maps.
- **Data Sheets**: `DataSheets.py` generates technical sheets of desired results.
- **Reports**: `Reports.py` allows users to download pre-generated technical sheets.

#### 2.1.3. Common Functions Library: FunctionsLibrary.py
Stores reusable functions for generating graphs, inserting buttons, exporting results, etc., facilitating maintenance and expansion of the application.

## Usage
1. **Start the application:**
   \```bash
   python InterfaceLayout.py
   \```
2. **Navigate through the interface using the tabs to analyze risk scenarios.**

## Contributing
We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments
We acknowledge the developers of OpenQuake for their foundational platform and the community for their continuous support and contributions.

