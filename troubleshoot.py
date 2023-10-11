import tkinter as tk
from tkinter import filedialog
import pandas as pd

def process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
          
            # Main Script
            # Access the first cell in the 'officialCellCount' column
            first_cell_value = df['officialCellCount'].iloc[0]
            
            # Check if there's any number greater than 72 in the 'column_name'
            greater_than_72 = df['observedCellCount'] > first_cell_value
            
            # Check if any True values exist (i.e., if there's any number greater than 72)
            if greater_than_72.any():
                print("There is at least one oveserved cell count greater than the official cell count:",first_cell_value, "in the file.")
                exit()
            
            
            
            
            # Find rows where 'maxCellTemp' is greater than 150
            filtered_rows = df[df['maxCellTemp'] > 150]
            
            print('Rows with temps greater than 150 degrees:')
            # Iterate through the filtered rows
            for index, row in filtered_rows.iterrows():
                print(f"Row {index}:")
                
                # Iterate through columns containing 'cellt'
                for column in df.columns:
                    if 'cellt' in column:
                        # Check if the value in the column is greater than 150
                        if pd.notna(row[column]) and row[column] > 150:
                            print(f"  {column}: {row[column]}")
            
                            
            # Count the occurrences of each unique timestamp
            timestamp_counts = df['timestamp'].value_counts()
            
            # Check if any timestamp occurs 3 or fewer times
            rare_timestamps = timestamp_counts[timestamp_counts <= 3]
            
            # Convert the rare timestamps to a list or extract the values
            rare_timestamps_list = rare_timestamps.index.tolist()
            
            print("\nTimestamps occurring 3 or fewer times:")
            print(rare_timestamps_list)
            
            
            
            
            # Define thresholds for 'cellv' and 'cellt' columns
            threshold_cellv = 30  # Adjust this value for 'cellv'
            threshold_cellt = 5   # Adjust this value for 'cellt'
            
            # Define lists to store the indices of rows with erratic changes
            erratic_rows_cellv = []
            erratic_rows_cellt = []
            
            # Iterate through rows using a for loop starting from 0
            for index in range(len(df)):
                row = df.iloc[index]  # Get the row data
                for column in df.columns:
                    if 'cellv' in column:
                        current_value = row[column]
                        if index > 0:
                            previous_value = df.iloc[index - 1][column]
                            change = abs(current_value - previous_value)
                            if change > threshold_cellv:
                                erratic_rows_cellv.append(index)
                                break  # Exit inner loop for this row
                    elif 'cellt' in column:
                        current_value = row[column]
                        if index > 0:
                            previous_value = df.iloc[index - 1][column]
                            change = abs(current_value - previous_value)
                            if change > threshold_cellt:
                                erratic_rows_cellt.append(index)
                                break  # Exit inner loop for this row
            
            # Print rows with erratic changes in 'cellv'
            if erratic_rows_cellv:
                print("Rows with erratic changes in 'cellv' detected:")
                print(df.iloc[erratic_rows_cellv])
            
            # Print rows with erratic changes in 'cellt'
            if erratic_rows_cellt:
                print("Rows with erratic changes in 'cellt' detected:")
                print(df.iloc[erratic_rows_cellt])
            
            if not (erratic_rows_cellv or erratic_rows_cellt):
                print("No rows with erratic changes detected in 'cellv' or 'cellt'.")


        except Exception as e:
            result_label.config(text=f"Error: {str(e)}")
    else:
        result_label.config(text="No file selected")
# funtion to eppend text to text widget      
def append_to_text_widget(text):
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, text + '\n')
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)  # Scroll to the end to show the latest output

# function to clear the result label
def clear_result():
    result_label.config(text="")

# function to exit the application
def exit_app():
    root.destroy()

# function to show example data (optional)
def show_example_data():
    example_data = pd.DataFrame({"officialCellCount": [72, 72, 72],
                                "observedCellCount": [75, 70, 74],
                                "maxCellTemp": [152, 149, 153],
                                "timestamp": ["2023-10-11 10:00", "2023-10-11 10:01", "2023-10-11 10:02"]})
    text.config(state=tk.NORMAL)
    text.delete(1.0, tk.END)
    text.insert(tk.END, example_data.to_string(index=False))
    text.config(state=tk.DISABLED)

# main application window
root = tk.Tk()
root.title("CSV File Processor")

# button to select a CSV file
open_button = tk.Button(root, text="Select CSV File", command=process_csv)
open_button.pack(pady=10)

# label to display the processing result
result_label = tk.Label(root, text="")
result_label.pack()

# button to clear the result label
clear_button = tk.Button(root, text="Clear Result", command=clear_result)
clear_button.pack()

# button to exit the application
exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack()

# button to show example data (optional)
show_data_button = tk.Button(root, text="Show Example Data", command=show_example_data)
show_data_button.pack()

# text widget to display example data (optional)
text = tk.Text(root, wrap=tk.NONE, state=tk.DISABLED)
text.pack()

# Start the Tkinter main loop
root.mainloop()
