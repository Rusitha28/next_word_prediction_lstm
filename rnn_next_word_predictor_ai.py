# import necessary libraries
import numpy as np
import tensorflow as tf

# load dataset
with open("/content/ai.txt", 'r', encoding='utf-8') as file:
    artificial_intelligence = file.read()

artificial_intelligence

artificial_intelligence[:100]

tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts([artificial_intelligence])

#tokenizer.get_config()['filters']

tokenizer = tf.keras.preprocessing.text.Tokenizer()

tokenizer.fit_on_texts([artificial_intelligence])

tokenizer.get_config()['word_counts']

tokenizer.word_index

input_sequences = []
for sentence in artificial_intelligence.split('\n'):
    token_list = tokenizer.texts_to_sequences([sentence])[0]
    for i in range(1, len(token_list)):
        sequence = token_list[:i+1]
        input_sequences.append(sequence)

input_sequences[:10]

max_length = max([len(input_sequence) for input_sequence in input_sequences])
max_length

# add padding
input_sequences = np.array(tf.keras.preprocessing.sequence.pad_sequences(input_sequences, maxlen=max_length, padding='pre'))

input_sequences[1]

# divide dataset into feature set (X) and labels (y)
X = input_sequences[:, :-1]
y = input_sequences[:, -1]

X[0]

y

# number of words
num_classes = len(tokenizer.word_index)+1
num_classes

# one-hot encoding labels
y = np.array(tf.keras.utils.to_categorical(y, num_classes=num_classes))

y[1]

# model building
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(num_classes, 80, input_length=max_length-1))
model.add(tf.keras.layers.LSTM(100))
model.add(tf.keras.layers.Dense(num_classes, activation='softmax'))

model.summary()

# compile the model
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# model training
history = model.fit(X, y, epochs=100)

input_text = " Most people are not very familiar "
for i in range(22):
    token_list = tokenizer.texts_to_sequences([input_text])[0]
    token_list = tf.keras.preprocessing.sequence.pad_sequences([token_list], maxlen=max_length-1, padding='pre')
    predicted = np.argmax(model.predict(token_list), axis=-1)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    input_text += " " + output_word

print(input_text)
