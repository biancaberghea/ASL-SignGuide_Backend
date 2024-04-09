import json
import os

import cv2
import mediapipe as mp
import numpy as np

from comp_vision import train_path, test_path, val_path

with open('../WLASL_v0.3.json', 'r') as file:
    data = json.load(file)


def process_videos():
    videos_path = '../videos'

    for i in range(len(data)):
        gloss = data[i]['gloss']
        instances = data[i]['instances']
        for inst in instances:
            video_id = inst['video_id']
            inst_path = os.path.join(videos_path, f'{video_id}.mp4')
            split = inst['split']

            extract_keypoints(gloss, video_id, inst_path, split)


def get_keypoints(result):
    if not result.left_hand_landmarks:
        left = np.zeros(21 * 3)
    else:
        left = np.array([[r.x, r.y, r.z] for r in result.left_hand_landmarks.landmark]).flatten()
    if not result.right_hand_landmarks:
        right = np.zeros(21 * 3)
    else:
        right = np.array([[r.x, r.y, r.z] for r in result.right_hand_landmarks.landmark]).flatten()
    return np.concatenate((left, right))


def extract_keypoints(gloss, video_id, video_path, split):
    if split == 'train':
        split_dir = train_path
    elif split == 'test':
        split_dir = test_path
    else:
        split_dir = val_path

    if not os.path.exists(os.path.join(split_dir, gloss)):
        os.makedirs(os.path.join(split_dir, gloss))

    holisitic = mp.solutions.holistic
    capture = cv2.VideoCapture(video_path)

    with holisitic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holisitic_model:
        frame_keypoints = []
        while capture.isOpened():
            ret, frame = capture.read()
            if ret:
                result = holisitic_model.process(frame)
                keypoints = get_keypoints(result)
                frame_keypoints.append(keypoints)
            else:
                break
        np_path = os.path.join(split_dir, gloss, str(video_id))
        np.save(np_path, frame_keypoints)

        capture.release()
        cv2.destroyAllWindows()


def get_max_shape(split):
    split_dir = os.path.join(f'../{split}')
    words = os.listdir(split_dir)

    max_shape = 0
    for word in words:
        word_dir = os.path.join(split_dir, word)
        video_ids = os.listdir(word_dir)
        for video_id in video_ids:
            file_path = os.path.join(split_dir, word, video_id)
            keypoints = np.load(file_path)
            if keypoints.shape == (0,):
                os.remove(file_path)
            elif keypoints.shape[0] > max_shape:
                max_shape = keypoints.shape[0]
    return max_shape


def pad_keypoints(split):
    split_dir = os.path.join(f'../{split}')
    words = os.listdir(split_dir)

    max_shape = get_max_shape(split)

    for word in words:
        word_dir = os.path.join(split_dir, word)
        video_ids = os.listdir(word_dir)
        for video_id in video_ids:
            file_path = os.path.join(split_dir, word, video_id)
            keypoints = np.load(file_path)
            padded_keypoints = np.pad(keypoints, ((0, max_shape - keypoints.shape[0]), (0, 0)), mode='constant',
                                      constant_values=0)
            np.save(file_path, padded_keypoints)

    print('done')


if __name__ == '__main__':
    pad_keypoints('train')
    pad_keypoints('test')
    pad_keypoints('val')
