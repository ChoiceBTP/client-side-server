# from sklearn.model_selection import train_test_split

import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.utils import pad_sequences
import tensorflow as tf
import re
import random
import numpy as np
import keras
from keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(lower=True, split=' ')


class Inferrer:
    def __init__(self):
        """"""
        self.path = "./therapybot"
        self.model = keras.models.load_model(r"C:\Users\jhasa\Desktop\client-side-server\clientSideServer\clientApp\model.h5")
        self.lbl_enc = LabelEncoder()

        self.tokenizer = Tokenizer(lower=True, split=' ')
        with open(r'C:\Users\jhasa\Desktop\client-side-server\clientSideServer\clientApp\intents.json') as f:
            data = json.load(f)

        df = pd.DataFrame(data['intents'])
        dic = {"tag": [], "patterns": [], "responses": []}
        for i in range(len(df)):
            ptrns = df[df.index == i]['patterns'].values[0]
            rspns = df[df.index == i]['responses'].values[0]
            tag = df[df.index == i]['tag'].values[0]
            for j in range(len(ptrns)):
                dic['tag'].append(tag)
                dic['patterns'].append(ptrns[j])
                dic['responses'].append(rspns)

        self.df = pd.DataFrame.from_dict(dic)
        self.lbl_enc.fit(self.df['tag'])
        self.tokenizer.fit_on_texts(self.df['patterns'])
        # print(self.lbl_enc.get_params())

    def model_response(self, query):
        """hello"""
        text = []
        txt = re.sub('[^a-zA-Z\']', ' ', query)
        txt = txt.lower()
        txt = txt.split()
        txt = " ".join(txt)
        text.append(txt)
        print(txt)
        x_test = self.tokenizer.texts_to_sequences(text)
        x_test = np.array(x_test).squeeze()
        x_test = pad_sequences([x_test], padding='post', maxlen=18)
        y_pred = self.model.predict(x_test)
        y_pred = y_pred.argmax()
        print(y_pred)
        tag = self.lbl_enc.inverse_transform([y_pred])[0]
        print(tag)
        responses = self.df[self.df['tag'] == tag]['responses'].values[0]

        # print("you: {}".format(query))
        return random.choice(responses)
