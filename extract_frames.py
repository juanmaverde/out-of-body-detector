import cv2
import os
import argparse

'''
modified by Juan Verde

source: (c) Research Group CAMMA, University of Strasbourg, IHU Strasbourg, France
Website: http://camma.u-strasbg.fr
'''

def extract_frames(video_path, output_folder, start_frame, end_frame):
    video_in = cv2.VideoCapture(video_path)
    video_nframes = int(video_in.get(cv2.CAP_PROP_FRAME_COUNT))

    if end_frame < start_frame:
        print("error: end frame can't be less than start frame")
        return

    if start_frame < 0 or end_frame >= video_nframes:
        print("invalid start | end frame")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    for i in range(start_frame, end_frame):
        video_in.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = video_in.read()
        if not ret:
            print(f"error: could not read frame {i}")
            break
        output_path = os.path.join(output_folder, f"{video_name}_{i:06d}.png")
        cv2.imwrite(output_path, frame)

    video_in.release()
    print(f"extracted frames from {start_frame} to {end_frame} into {output_folder}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='extract frames from a video file.')
    parser.add_argument('video_path', type=str, help='path to the video file')
    parser.add_argument('output_folder', type=str, help='path to the output folder')
    parser.add_argument('--start_frame', type=int, default=0, help='frame number to start extraction (default: 0)')
    parser.add_argument('--end_frame', type=int, help='frame number to end extraction (default: last frame of the video)')

    args = parser.parse_args()

    video_path = args.video_path
    output_folder = args.output_folder
    start_frame = args.start_frame
    end_frame = args.end_frame

    if end_frame is None:
        video_in = cv2.VideoCapture(video_path)
        end_frame = int(video_in.get(cv2.CAP_PROP_FRAME_COUNT))
        video_in.release()

    extract_frames(video_path, output_folder, start_frame, end_frame)

# python extract_frames.py <video_path> <output_folder> [--start_frame START_FRAME] [--end_frame END_FRAME]
