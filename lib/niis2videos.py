from parse_data import *
from build_seq import *

# NOTE:Usage:
# Search sequence data and copy to new file path
# Slice nii-data and save to png
# Make sequence video

# VIDEO_SIZE = (255, 255)
# SRC_DIRS = [
#     "./mri/p0AD", 
#     "./mri/p0CN", 
#     "./mri/p0EMCI", 
#     "./mri/p0LMCI", 
#     "./mri/p0MCI", 
#     "./mri/p0SMC"
# ]
# DST_DIR = "./mri_seq"
# TEMPLATE_VIDEO_PATH = "./template.mp4"
# VIDEOS_PATH = "./mri_seq_videos"

# for item in SRC_DIRS:
#     dataset = parse_preprocess_data(item, is_print=False)
#     sequences = search_sequence_data(dataset)
#     make_sequence_files(sequences, item, DST_DIR)

# param = parse_sample_video_param(TEMPLATE_VIDEO_PATH)
# make_sequence_videos(DST_DIR, param, VIDEO_SIZE)

# # Search video files and move to new dir
# move_videos_to_dir(DST_DIR, VIDEOS_PATH)

make_sequence_files_and_labels("./data/mri_seq_videos")
