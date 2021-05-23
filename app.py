import av
import cv2
from keras.models import model_from_json
from string import ascii_uppercase
import numpy as np
import operator
import os
import streamlit as st
from PIL import Image
import time
from streamlit_webrtc import (
    ClientSettings,
    VideoTransformerBase,
    WebRtcMode,
    webrtc_streamer,
)

WEBRTC_CLIENT_SETTINGS = ClientSettings(
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": True},
)


def main():
    st.header("Sign Language Recognition using CNN")
    sign_to_text = "Real time gesture detection"
    loopback_page = "Simple video loopback (sendrecv)"

    app_mode = st.sidebar.selectbox(
        "Choose app mode",
        [sign_to_text,
         loopback_page],
    )
    st.subheader(app_mode)
    if app_mode == sign_to_text:
        app_sign_to_text()
    elif app_mode == loopback_page:
        app_loopback()


#  Mode 1

def app_sign_to_text():
    class Predictions(VideoTransformerBase):
        def __init__(self) -> None:

            self.json_file = open("models/model.json", "r")
            self.model_json = self.json_file.read()
            self.json_file.close()
            self.model = model_from_json(self.model_json)
            self.model.load_weights("models/model.h5")
            self.image_x = 128
            self.image_y = 128

            self.ct = {'blank': 0}
            self.blank_flag = 0
            for i in ascii_uppercase:
                self.ct[i] = 0
            self.sentence = ""
            self.word = ""
            self.current_symbol = "Empty"

        def transform(self, frame: av.VideoFrame) -> np.ndarray:
            img = frame.to_ndarray(format="bgr24")
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_crop = gray[50:250, 400:600]
            blur = cv2.GaussianBlur(gray_crop, (5, 5), 2)
            th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            self.signPrediction(res)
            cv2.rectangle(img, (400, 50), (600, 250), (0, 0, 255), 5)
            cv2.putText(img, self.current_symbol, (380, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.9, (255, 0, 0), 2)
            cv2.putText(img, "Word->" + self.word, (10, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, "Sentence->" + self.sentence, (10, 390), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return img

        def signPrediction(self, res):
            img2 = res.copy()
            img2 = cv2.resize(img2, (self.image_x, self.image_y))
            img2 = np.array(img2, dtype=np.float32)
            img2 = np.reshape(img2, (1, self.image_x, self.image_y, 1))

            result = self.model.predict(img2)
            prediction = {}
            inde = 1
            prediction['blank'] = result[0][0]
            for i in ascii_uppercase:
                prediction[i] = result[0][inde]
                inde += 1

            prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)
            self.current_symbol = prediction[0][0]
            if self.current_symbol == 'blank':
                for i in ascii_uppercase:
                    self.ct[i] = 0
            self.ct[self.current_symbol] += 1
            if self.ct[self.current_symbol] > 45:
                for i in ascii_uppercase:
                    if i == self.current_symbol:
                        continue
                    tmp = self.ct[self.current_symbol] - self.ct[i]
                    if tmp < 0:
                        tmp *= -1
                    if tmp <= 5:
                        self.ct['blank'] = 0
                        for i in ascii_uppercase:
                            self.ct[i] = 0
                        return
                self.ct['blank'] = 0
                for i in ascii_uppercase:
                    self.ct[i] = 0
                if self.current_symbol == 'blank':
                    if self.blank_flag == 0:
                        self.blank_flag = 1
                        if len(self.sentence) > 0:
                            self.sentence += " "
                        self.sentence += self.word
                        self.word = ""
                else:
                    self.blank_flag = 0
                    self.word += self.current_symbol

        # return prediction[0][0]

    pred = Predictions()
    webrtc_ctx = webrtc_streamer(
        key="object-detection",
        mode=WebRtcMode.SENDRECV,
        client_settings=WEBRTC_CLIENT_SETTINGS,
        video_transformer_factory=Predictions,
        async_transform=True,
    )


# MODE 2
def play_image(char):
    path = "images"
    p1 = "gestures"
    if (char == " "):
        final = os.path.join(path, p1, "0.jpg")
    else:
        final = os.path.join(path, p1, char + ".jpg")
    # print(final)
    gesture = Image.open(final)
    return gesture

#    Mode 3
def app_loopback():
    webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDRECV,
        client_settings=WEBRTC_CLIENT_SETTINGS,
        video_transformer_factory=None,  # NoOp
    )


if __name__ == "__main__":
    main()
