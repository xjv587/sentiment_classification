# models.py

from sentiment_data import *
from utils import *

from collections import Counter, defaultdict
import numpy as np


class FeatureExtractor(object):
    """
    Feature extraction base type. Takes a sentence and returns an indexed list of features.
    """
    def get_indexer(self):
        raise Exception("Don't call me, call my subclasses")

    def extract_features(self, sentence: List[str], add_to_indexer: bool=False) -> Counter:
        """
        Extract features from a sentence represented as a list of words. Includes a flag add_to_indexer to
        :param sentence: words in the example to featurize
        :param add_to_indexer: True if we should grow the dimensionality of the featurizer if new features are encountered.
        At test time, any unseen features should be discarded, but at train time, we probably want to keep growing it.
        :return: A feature vector. We suggest using a Counter[int], which can encode a sparse feature vector (only
        a few indices have nonzero value) in essentially the same way as a map. However, you can use whatever data
        structure you prefer, since this does not interact with the framework code.
        """
        raise Exception("Don't call me, call my subclasses")


class UnigramFeatureExtractor(FeatureExtractor):
    """
    Extracts unigram bag-of-words features from a sentence. It's up to you to decide how you want to handle counts
    and any additional preprocessing you want to do.
    """
    def __init__(self, indexer: Indexer):
        #raise Exception("Must be implemented")
        self.indexer = indexer

    def get_indexer(self):
        return self.indexer
    
    def extract_features(self, sentence: List[str], add_to_indexer: bool=False) -> Counter:
        features = Counter()
        for word in sentence:
            if add_to_indexer:
                index = self.indexer.add_and_get_index(word)
            else:
                index = self.indexer.index_of(word)
            if index != -1:
                features[index] += 1
        return features


class BigramFeatureExtractor(FeatureExtractor):
    """
    Bigram feature extractor analogous to the unigram one.
    """
    def __init__(self, indexer: Indexer):
        #raise Exception("Must be implemented")
        self.indexer = indexer

    def get_indexer(self):
        return self.indexer

    def extract_features(self, sentence: List[str], add_to_indexer: bool=False) -> Counter:
        features = Counter()
        for i in range(len(sentence) - 1):
            bigram = f"{sentence[i]}_{sentence[i+1]}"
            if add_to_indexer:
                index = self.indexer.add_and_get_index(bigram)
            else:
                index = self.indexer.index_of(bigram)
            if index != -1:
                features[index] += 1
        return features


class BetterFeatureExtractor(FeatureExtractor):
    """
    Better feature extractor...try whatever you can think of!
    """
    def __init__(self, indexer: Indexer):
        #raise Exception("Must be implemented")
        self.indexer = indexer

    def get_indexer(self):
        return self.indexer

    def extract_features(self, sentence: List[str], add_to_indexer: bool=False) -> Counter:
        features = Counter()
        for word in sentence:
            if len(word) > 2:  # ignore very short words (could be stopwords)
                if add_to_indexer:
                    index = self.indexer.add_and_get_index(word)
                else:
                    index = self.indexer.index_of(word)
                if index != -1:
                    features[index] += 1
        
        # Add bigram features
        for i in range(len(sentence) - 1):
            bigram = f"{sentence[i]}_{sentence[i+1]}"
            if add_to_indexer:
                index = self.indexer.add_and_get_index(bigram)
            else:
                index = self.indexer.index_of(bigram)
            if index != -1:
                features[index] += 1
        
        return features



class SentimentClassifier(object):
    """
    Sentiment classifier base type
    """
    def predict(self, sentence: List[str]) -> int:
        """
        :param sentence: words (List[str]) in the sentence to classify
        :return: Either 0 for negative class or 1 for positive class
        """
        raise Exception("Don't call me, call my subclasses")


class TrivialSentimentClassifier(SentimentClassifier):
    """
    Sentiment classifier that always predicts the positive class.
    """
    def predict(self, sentence: List[str]) -> int:
        return 1


class PerceptronClassifier(SentimentClassifier):
    """
    Implement this class -- you should at least have init() and implement the predict method from the SentimentClassifier
    superclass. Hint: you'll probably need this class to wrap both the weight vector and featurizer -- feel free to
    modify the constructor to pass these in.
    """
    #def __init__(self):
        #raise Exception("Must be implemented")
    def __init__(self, weights: np.ndarray, feat_extractor: FeatureExtractor):
        self.weights = weights
        self.feat_extractor = feat_extractor

    def predict(self, sentence: List[str]) -> int:
        features = self.feat_extractor.extract_features(sentence, add_to_indexer=False)
        score = sum(self.weights[idx] * value for idx, value in features.items())
        return 1 if score > 0 else 0


class LogisticRegressionClassifier(SentimentClassifier):
    """
    Implement this class -- you should at least have init() and implement the predict method from the SentimentClassifier
    superclass. Hint: you'll probably need this class to wrap both the weight vector and featurizer -- feel free to
    modify the constructor to pass these in.
    """
    #def __init__(self):
    #    raise Exception("Must be implemented")
    def __init__(self, weights: np.ndarray, feat_extractor: FeatureExtractor):
        self.weights = weights
        self.feat_extractor = feat_extractor

    def predict(self, sentence: List[str]) -> int:
        features = self.feat_extractor.extract_features(sentence, add_to_indexer=False)
        score = sum(self.weights[idx] * value for idx, value in features.items())
        probability = 1 / (1 + np.exp(score))
        return 1 if probability >= 0.5 else 0


def train_perceptron(train_exs: List[SentimentExample], feat_extractor: FeatureExtractor) -> PerceptronClassifier:
    """
    Train a classifier with the perceptron.
    :param train_exs: training set, List of SentimentExample objects
    :param feat_extractor: feature extractor to use
    :return: trained PerceptronClassifier model
    """
    #raise Exception("Must be implemented")
    for ex in train_exs:
        feat_extractor.extract_features(ex.words, add_to_indexer=True)
    vocab_size = len(feat_extractor.get_indexer())
    weights = np.zeros(vocab_size)
    learning_rate = 0.0001
    num_epochs = 30

    for epoch in range(num_epochs):
        np.random.shuffle(train_exs)
        for ex in train_exs:
            features = feat_extractor.extract_features(ex.words, add_to_indexer=False)
            prediction = sum(weights[idx] * value for idx, value in features.items())
            if (prediction > 0) != (ex.label == 1):
                for idx, value in features.items():
                    weights[idx] += learning_rate * value if ex.label == 1 else -learning_rate * value

    return PerceptronClassifier(weights, feat_extractor)


def train_logistic_regression(train_exs: List[SentimentExample], feat_extractor: FeatureExtractor) -> LogisticRegressionClassifier:
    """
    Train a logistic regression model.
    :param train_exs: training set, List of SentimentExample objects
    :param feat_extractor: feature extractor to use
    :return: trained LogisticRegressionClassifier model
    """
    #raise Exception("Must be implemented")
    for ex in train_exs:
        feat_extractor.extract_features(ex.words, add_to_indexer=True)
    vocab_size = len(feat_extractor.get_indexer())
    weights = np.zeros(vocab_size)
    learning_rate = 0.4
    num_epochs = 30

    for epoch in range(num_epochs):
        np.random.shuffle(train_exs)
        for ex in train_exs:
            features = feat_extractor.extract_features(ex.words, add_to_indexer=False)
            score = sum(weights[idx] * value for idx, value in features.items())
            probability = 1 / (1 + np.exp(score))
            error = ex.label - probability
            for idx, value in features.items():
                weights[idx] -= learning_rate * error * value

    return LogisticRegressionClassifier(weights, feat_extractor)


def train_better(train_exs: List[SentimentExample], feat_extractor: FeatureExtractor) -> BetterFeatureExtractor:
    for ex in train_exs:
        feat_extractor.extract_features(ex.words, add_to_indexer=True)
    
    model_type = "PERCEPTRON"
    if model_type == "PERCEPTRON":
        model = train_perceptron(train_exs, feat_extractor)
    elif model_type == "LR":
        model = train_logistic_regression(train_exs, feat_extractor)
    else:
        raise ValueError("Unsupported model type. Choose 'PERCEPTRON' or 'LR'.")

    return model


def train_model(args, train_exs: List[SentimentExample], dev_exs: List[SentimentExample]) -> SentimentClassifier:
    """
    Main entry point for your modifications. Trains and returns one of several models depending on the args
    passed in from the main method. You may modify this function, but probably will not need to.
    :param args: args bundle from sentiment_classifier.py
    :param train_exs: training set, List of SentimentExample objects
    :param dev_exs: dev set, List of SentimentExample objects. You can use this for validation throughout the training
    process, but you should *not* directly train on this data.
    :return: trained SentimentClassifier model, of whichever type is specified
    """
    # Initialize feature extractor
    if args.model == "TRIVIAL":
        feat_extractor = None
    elif args.feats == "UNIGRAM":
        # Add additional preprocessing code here
        feat_extractor = UnigramFeatureExtractor(Indexer())
    elif args.feats == "BIGRAM":
        # Add additional preprocessing code here
        feat_extractor = BigramFeatureExtractor(Indexer())
    elif args.feats == "BETTER":
        # Add additional preprocessing code here
        feat_extractor = BetterFeatureExtractor(Indexer())
    else:
        raise Exception("Pass in UNIGRAM, BIGRAM, or BETTER to run the appropriate system")

    # Train the model
    if args.model == "TRIVIAL":
        model = TrivialSentimentClassifier()
    elif args.model == "PERCEPTRON":
        model = train_perceptron(train_exs, feat_extractor)
    elif args.model == "LR":
        model = train_logistic_regression(train_exs, feat_extractor)
    elif args.model == "BETTER":
        model = train_better(train_exs, feat_extractor)
    else:
        raise Exception("Pass in TRIVIAL, PERCEPTRON, or LR to run the appropriate system")
    return model