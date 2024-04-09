import os.path

import cv2
import mediapipe as mp
import numpy as np
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import TensorBoard
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.models import Sequential

from comp_vision import actions, nr_videos, nr_frames_video, path

holisitic_model = mp.solutions.holistic
drawing_utils = mp.solutions.drawing_utils


def access_camera():
    capture = cv2.VideoCapture(0)
    with holisitic_model.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as model:
        while capture.isOpened():
            _, frame = capture.read()
            img, res = process_frame(frame, model)
            show_keypoints(img, res)
            cv2.imshow('Feed', img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        capture.release()
        cv2.destroyAllWindows()


def process_frame(frame, mp_model):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img.flags.writeable = False
    results = mp_model.process(img)
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img, results


def show_keypoints(img, processed_img):
    circle_style = drawing_utils.DrawingSpec(color=(0, 0, 0), thickness=1, circle_radius=10)
    line_style = drawing_utils.DrawingSpec(color=(255, 255, 255), thickness=1, circle_radius=7)
    drawing_utils.draw_landmarks(img, processed_img.left_hand_landmarks, holisitic_model.HAND_CONNECTIONS, circle_style,
                                 line_style)
    drawing_utils.draw_landmarks(img, processed_img.right_hand_landmarks, holisitic_model.HAND_CONNECTIONS,
                                 circle_style, line_style)


def get_left_keypoint_coords(res):
    if not res.left_hand_landmarks:
        return np.zeros(21 * 3)
    return np.array([[r.x, r.y, r.z] for r in res.left_hand_landmarks.landmark]).flatten()


def get_right_keypoint_coords(res):
    if not res.right_hand_landmarks:
        return np.zeros(21 * 3)
    return np.array([[r.x, r.y, r.z] for r in res.right_hand_landmarks.landmark]).flatten()


def collect_data():
    capture = cv2.VideoCapture(0)
    with holisitic_model.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as model:
        for act in actions:
            for v in range(nr_videos):
                for f in range(nr_frames_video):
                    _, frame = capture.read()
                    img, res = process_frame(frame, model)
                    show_keypoints(img, res)

                    if f == 0:
                        cv2.putText(img, 'Start', (120, 200), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
                        cv2.putText(img, 'Action {}'.format(act), (15, 12), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 255),
                                    1, cv2.LINE_AA)
                        cv2.imshow('Feed', img)
                        cv2.waitKey(2000)
                    else:
                        cv2.putText(img, 'Action {}'.format(act), (15, 12), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 255),
                                    1, cv2.LINE_AA)
                        cv2.imshow('Feed', img)

                    left_keypts = get_left_keypoint_coords(res)
                    right_keypts = get_right_keypoint_coords(res)
                    all_keypts = np.concatenate((left_keypts, right_keypts))
                    np_path = os.path.join(path, act, str(v), str(f))
                    np.save(np_path, all_keypts)

                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break
    capture.release()
    cv2.destroyAllWindows()


def preprocess_data():
    label_mapping = {label: nr for nr, label in enumerate(actions)}
    videos, labels = [], []
    for act in actions:
        for v in range(nr_videos):
            window = []
            for f in range(nr_frames_video):
                res = np.load(os.path.join(path, act, str(v), "{}.npy".format(f)))
                window.append(res)
            videos.append(window)
            labels.append(label_mapping[act])

    videos = np.array(videos)
    categorical_labels = to_categorical(labels).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(videos, categorical_labels, test_size=0.1)
    return X_train, X_test, y_train, y_test


def model():
    X_train, X_test, y_train, y_test = preprocess_data()
    tb_callback = TensorBoard(log_dir=os.path.join('logs'))

    model = Sequential()
    model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30, 1662)))
    model.add(LSTM(128, return_sequences=True, activation='relu'))
    model.add(LSTM(64, return_sequences=False, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(actions.shape[0], activation='softmax'))

    model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
    model.fit(X_train, y_train, epochs=2000, callbacks=[tb_callback])
    # res = model.predict(X_test)
    # actions[np.argmax(res[0])]
    # actions[np.argmax(y_test[0])]
    model.save('actions.hS')
    model.load_weights('actions.hS')


if __name__ == '__main__':
    collect_data()
