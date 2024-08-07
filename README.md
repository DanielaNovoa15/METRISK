# MetRisk: A Post-Processing Application for OpenQuake Risk Analysis

MetRisk is a powerful offline application designed to enhance the post-processing capabilities of the OpenQuake platform. OpenQuake is a state-of-the-art open-source platform for modeling and analyzing earthquake hazards and risks. However, the available post-processing tools are limited. MetRisk addresses this gap by providing a graphical interface for risk scenario analysis, enabling users to produce risk maps, compute hazard exceedance curves, and assess simulation convergence.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#Installation)
4. [Software Description](#software-description)
5. [Usage](#usage)
6. [License](#license)

## Features
- **Risk Maps**: Generate visual representations of risk scenarios.
- **Hazard Exceedance Curves**: Compute and visualize hazard exceedance probabilities.
- **Simulation Convergence Assessment**: Evaluate the convergence of stochastic risk scenarios.
- **Interactive Interface**: User-friendly interface built with Tkinter for easy navigation and data visualization.

## Requirements
To run MetRisk offline, you need a Python environment capable of executing Python scripts and visualizing the Tkinter-based interface. We recommend using Git Bash, which can be easily downloaded from the official website.

### Required Python Libraries
Before running MetRisk, ensure the following libraries are installed:

```python
pip install Pillow
pip install matplotlib
pip install pandas
pip install numpy
pip install openpyxl
pip install geopandas
pip install contextily
pip install reportlab
pip install PyPDF2
pip install h5py
```

## Installation
1. **Installing the Abadi Font:**
   
   ##### Unix-based Systems (Linux, macOS)
   You can install the Abadi font from the command line. Navigate to the `css` folder and run:
   ```bash
   sudo cp css/abadi-mt.ttf /Library/Fonts/  # macOS
   sudo cp css/abadi-mt.ttf /usr/share/fonts/  # Linux
   fc-cache -f -v
   ```

   ##### Windows
   For Windows users, the font must be installed manually:
   1. Navigate to the `css` folder.
   2. Double-click on `abadi-mt.ttf`.
   3. Click "Install" to install the font.

2. **Install Git Bash:**

   Go to the official Git website (`https://git-scm.com/downloads`) and download the installer.

   Run the installer and follow the on-screen instructions.

   During installation, select the default options unless you have specific needs.
3. **Install Python:**

   Go to the official Python website and download the installer (`https://www.python.org/downloads/`).

   Run the installer and be sure to check the **“Add Python to PATH”** option before installing.

   Follow the on-screen instructions to complete the installation.
4. **Verify the installation:**

   To make sure that both Git Bash and Python are properly installed, open Git Bash and run the following commands:
   ```bash
   git --version
   python --version
   pip --version
   ```
5. **Clone the repository:**

   Open Git Bash and run:
   ```bash
   git clone https://github.com/DanielaNovoa15/METRISK.git
   ```
6. **Navigate to the project directory:**

   Open Git Bash and run:
   ```bash
   cd METRISK
   ```
7. **Create and activate a virtual environment:**

   Open Git Bash and run:
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```
8. **Install the required libraries:**

   With the virtual environment activated, install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
9. **Run the application:**

   Finally, run the application:
   ```bash
   python InterfaceLayout.py
   ```

## Software Description

### Software Architecture
The application operates offline, featuring an interactive interface developed with Tkinter. This interface facilitates the visualization and manipulation of data associated with stochastic events and their analysis.

#### Application Core: InterfaceLayout.py
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

#### Content-Specific Modules
- **Home**: `Home.py` generates the initial content visible to the user.
- **Stochastic Events**: `CalibrationStochasticEvents.py` and `DispersionStochasticEvents.py` process and display the calibration and dispersion of stochastic events. `StochasticEvents.py` configures the page within the interface.
- **Losses and Damages**: `LossesANDDamage.py` and submodules like `Damage.py` and `Losses.py` handle the visualization and analysis of losses and damages.
- **Geographic Maps**: `MapsGenerator.py` generates geographic risk and damage maps based on probabilistic and deterministic events.
- **Generator**: `Generator.py` obtains all risk and damage results based on probabilistic or deterministic events, exporting geographic maps.
- **Data Sheets**: `DataSheets.py` generates technical sheets of desired results.
- **Reports**: `Reports.py` allows users to download pre-generated technical sheets.

#### Common Functions Library: FunctionsLibrary.py
Stores reusable functions for generating graphs, inserting buttons, exporting results, etc., facilitating maintenance and expansion of the application.

### Additional Folders
The application includes two additional folders:
- **icon**: Contains all .png images used in the platform to enhance the user interface, including logos of the application and the universities involved in the project.
- **css**: Stores the user manual for the platform (downloadable from the offline application), templates for deterministic and probabilistic results, and an important file called `abadi-mt.ttf` which users need to install on their computers to ensure the correct font (Abadi) is used by the application.

## Usage
1. **Start the application:**
   ```bash
   python InterfaceLayout.py
   ```
2. **Navigate through the interface using the tabs to analyze risk scenarios.**

## License
This project is licensed under the GNU General Public License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments
We acknowledge the developers of OpenQuake for their foundational platform and the community for their continuous support and contributions.

Special thanks to the Universidad de La Sabana for funding and overseeing the project. Although the moral rights of the product belong to me (Daniela Novoa Ramirez), the project was developed under the supervision and investment of Universidad de La Sabana.

Additionally, we recognize the contributions of Universidad de Medellín and Universidad Militar Nueva Granada for their involvement in generating risk models and developing the codes used by the platform.

