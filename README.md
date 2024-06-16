# Sentiment_Analysis_Project-3
This code performs sentiment analysis, which is a technique used to determine whether a piece of text (like a tweet or a review) expresses a positive, negative, or neutral sentiment.

### Key Takeways
*Positive Sentiment*
![positive_sentiment](https://github.com/ANSHPG/Sentiment_Analysis_Project-3/assets/132222062/c1201d52-8449-4f84-8002-f8e49a1fcc93)
*Neutral Sentiment*
![neutral_sentiment](https://github.com/ANSHPG/Sentiment_Analysis_Project-3/assets/132222062/619a9760-82c6-4029-88bf-1a67618f067e)
*Negative Sentiment*
![negative_sentiment](https://github.com/ANSHPG/Sentiment_Analysis_Project-3/assets/132222062/b97fd9ec-552d-4e3d-a159-6db17e170620)
*Length Distribution*
![length_distribution](https://github.com/ANSHPG/Sentiment_Analysis_Project-3/assets/132222062/1902ac6d-5b98-40e7-aa6d-9765822c3627)

### Step-by-Step Explanation:

1. **Data Acquisition and Preparation**:
   - The code begins by downloading a dataset from an online source. This dataset contains text samples labeled with sentiments (positive, negative, neutral). After downloading, it is extracted and prepared for analysis.

2. **Data Exploration and Cleaning**:
   - Once the dataset is loaded into a Pandas DataFrame (`df`), the code checks its shape, looks for any missing values (`NaN`), and removes any rows with missing data to ensure quality.

3. **Text Preprocessing**:
   - The text in each row undergoes cleaning:
     - Non-alphabetic characters (like punctuation) are removed.
     - Text is converted to lowercase to ensure consistency.
     - Extra whitespaces are removed.

4. **Visualizing Data**:
   - Various visualizations are created to understand the dataset better:
     - **Word Length Distribution**: Shows how often words of different lengths appear in the text.
     - **Sentence Length Distribution**: Illustrates the distribution of sentence lengths in the dataset.
     - **Word Clouds**: Visual representations of the most frequent words in each sentiment category (positive, negative, neutral).

5. **Model Building**:
   - A deep learning model (LSTM-based neural network) is constructed using TensorFlow/Keras. This model is trained to predict the sentiment (positive, negative, neutral) of a given text based on its content. The text data is tokenized (converted into numerical sequences) and padded (ensuring all sequences are of the same length) before training.

6. **Model Training and Evaluation**:
   - The model is trained on a portion of the dataset (`xtrain`, `ytrain`) and evaluated on another portion (`xtest`, `ytest`). Training involves adjusting the model’s weights based on how well it predicts sentiment labels.

7. **Saving the Model**:
   - Once trained, the model is saved to a file (`lstm.h5`) for later use.

8. **Prediction**:
   - A function (`predict_sentiment`) is defined to predict sentiment labels for new input text using the trained model. This function preprocesses the input text, feeds it into the model, and returns the predicted sentiment label (positive, negative, or neutral).

### Summary:
This code essentially automates the process of analyzing sentiment from textual data. It downloads a dataset, cleans and prepares it, visualizes key aspects, builds and trains a deep learning model for sentiment prediction, and finally provides a function to predict sentiments of new text inputs. This approach helps in understanding and categorizing the sentiment expressed in text data automatically.
