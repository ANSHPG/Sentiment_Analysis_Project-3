# -*- coding: utf-8 -*-
"""Sentiment Analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tdMHTsXKvrHxLtc_cvJCQZFf-FKeccmN
"""

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'sentiment-analysis-dataset:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F989445%2F1808590%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240616%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240616T050339Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D16add6fdcac3fa49bc4a479776cea4aad40a04bb0bd5af86c6b5c6fb99033dc3044d9e21b1a17edd59fa998cd6269ca069e3e6ac8a2d0e123acf8596e1777bf4e8ba8b353998cd946302842d57ac3a8f0668ff7c3af7a82591d0c4a58d86ae1c2cf461a2c57823341aa22a598eac0b97a55d0e1fd02a28a4fd1608891ddfb77ffeab4fb32d807e9f4c9a774434a1dac70c5b0174351e25e45166abb77c1c4808a13529d2b7f31cc0c2b3a5b258d93a89d3b750bccde4301b7ac1320273737b8daaff2511b20b945ca085daaaedddce4196e5b3f4369923ab6bf754590e4b8d01da4a94c3110636e3046adeee3be73c530dc6b4913db2d04db90a87f9c2863713'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import layers

df = pd.read_csv('/kaggle/input/sentiment-analysis-dataset/train.csv', encoding='ISO-8859-1')

df.head(2)

print(df.shape)
print(df.isnull().sum())
print(df.duplicated().sum())
print(df.info)

df['sentiment'].value_counts()

df.dropna(inplace = True)

df.head()

for i in range(10):
    print(df['text'][i+1])

"""# Preprocessing Text"""

import re
def clean(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Conver to lower
    text = text.lower()
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['text'] = df['text'].apply(clean)

for i in range(10):
    print(df['text'][i+1])

df.shape

"""# Visualize Data"""

cyberpunk_palette = ["#FF00FF", "#00FF00", "#0000FF"]  # Neon pink, green, and blue
template = "plotly_dark"

import plotly.express as px
import plotly.graph_objs as go
from wordcloud import WordCloud



import plotly.graph_objs as go
import plotly.colors as colors
import numpy as np

# Word Length Distribution
word_lengths = [len(word) for text in df['text'] for word in text.split()]
word_lengths_counts = {length: word_lengths.count(length) for length in set(word_lengths)}

# Sort the word lengths by count in descending order
sorted_word_lengths = sorted(word_lengths_counts.items(), key=lambda x: x[1], reverse=True)

# Create a custom colorscale with a fixed number of colors
colorscale = colors.sample_colorscale('Viridis', len(word_lengths_counts))

# Create the bar chart trace
bar_trace = go.Bar(
    x=[length for length, count in sorted_word_lengths],
    y=[count for length, count in sorted_word_lengths],
    marker=dict(
        color=[colorscale[i] for i in range(len(sorted_word_lengths))],
        line=dict(
            color=cyberpunk_palette[0],
            width=2
        )
    ),
    hovertemplate='Word Length: %{x}<br>Count: %{y}<extra></extra>'
)

# Create the neon light effect trace
light_effect_trace = go.Scatter(
    x=[length for length, count in sorted_word_lengths],
    y=[count * 1.05 for length, count in sorted_word_lengths],
    mode='lines',
    line=dict(
        color=cyberpunk_palette[1],
        width=5
    ),
    hoverinfo='skip'
)

# Create the layout
layout = go.Layout(
    title="Word Length Distribution",
    xaxis=dict(
        title="Word Length",
        tickfont=dict(color=cyberpunk_palette[2])
    ),
    yaxis=dict(
        title="Count",
        tickfont=dict(color=cyberpunk_palette[2])
    ),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color=cyberpunk_palette[2],
    title_font_color=cyberpunk_palette[2],
    title_font_size=20,
    margin=dict(t=80, l=100, r=50, b=100)
)

# Create the figure and show it
fig = go.Figure(data=[bar_trace, light_effect_trace], layout=layout)
fig.show()

# Sentence Length Distribution
sentence_lengths = [len(text.split()) for text in df['text']]

# Create a custom colorscale with a fixed number of colors
colorscale = colors.sample_colorscale('Viridis', len(set(sentence_lengths)))

bar_trace = go.Bar(
    x=sorted(set(sentence_lengths)),
    y=[sentence_lengths.count(length) for length in sorted(set(sentence_lengths))],
    marker=dict(
        color=[colorscale[i] for i in range(len(set(sentence_lengths)))],
        line=dict(
            color=cyberpunk_palette[0],
            width=2
        )
    ),
    hovertemplate='Sentence Length: %{x}<br>Count: %{y}<extra></extra>'
)

light_effect_trace = go.Scatter(
    x=sorted(set(sentence_lengths)),
    y=[sentence_lengths.count(length) * 1.05 for length in sorted(set(sentence_lengths))],
    mode='lines',
    line=dict(
        color=cyberpunk_palette[1],
        width=5
    ),
    hoverinfo='skip'
)

layout = go.Layout(
    title="Sentence Length Distribution",
    xaxis=dict(
        title="Sentence Length",
        tickfont=dict(color=cyberpunk_palette[2])
    ),
    yaxis=dict(
        title="Count",
        tickfont=dict(color=cyberpunk_palette[2])
    ),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color=cyberpunk_palette[2],
    title_font_color=cyberpunk_palette[2],
    title_font_size=20,
    margin=dict(t=80, l=100, r=50, b=100)
)

fig = go.Figure(data=[bar_trace, light_effect_trace], layout=layout)
fig.show()

# Word Cloud for Positive Sentiment
positive_text = ' '.join(df[df['sentiment'] == 'positive']['text'])
wordcloud = WordCloud(background_color='black', width = 800, height = 400, max_words=200, colormap='Greens').generate(positive_text)
fig = go.Figure(go.Image(z = np.dstack((wordcloud.to_array(), wordcloud.to_array(), wordcloud.to_array()))))
fig.update_layout(
    title = 'Word Cloud For Positive Sentiment',
    template = template,
    plot_bgcolor = 'black',
    paper_bgcolor = 'black',
    font_color = cyberpunk_palette[2],
    title_font_color = cyberpunk_palette[2],
    title_font_size = 20,
    margin = dict(t = 80, l = 50, r = 50, b = 50)
)
fig.show()

# Word Cloud for Negative Sentiment
negative_text = ' '.join(df[df['sentiment'] == 'negative']['text'])
wordcloud = WordCloud(background_color='black', width=800, height=400, max_words=200, colormap='Reds').generate(negative_text)
fig = go.Figure(go.Image(z=np.dstack((wordcloud.to_array(), wordcloud.to_array(), wordcloud.to_array()))))
fig.update_layout(
    title="Word Cloud for Negative Sentiment",
    template=template,
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color=cyberpunk_palette[2],
    title_font_color=cyberpunk_palette[2],
    title_font_size=20,
    margin=dict(t=80, l=50, r=50, b=50)
)
fig.show()

# Word Cloud for Neutral Sentiment
neutral_text = ' '.join(df[df['sentiment'] == 'neutral']['text'])
wordcloud = WordCloud(background_color='black', width=800, height=400, max_words=200, colormap='Blues').generate(neutral_text)
fig = go.Figure(go.Image(z=np.dstack((wordcloud.to_array(), wordcloud.to_array(), wordcloud.to_array()))))
fig.update_layout(
    title="Word Cloud for Neutral Sentiment",
    template=template,
    plot_bgcolor="black",
    paper_bgcolor="black",
    font_color=cyberpunk_palette[2],
    title_font_color=cyberpunk_palette[2],
    title_font_size=20,
    margin=dict(t=80, l=50, r=50, b=50)
)
fig.show()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

"""# Tokenize Text"""

tokenizer = Tokenizer()
tokenizer.fit_on_texts(df['text'])
sequences = tokenizer.texts_to_sequences(df['text'])

"""# Padding the Sequences"""

max_length = max([len(seq) for seq in sequences])
padded_sequences = pad_sequences(sequences, maxlen = max_length, padding = 'post')

"""# Prepare The Target Variable"""

labels = pd.get_dummies(df['sentiment']).values

xtrian,xtest,ytrain,ytest = train_test_split(padded_sequences, labels, test_size = 0.1)

"""# Model Archiecture"""

#to install keras-tuner
!pip install keras-tuner

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout, BatchNormalization,RNN
from kerastuner.tuners import RandomSearch
from sklearn.model_selection import train_test_split

vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 128
max_length = 32


from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN, BatchNormalization, Dense, Dropout
from keras.optimizers import Adam

vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 128
max_length = 32

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(LSTM(32, return_sequences=True))
model.add(BatchNormalization())

model.add(LSTM(64))
model.add(BatchNormalization())

model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

model.fit(xtrian, ytrain, epochs=5, validation_data=(xtest, ytest))

model.save('lstm.h5')

loss, accuracy = model.evaluate(xtest, ytest)
print("Test Accuracy:", accuracy)

max_length

def predict_sentiment(input_text, tokenizer, model, max_length):
    # Preprocess the input text
    input_sequence = tokenizer.texts_to_sequences([input_text])
    padded_input_sequence = pad_sequences(input_sequence, maxlen=max_length, padding='post')

    # Get the prediction
    prediction = model.predict(padded_input_sequence)

    # Convert the prediction to sentiment label
    sentiment_labels = ['Negative', 'Neutral', 'Positive']
    predicted_label_index = np.argmax(prediction)
    predicted_sentiment = sentiment_labels[predicted_label_index]

    return predicted_sentiment

positive_rows = df[df['sentiment'] == 'negative']
print(positive_rows[['text']].head(5))

input_text = "oh no i have only 1 day left.  how will i   finish my work in just 1 day"
predicted_sentiment = predict_sentiment(input_text, tokenizer, model, max_length)
print("Predicted Sentiment:", predicted_sentiment)

import pickle
with open('tokenizer.pkl', 'wb') as file:
    pickle.dump(tokenizer, file)

