# Correlation Heatmap Visualizer

## Description
An interactive view of a correlation heatmap for correlation analysis between assets.
You can choose between or upload multiple assets, select the period for display aswell as the window
for correlation computation and view the heatmap below.

## Setup
To run the visualizer, follow these steps:
1. Download the repository
2. a. On Windows, run the following commands in Git Bash (see following guides for installation of [Git Bash](https://git-scm.com/install/windows)):
   ```bash
   cd [Your path to the downloaded repo folder] # you may skip this step if you open Git Bash in the desired folder
   
   python -m venv venv # omit after initial setup
   source venv/Scripts/activate
   pip install -r requirements.txt # omit after initial setup
   
   streamlit run main.py
   ```
   
   b. On macOS, run the following commands in Terminal:
   ```bash
   cd [Your path to the downloaded repo folder]
   
   python -m venv venv # omit after initial setup
   source venv/bin/activate
   pip install -r requirements.txt # omit after initial setup
   
   streamlit run main.py
   ```

## Usage

### Select from available assets
1. In the top left, select the assets you want to compare from the list of available assets.
2. Below, select the start and end date. A chart of the history of the assets will be plotted in this window (not the correlation window yet).
You may see the history to the right.
3. Below the history chart, you may drag and drop the ends of the slider to select the correlation window.
You may see the window in the chart depicted by the highlighted area.
4. Below the slider, you may see the correlation heatmap. Hover over the different rectangles to see the precise
correlation value.

### Upload own files