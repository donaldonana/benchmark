import os
import csv
import json
import pandas as pd


def csv_save(output, headers, data) -> None:
    """_summary_

    Args:
        output (string): _description_
        headers (list): _description_
        data (dict): _description_
    """
    with open(output, 'w', newline='') as csvfile:
        file = csv.DictWriter(csvfile, fieldnames=headers)
        file.writeheader()

        for item in data:
            file.writerow({
                key : val for key, val in list(item.items())
            })
            
    print(f"{output}.csv succesfully save")

 
def metric_precess(output, headers) -> None:
     
    data = []
    buffer = ""
    brace_count = 0
    
    with open('result/result.txt', 'r') as file:
        log_content = file.read()
        
    for char in log_content:
        buffer += char
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        if brace_count == 0 and buffer.strip():
            try:
                data.append(json.loads(buffer.strip()))
                buffer = ""
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                buffer = ""

    csv_save(output, headers, data)
    
 
def process_cpu_energy_meter(output, headers, directory) -> None:
     
    data = list()
    item = dict()
    
    # for each subfolder in Energy folder (1Mb.JPEG)
    for dir in os.listdir("result/energy"):
        dir_path = os.path.join("result/energy", dir)
        image = dir.replace(".JPEG", "")

        for file in os.listdir(dir_path):  
            file_path = os.path.join(dir_path, file)
            model = file.replace(image+".JPEG.txt", "")
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    key, val = line.split('=')
                    item[key] = val
                else:
                    if item:
                        item["image"], item["model"] = image, model
                        data.append(item)
                        item = {}
                        
    csv_save(output, headers, data)
    
    

if __name__ == "__main__":
    
    # Define CSV headers for others data proc. 
    headers = [
        "label", 
        "prediction_time", 
        "index", 
        "image", 
        "model", 
        "download_time", 
        "model_size", 
        "model_load_time", 
        "prob"
    ]
    
    metric_precess("result/result.csv", headers)
    
    headers = [
        'duration_seconds', 
        'cpu0_package_joules', 
        'cpu0_dram_joules', 
        'cpu0_core_joules', 
        'image', 
        'model',
        'cpu_count' 
    ]
    
    process_cpu_energy_meter("result/energy.csv", headers, "energy")


    

    

