# Accelerated Two-Level Network Design Model (Training Version)

## Process on Google Colab

Step 1 - open a new Colab notebook in your browser, https://colab.research.google.com/

Step 2 - in the created file, clone the training-version branch, using the code below
```python
!git clone --branch training-version https://github.com/SEL-Columbia/accel_tlnd.git
%cd <repository_folder>
```

Step 3 - install the dependencies
```python
!pip install -r requirements.txt
```

Step 4 - Run the UI notebook:

For structure the merging process, 
```python
%run merging_ui.ipynb
```

or for two-level network design process, 
```python
%run accel_tlnd_ui.ipynb
```

## Merging process notes
- Input files: You can upload your local files into 'accel_tlnd/structure_merging_model/inputs', or use the provided sample files.
- Next, specify the output path where you would like to save your results.
- Adjust the parameters as needed.
- Click 'Run Merging' and wait for the process to complete. The results will be saved in the folder you specified.


## Accelerated Two-Level Network Design Notes

- Input files: Upload your local files to the `accel_tlnd/accel_tlnd_model/inputs` directory, or use the provided sample files.
- Specify the desired output path for saving your results.
- Adjust the analysis parameters as needed.
- Click 'Run Analysis' and wait for the process to finish. The results will be saved in the folder you specified.


## Save results
Files uploaded to Google Colab are stored temporarily and will be deleted once the session ends. Be sure to save your files before closing your browser. 

You can download folders or specific files using the left sidebar menu.  
Alternatively, you can save your results directly to your Google Drive.

```python
from google.colab import drive
drive.mount('/content/drive')
```

```python
!cp -r /content/accel_tlnd /content/drive/MyDrive/accel_tlnd_training_model
```
