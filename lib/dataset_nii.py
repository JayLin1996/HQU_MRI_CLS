import os
import nibabel as nib
import numpy as np
from skimage.transform import resize
from parse_data import parse_single_data
import imageio

def read_data(path):
    return nib.load(path).get_fdata()

def fix_data(data):
    width = data.shape[0]
    height = data.shape[1]
    depth = data.shape[2]
    data = resize(data, (width, height, depth))
    data = np.reshape(data, (width, height, depth))
    return data

def grab_nii_images(file_dir, size=None):
    """
    INSTRUCTIONS:
    Source data shape type->(w, h, d, 1) or (w, h, d)
    Params：
        dir：file dir
        size: (width, height, depth)
    Return:
        imgs: image list
    """
    imgs = list()
    print("[INFO] load data and transform...")

    for path in os.listdir(file_dir):
        # Check nii data
        nii = path.split(".")[-1]
        if nii != "nii":
            continue
        # Read nii data
        full_path = os.path.join(file_dir, path)
        data = read_data(full_path)
        # Fix the data format
        data = fix_data(data)
        if size is not None:
            img = resize(data, size)
            img = np.reshape(img, size)

        print("[INFO] file name:{}, \nload data shape:{}->img shape:{}".format(
            full_path, 
            data.shape, 
            img.shape)
            )

        imgs.append(img)

    print("[INFO] load data end...")
    return imgs

def grab_nii_images_and_labels(file_dir, size=None):
    """
    INSTRUCTIONS:
    Source data shape type->(w, h, d, 1) or (w, h, d)
    Params：
        dir：file dir
        size: (width, height, depth)
    Return:
        imgs: image list
        labs: label list
    """
    imgs = list()
    labs = list()
    print("[INFO] load data and transform...")
    for idx, path in enumerate(os.listdir(file_dir)):
        # Check nii data
        nii = path.split(".")[-1]
        if nii != "nii":
            continue
        # Read nii data
        full_path = os.path.join(file_dir, path)
        data = read_data(full_path)
        container = parse_single_data(path, idx)
        if container is None:
            continue
        # Fix the data format
        data = fix_data(data)
        if size is not None:
            img = resize(data, size)
            img = np.reshape(img, size)

        print("[INFO] file name:{}, label:{}, \nload data shape:{}->img shape:{}".format(
            full_path, 
            container.get("disease"), 
            data.shape, 
            img.shape)
            )

        imgs.append(img)
        labs.append(container.get("disease"))

    print("[INFO] load data end...")
    return imgs, labs

def array_to_nii(np_array, file_path):
    """
    The array must be 3D DATA format (h, w, d)
    The array dtype must be np.float64
    """
    image = nib.Nifti1Image(np_array, np.eye(4)) 
    nib.save(image, file_path)

def to_slices(data, dim=0):
    """
    The dim must be 0, 1, 2
    """
    if dim > 2:
        raise ValueError("dim wrong...")
    
    assert len(data.shape) == 3

    slices = list()
    for idx in range(data.shape[dim]):
        if dim == 0:
            slices.append(data[idx, :, :])
        elif dim == 1:
            slices.append(data[:, idx, :])
        else:
            slices.append(data[:, :, idx])

    return slices

def save_to_png(nii_image, file_dir):
    """
    Save nii image to slices to local.
    """
    slices = to_slices(nii_image)
    for i, slice in enumerate(slices):
        print("[INFO] write slice item:{}:".format(i))
        imageio.imwrite(os.path.join(file_dir, "slice{}.png".format(i)), slice)

def save_batch_to_png(file_dir):
    """
    Save batch nii images to local.
    """
    if file_dir[-1] != "/":
        file_dir = file_dir + "/"

    for path in os.listdir(file_dir):
        # Check nii data
        nii = path.split(".")[-1]
        if nii != "nii":
            continue
        # Read nii data
        full_path = os.path.join(file_dir, path)
        data = read_data(full_path)
        # Fix the data format
        data = fix_data(data)
        # Create slice-images dir in current dir
        images_dir = "{}{}/".format(file_dir, path.split(".")[0])
        print("[INFO] set to dir:{}".format(images_dir))
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        save_to_png(data, images_dir)
