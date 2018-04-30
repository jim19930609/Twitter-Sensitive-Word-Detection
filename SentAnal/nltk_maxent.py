import random
import pickle
import nltk
import prepro
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('all')


def collect_data(input_dir, forTest=False):
    data = []
    print('start to collect data for %s: ' % input_dir)
    with open(input_dir, 'r') as csv:
        lines = csv.readlines()
        for i, line in enumerate(lines):
            # print('current line: ', line)
            if not forTest:
                tag = line.split(',')[1]
            else:
                tag = '5'
            rest = line[line.find(','):]
            rest = rest[line.find(',')-1:-2]
            word_list = rest.split(',')
            data.append((word_list, tag))
            # print('length of word list: ', len(word_list))
            # print('tag: ' + tag + ', wordlist: ' + ' '.join(map(str, word_list)))

            # if i == 1000:
            #     break
    return data


def save_results_to_csv(results, csv_file):
    ''' Save list of type [(tweet_id, positive)] to csv in Kaggle format '''
    with open(csv_file, 'w') as csv:
        csv.write('id,prediction\n')
        for tweet_id, pred in results:
            csv.write(tweet_id)
            csv.write(',')
            csv.write(str(pred))
            csv.write('\n')
    return


def split_data(tweets, ratio=0.9):
    index = int(ratio * len(tweets))
    random.shuffle(tweets)
    return tweets[:index], tweets[index:]


def list_to_dict(words_list):
    return dict([(word, True) for word in words_list])


def format_train_data(dir):
    train_data = collect_data(dir, forTest=False)
    print('shape of train_data: ', len(train_data))
    train_set, vali_set = split_data(train_data)
    print('shape of train_set and vali_set: ', len(train_set), len(vali_set))

    train_list = [(list_to_dict(item[0]), item[1]) for item in train_set]
    vali_list = [(list_to_dict(item[0]), item[1]) for item in vali_set]

    return train_set, vali_set, train_list, vali_list


def format_test_data(dir):
    test_set = collect_data(dir, forTest=True)
    test_list = [(list_to_dict(item[0]), item[1]) for item in test_set]
    return test_set, test_list


def generate_model(train_list, num_iter):
    algo = nltk.classify.MaxentClassifier.ALGORITHMS[1]
    classifier = nltk.MaxentClassifier.train(train_list, algo, max_iter=num_iter)
    classifier.show_most_informative_features(10)
    return classifier


def get_accuracy(model, data_set, data_list):
    err_count = 0
    for item in data_list:
        label = item[1]
        tweet = item[0]
        pred_label = model.classify(tweet)
        # print(pred_sent, sent)
        if pred_label != label:
            err_count += 1
    return (len(data_set) - err_count) / len(data_set)


def save_model(model, pickle_dir):
    f = open(pickle_dir, 'wb')
    pickle.dump(model, f)
    f.close()
    return

def load_model(pickle_dir):
    return pickle.load(open(pickle_dir, 'rb'))


def predict(model, test_dir, pred_dir):
    # print('Formatting testing data set:')
    test_set, test_list = format_test_data(test_dir)
    # print('\nPredicting for test data:')
    id = 0
    prediction = []
    for item in test_list:
        tweet = item[0]
        pred_label = model.classify(tweet)
        prediction.append((str(id), pred_label))
        id += 1
    save_results_to_csv(prediction, pred_dir)
    print('Saved prediction results to %s' % pred_dir)
    return prediction


def train(train_dir, pickle_dir, num_iter):
    # print('Formatting training & validation data set:')
    train_set, vali_set, train_list, vali_list = format_train_data(train_dir)
    model = generate_model(train_list, num_iter)
    accuracy = get_accuracy(model, vali_set, vali_list)
    # print('Validation set accuracy:%.4f'% accuracy)
    save_model(model, pickle_dir)
    print('Saved model to %s' % pickle_dir)
    return model


def get_label(model_dir, raw_tweet):
    processed_tweet = prepro.cleansing(raw_tweet)
    print('Processed tweet:', processed_tweet)
    single_csv = 'single_tweet.csv'
    with open(single_csv, 'w') as csv:
        csv.write('1')
        csv.write(',')
        csv.write(str(processed_tweet))
        csv.write('\n')
    single_set, single_list = format_test_data(single_csv)

    model = load_model(model_dir)
    label = []
    for item in single_list:
        pred_label = model.classify(item[0])
        label.append(pred_label)
    return label[0]


if __name__ == '__main__':
    train_file_dir = './dataset/train_pre.csv'
    test_file_dir = './dataset/test_pre.csv'
    model_dir = './maxent_classifier.pickle'
    result_dir = './dataset/pred_result.csv'

    classifier = train(train_file_dir, model_dir, num_iter=10)
    result = predict(classifier, test_file_dir, result_dir)

    eg_tweet = 'You a lame if you fuck over a great person who’s always been down for you since day one'
    print('Current tweet: ', eg_tweet)
    sent_label = get_label(model_dir, eg_tweet)
    print('Sentiment Analysis result: ', sent_label)



