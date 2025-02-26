### sentiment_classification
# Overview:
This project focuses on sentiment classification of movie reviews, where the goal is to distinguish between positive and negative sentiments in text. Using a machine learning pipeline, I implemented multiple classifiers and feature extraction techniques to improve accuracy on a binary sentiment classification task.

# Key Components:
1. Feature Engineering
  - Unigram Feature Extraction: Converted sentences into sparse vectors using single-word representations.
  - Bigram Feature Extraction: Incorporated word pairs to capture contextual sentiment.
  - Better Feature Extraction: Explored additional techniques such as TF-IDF weighting, stopword removal, and frequency clipping to improve performance.
2. Machine Learning Models
  - Perceptron Classifier: Implemented a simple, linear classification model trained using an online learning approach.
  - Logistic Regression Classifier: Implemented a probabilistic classification model optimized using gradient descent.
  - Performance Optimization: Experimented with learning rate schedules, feature selection, and weight regularization to enhance model accuracy.
3. Model Evaluation
  - Perceptron: Achieved 78% accuracy
  - Logistic Regression: Achieved 82% accuracy
  - Runtime Efficiency: within 20 seconds (or 60 seconds for advanced feature extraction).

