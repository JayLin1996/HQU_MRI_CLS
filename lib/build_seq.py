import cv2
from dataset_nii import *
import shutil
import csv

def parse_sample_video_param(file_dir):
    """
    For test dataset video param.
    """
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    cap = cv2.VideoCapture(file_dir)
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    param = {
        "fourcc": fourcc, 
        "cap": cap, 
        "fps": fps
    }

    print("[INFO] input video size: {}, fps: {}".format(size, param.get("fps")))
    cap.release()

    return param
    
def images2video(file_dir, size, param):
    """
    Images to video.
    """
    if file_dir[-1] != "/":
        file_dir = file_dir + "/"
    # Make video name
    file_name = "{}{}.mp4".format(file_dir, file_dir.split("/")[-2])
    writer = cv2.VideoWriter(file_name, param.get("fourcc"), param.get("fps"), size)

    for path in os.listdir(file_dir):
        png = path.split(".")[-1]
        if png != "png":
            continue
        # Read slice data
        full_path = os.path.join(file_dir, path)
        image = cv2.imread(full_path)
        frame = cv2.resize(image, size)
        writer.write(frame)
    # Release buffer
    writer.release()
    cv2.destroyAllWindows()

def images_to_sequence_video(file_dir, video_name, size, param, nii_slices_num=100000):
    """
    Images to sequence video.
    Input must be "./root_dir/file_dir/images_dir"
    """
    # Make video name
    file_name = "{}/{}.mp4".format(file_dir, video_name)
    writer = cv2.VideoWriter(file_name, param.get("fourcc"), param.get("fps"), size)
    if file_dir[-1] != "/":
        file_dir = file_dir + "/"
    # Grab all slices files
    all_container_files = list()
    for path in os.listdir(file_dir):
        # Grab nii file name
        # If can not find nii-data, do nothing
        # NOTE:full_path is "./mri_seq/S_4769_p0LMCI/xxx/"
        full_path = os.path.join(file_dir, path)
        if not os.path.isdir(full_path):
            continue
        # Grab per-nii-data slices
        image_container_files = list()
        for image_idx, image_file in enumerate(os.listdir(full_path)):
            # Filter not png file
            png = image_file.split(".")[-1]
            if png != "png":
                continue
            # Read slice data
            full_image_file = os.path.join(full_path, image_file)
            print(full_image_file, ", ", image_idx)
            image = cv2.imread(full_image_file)
            frame = cv2.resize(image, size)
            container = {
                "idx": image_idx, 
                "frame": frame
            }
            image_container_files.append(container)
        all_container_files.append(image_container_files)
    # Merge all sequence into video
    for idx in range(nii_slices_num):
        for image_container_list in all_container_files:
            for image_container in image_container_list:
                    if image_container.get("idx") == idx:
                        writer.write(image_container.get("frame"))
                        break
    # Release buffer
    writer.release()
    cv2.destroyAllWindows()

def make_videos(root_dir, size, param):
    # Grab assets dir by nii file
    if root_dir[-1] != "/":
        root_dir = root_dir + "/"

    for file_dir in os.listdir(root_dir):
        # NOTE:full_file_dir is "./mri_seq/S_4769_p0LMCI"
        full_file_dir = os.path.join(root_dir, file_dir)
        # Make slice-images
        save_batch_to_png(full_file_dir)
        for path in os.listdir(full_file_dir):
            # Grab nii file name
            # If can not find nii-data, do nothing
            if os.path.isdir(full_file_dir):
                continue
            nii_file_name = path.split(".")[0]
            # NOTE:full_path is "./mri_seq/S_4769_p0LMCI/xxx/"
            full_path = os.path.join(root_dir, file_dir, nii_file_name)
            # Make video
            images2video(full_path, param, size)

def make_sequence_videos(root_dir, param, size):
    # Grab assets dir by nii file
    if root_dir[-1] != "/":
        root_dir = root_dir + "/"

    for file_dir in os.listdir(root_dir):
        # NOTE:full_file_dir is "./mri_seq/S_4769_p0LMCI"
        full_file_dir = os.path.join(root_dir, file_dir)
        if not os.path.isdir(full_file_dir):
            continue
        # Make slice-images
        save_batch_to_png(full_file_dir)
        images_to_sequence_video(full_file_dir, file_dir, size, param)

def move_videos_to_dir(src_dir, dst_dir):
    if src_dir[-1] != "/":
        src_dir = src_dir + "/"
    
    if dst_dir[-1] != "/":
        dst_dir = dst_dir + "/"

    for path in os.listdir(src_dir):
        full_path = os.path.join(src_dir, path)
        # NOTE:src_video_path is ./mri_seq/S_0021_p0CN/S_0021_p0CN.mp4
        src_video_path = "{}/{}.mp4".format(full_path, path)
        # NOTE:dst_video_path is ./mri_seq_videos//S_0021_p0CN.mp4
        dst_video_path = "{}/{}.mp4".format(dst_dir, path)
        shutil.copyfile(src_video_path, dst_video_path)

def make_sequence_files_and_labels(file_dir, split_rate=[0.6, 0.2, 0.2]):
    """
    Make dataset paths and labels csv files.
    Split files into train-set, test-set, val-set csv files by rate.
    """
    if file_dir[-1] != "/":
        file_dir = file_dir + "/"

    file_name = "{}data.csv".format(file_dir)
    file = open(file_name, "w", newline="")
    wirter = csv.writer(file, delimiter=" ")
 
    data_set = list()
    total = 0
    for i, path in enumerate(os.listdir(file_dir)):
        if path.split(".")[-1] != "mp4":
            continue
        full_path = os.path.join(file_dir, path)
        file_name = path.split(".")[0]
        class_name = file_name.split("_")[-1]
        print("[INFO] id:{}, class name:{}".format(i, class_name))
        data_set.append((full_path, class_name))
        total = total + 1
        wirter.writerow((full_path, class_name))
    

    file_name = "{}train.csv".format(file_dir)
    train_set = open(file_name, "w", newline="")
    train_wirter = csv.writer(train_set, delimiter=" ")

    file_name = "{}test.csv".format(file_dir)
    test_set = open(file_name, "w", newline="")
    test_wirter = csv.writer(test_set, delimiter=" ")

    file_name = "{}val.csv".format(file_dir)
    val_set = open(file_name, "w", newline="")
    val_wirter = csv.writer(val_set, delimiter=" ")

    train_total = int(total * split_rate[0])
    test_total = int(total * split_rate[1])
    val_total = int(total * split_rate[2])

    for idx in range(0, train_total):
        train_wirter.writerow(data_set[idx])
    for idx in range(train_total, train_total+test_total):
        test_wirter.writerow(data_set[idx])
    for idx in range(train_total+test_total, train_total+test_total+val_total):
        val_wirter.writerow(data_set[idx])

    file.close()
    train_set.close()
    test_set.close()
    val_set.close()
