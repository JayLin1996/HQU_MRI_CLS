import os
import shutil

def parse_single_data(path, idx):
    mark1_index = path.index("_")
    mark2_index = mark1_index + 2
    mark3_index = path.index("MRI")
    try:
        container = {
            "idx": idx, 
            "disease": path[:mark1_index], 
            "sex": path[mark1_index + 1], 
            "timestep": int(path[mark2_index:mark3_index].replace("_", "")),
            "patient": path[path.index("S_"):path.index("_MR_")], 
            "path": path
        }
        return container
    except (ValueError, TypeError):
        print("data error")
        return None

def parse_all_data(file_dir, order_timestep=True):
    """
    TODO age
    TODO id
    """
    dataset = list()
    for idx, path in enumerate(os.listdir(file_dir)):
        try:
            container = parse_single_data(path, idx)
            dataset.append(container)
            print("[INFO] idx:{}, disease:{}, sex:{}, timestep:{}, patient:{}, path:{}".format(
                container.get("idx"),
                container.get("disease"), 
                container.get("sex"), 
                container.get("timestep"), 
                container.get("patient"), 
                container.get("path")))
        except (ValueError, TypeError):
            continue
    if order_timestep:
        dataset = sorted(dataset, key=lambda obj:obj["timestep"])
    
    print("[INFO] sorted by timestep...")

    for container in dataset:
        print("[INFO] idx:{}, disease:{}, sex:{}, timestep:{}, patient:{}, path:{}".format(
                    container.get("idx"),
                    container.get("disease"), 
                    container.get("sex"), 
                    container.get("timestep"), 
                    container.get("patient"), 
                    container.get("path"))
        )

def parse_src_data(file_dir, order_timestep=True):
    """
    TODO age
    TODO id
    """
    container = dict()
    dataset = list()
    for idx, path in enumerate(os.listdir(file_dir)):
        try:
            mark1_index = path.index("_")
            mark2_index = mark1_index + 2
            mark3_index = path.index("MRI")
            container = {
                "idx": idx, 
                "disease": path[:mark1_index], 
                "sex": path[mark1_index + 1], 
                "timestep": int(path[mark2_index:mark3_index].replace("_", "")),
                "patient": path[path.index("S_"):path.index("_MR_")], 
                "path": path
            }
            dataset.append(container)
            print("[INFO] idx:{}, disease:{}, sex:{}, timestep:{}, patient:{}, path:{}".format(
                container.get("idx"),
                container.get("disease"), 
                container.get("sex"), 
                container.get("timestep"), 
                container.get("patient"), 
                container.get("path")
                )
            )

        except (ValueError, TypeError):
            continue
    
    # Sort by timestep
    if order_timestep:
        dataset = sorted(dataset, key=lambda obj:obj["timestep"])
    
    print("[INFO] sorted by timestep...")
    for container in dataset:
        print("[INFO] idx:{}, disease:{}, sex:{}, timestep:{}, patient:{}, path:{}".format(
                    container.get("idx"),
                    container.get("disease"), 
                    container.get("sex"), 
                    container.get("timestep"), 
                    container.get("patient"), 
                    container.get("path")
                )
            )

def parse_preprocess_data(file_dir, order_timestep=True, is_print=True):
    """
    Data info container
    TODO age
    TODO id
    """
    container = dict()
    dataset = list()
    for idx, path in enumerate(os.listdir(file_dir)):
        try:
            mark1_index = path.index("_")
            mark2_index = mark1_index + 2
            mark3_index = path.index("MRI")

            container = {
                "idx": idx, 
                "disease": path[:mark1_index], 
                "sex": path[mark1_index + 1], 
                "timestep": int(path[mark2_index:mark3_index].replace("_", "")),
                "patient": path[path.index("S_"):path.index("_MR_")], 
                "path": path
            }

            dataset.append(container)

            if not is_print:
                continue

            print("[INFO] idx:{}, disease:{}, sex:{}, timestep:{}, patient:{}, path:{}".format(
                container.get("idx"),
                container.get("disease"), 
                container.get("sex"), 
                container.get("timestep"), 
                container.get("patient"), 
                container.get("path"))
            )

        except (ValueError, TypeError):
            continue

    if order_timestep:
        dataset = sorted(dataset, key=lambda obj:obj["timestep"])
    
    if is_print:
        print("[INFO] sorted by timestep...")

    for container in dataset:
        if not is_print:
            continue
        print("[INFO] idx:{}, disease:{}, sex:{}, timestep:{}, patient:{}, path:{}".format(
                    container.get("idx"),
                    container.get("disease"), 
                    container.get("sex"), 
                    container.get("timestep"), 
                    container.get("patient"), 
                    container.get("path"))
                )
    return dataset

def search_sequence_data(dataset):
    """
    Search same patient MRI info.
    """
    # Grab all patients.
    patients = list()
    for container in dataset:
        patients.append(container.get("patient"))
    
    patients = set(patients)
    print("[INFO] total patients:{}\n{}".format(len(patients), patients))

    # Grab per patient's sequence data
    sequences = list()
    for patient in patients:

        paths = list()
        disease = None
        for container in dataset:
            if container.get("patient") == patient:
                paths.append(container.get("path"))
                disease = container.get("disease")

        sequence = {
            "patient": patient, 
            "disease": disease, 
            "paths": paths
        }
        print("[INFO] patient:{}, disease:{}, sequences:\n{}".format(
            sequence.get("patient"), 
            sequence.get("disease"), 
            sequence.get("paths"))
            )

        sequences.append(sequence)

    return sequences

def make_sequence_files(sequences, src_dir, save_dir):

    if src_dir[-1] != "/":
        src_dir = src_dir + "/"

    if save_dir[-1] != "/":
        save_dir = save_dir + "/"

    for sequence in sequences:
        # Create sequence fold
        file_dir = "{}{}_{}/".format(save_dir, sequence.get("patient"), sequence.get("disease"))
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            print("[INFO] make fold:{}".format(file_dir))
        
        # Copy sequence to the fold from source
        for path in sequence.get("paths"):
            shutil.copyfile(src_dir+path, file_dir+path)
            print("[INFO] copy file [{}] to [{}]".format(src_dir+path, file_dir+path))
