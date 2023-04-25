import os
import glob
import pandas as pd

# display ascii art logo
with open('logo.txt', 'r', encoding='utf-8') as file:
    art = file.read()
print(art)

# function to get video metadata
def get_metadata(path):
    # scan for video files
    video_files = glob.glob(os.path.join(path, '*.mp4')) + \
                  glob.glob(os.path.join(path, '*.avi')) + \
                  glob.glob(os.path.join(path, '*.mov')) + \
                  glob.glob(os.path.join(path, '*.mts'))

    metadata = []
    framerates = set()
    for file in video_files:
        # get video metadata
        fps_string = os.popen(f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate {file}').read().strip()
        fps_parts = fps_string.split('/')
        if len(fps_parts) == 2:
            fps = float(fps_parts[0]) / float(fps_parts[1])
        else:
            fps = float(fps_string)
        duration = float(os.popen(f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=duration {file}').read())
        metadata.append({
            'file': file,
            'fps': fps,
            'duration': duration
        })
        framerates.add(fps)

    # check for multiple framerates
    if len(framerates) > 1:
        print("Note: It is advised to keep video files with different framerates in separate folders for this program to work best.")

    return metadata

# function to convert timecode string to frame number
def timecode_to_frame(timecode, fps):
    h, m, s, f = map(int, timecode.split(':'))
    return (h * 3600 + m * 60 + s) * fps + f

# function to convert frame number to timecode string
def frame_to_timecode(frame, fps):
    total_seconds = int(frame // fps)
    h, m, s = total_seconds // 3600, (total_seconds // 60) % 60, total_seconds % 60
    f = int(frame % fps)
    return f'{h:02d}:{m:02d}:{s:02d}:{f:02d}'

# get folder path from user input
print("Note: Spaces in folder names can cause errors.")
path = input('Enter folder path: ')
print("Scanning folder, please wait...")

# get video metadata
metadata = get_metadata(path)

# get start timecode from user input
start_timecode = input('Enter start timecode (HH:MM:SS:FF). Press enter for 00:00:00:00: ')

# check if start timecode is empty and set default value
if not start_timecode:
    start_timecode = '00:00:00:00'

# ask user for output file name and location
print('Where would you like to save the output excel file?')
output_path = input('Enter a file path, or leave blank to save in the same location as the video files: ')
output_file = input('Enter a file name for the output excel file (excluding file extension): ')

# create pandas dataframe to store results
df = pd.DataFrame(columns=['File', 'Timecode In', 'Timecode Out', 'Scene Number', 'Shot Number', 'Usable'])

# process each video file
for i, file_metadata in enumerate(metadata):
    # get file name and metadata
    file = file_metadata['file']
    fps = file_metadata['fps']
    duration = file_metadata['duration']

    # calculate timecode in and timecode out
    if i == 0:
        timecode_in = start_timecode
    else:
        timecode_in = df.loc[i-1, 'Timecode Out']
    frame_in = timecode_to_frame(timecode_in, fps)
    frame_out = frame_in + duration * fps
    timecode_out = frame_to_timecode(frame_out, fps)

    # add row to dataframe
    if output_path:
        file_name = os.path.basename(file) if output_file_path else file
        file_path = os.path.join(output_path, file_name + '.xlsx')
    else:
        file_path = os.path.splitext(file)[0] + '.xlsx'
    df.loc[i] = [file_path, timecode_in, timecode_out, '', '', '']

# save dataframe to excel file
if output_path:
    file_path = os.path.join(output_path, output_file + '.xlsx')
else:
    file_path = os.path.join(path, output_file + '.xlsx')
df.to_excel(file_path, index=False)

print(f"Output file saved to {file_path}")
