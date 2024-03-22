import os
import glob
import pandas as pd
import colorama
from colorama import Fore, Back, Style

# display ascii art logo
with open('logo.txt', 'r', encoding='utf-8') as file:
    art = file.read()
print(Fore.MAGENTA + art)
print(Style.RESET_ALL + 'Version 1.1.0\n')

# function to get video metadata
def get_metadata(path):
    # scan for video files
    video_files = glob.glob(os.path.join(path, '*.mp4')) + \
                  glob.glob(os.path.join(path, '*.MP4')) + \
                  glob.glob(os.path.join(path, '*.avi')) + \
                  glob.glob(os.path.join(path, '*.AVI')) + \
                  glob.glob(os.path.join(path, '*.mov')) + \
                  glob.glob(os.path.join(path, '*.MOV')) + \
                  glob.glob(os.path.join(path, '*.mpg')) + \
                  glob.glob(os.path.join(path, '*.MPG'))

    # Sort files by creation time
    video_files.sort(key=os.path.getctime)

    metadata = []
    framerates = []
    for file in video_files:
        # get video metadata
        fps_string = os.popen(f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=r_frame_rate "{file}"').read().strip()
        fps_parts = fps_string.split('/')
        if len(fps_parts) == 2:
            fps = float(fps_parts[0]) / float(fps_parts[1])
        else:
            if '\n' in fps_string:
                fps_list = []
                for x in fps_string.split('\n'):
                    x = x.strip()
                    try:
                        fps_list.append(float(x))
                    except ValueError:
                        print(f"Error: could not convert '{x}' to float for file '{file}'")
                if len(fps_list) == 0:
                    fps = None
                elif len(fps_list) == 1:
                    fps = fps_list[0]
                else:
                    fps = sum(fps_list) / len(fps_list)
            else:
                try:
                    fps = float(fps_string)
                except ValueError:
                    print(f"Error: could not convert '{fps_string}' to float for file '{file}'")
                    fps = None
        duration_string = os.popen(f'ffprobe -v error -select_streams v -of default=noprint_wrappers=1:nokey=1 -show_entries stream=duration "{file}"').read()
        try:
            duration = float(duration_string.strip())
        except ValueError:
            duration_parts = duration_string.strip().split('\n')
            duration_list = [float(x) for x in duration_parts if x.strip()]
            if len(duration_list) == 0:
                duration = None
            elif len(duration_list) == 1:
                duration = duration_list[0]
            else:
                duration = sum(duration_list) / len(duration_list)
            if duration is None:
                print(f"Error: could not convert '{duration_string}' to float for file '{file}'")

        if fps is not None and duration is not None:
            metadata.append({
                'file': file,
                'fps': fps,
                'duration': duration
            })
            framerates.append(fps)

    # check for multiple framerates
    if len(set(framerates)) > 1:
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
df = pd.DataFrame(columns=['Director', 'Producer', 'DOP', 'File', 'Roll', 'Scene', 'Slate', 'Take', 'Comments', 'Timecode In', 'Timecode Out', 'Usable'])

## process each video file
for i, file_metadata in enumerate(metadata):
    # get file name and metadata
    file = os.path.basename(file_metadata['file'])
    fps = file_metadata['fps']
    duration = file_metadata['duration']

    # calculate timecode in and timecode out
    if i == 0:
        timecode_in = start_timecode
    else:
        # Adjusting the timecode in by one frame ahead of the previous row's timecode out
        frame_offset = 1 if i != 0 else 0
        timecode_in = frame_to_timecode(timecode_to_frame(df.loc[i - 1, 'Timecode Out'], fps) + frame_offset, fps)
    frame_in = timecode_to_frame(timecode_in, fps)
    frame_out = frame_in + duration * fps
    timecode_out = frame_to_timecode(frame_out, fps)

    # add row to dataframe
    if output_path:
        file_path = os.path.join(output_path, f'{file}.xlsx')
    else:
        file_path = os.path.splitext(file_metadata['file'])[0] + '.xlsx'
    df.loc[i] = ['', '', '', file, '', '', '', '', '', timecode_in, timecode_out, '']

# save dataframe to excel file
if output_path:
    file_path = os.path.join(output_path, f'{output_file}.xlsx')
else:
    file_path = os.path.join(path, f'{output_file}.xlsx')
df.to_excel(file_path, index=False)

print(f"Output file saved to {file_path}")
