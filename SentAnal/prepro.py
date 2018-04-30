import sys
import re
import numpy as np


def process_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet


def is_valid(word):
    return re.search(r'^[a-zA-Z][a-z0-9A-Z\._]*$', word) is not None


def cleansing(tweet):
    # Convert to lower case
    tweet = tweet.lower()
    # Replace URLs with the word URL
    tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ', tweet)
    # Replace @handle with the word USER_MENTION
    tweet = re.sub(r'@[\S]+', 'USER_MENTION', tweet)
    # Replace #hashtag with hashtag
    tweet = re.sub(r'#(\S+)', r' \1 ', tweet)
    # Remove RT (retweet)
    tweet = re.sub(r'\brt\b', '', tweet)
    # Replace 2+ dots with space
    tweet = re.sub(r'\.{2,}', ' ', tweet)
    # Strip space, " and ' from tweet
    tweet = tweet.strip(' "\'')
    # Replace emojis with either EMO_POS or EMO_NEG
    tweet = process_emojis(tweet)
    # Replace multiple spaces with a single space
    tweet = re.sub(r'\s+', ' ', tweet)

    words = tweet.split(' ')
    processed_tweet = []
    for word in words:
        word = word.strip('\'"?!,.():;')
        # Convert more than 2 letter repetitions to 2 letter
        # funnnnny --> funny
        word = re.sub(r'(.)\1+', r'\1\1', word)
        # Remove - & '
        word = re.sub(r'(-|\')', '', word)

        if is_valid(word):
            processed_tweet.append(word)

    return processed_tweet


def preprocess(input_dir, train_output_dir, test_output_dir):
    # print('input file: ', input_dir)
    # print('output file: ', train_output_dir)
    train_output_file = open(train_output_dir, 'w')
    test_output_file = open(test_output_dir, 'w')

    with open(input_dir, 'r') as csv:
        print('Reading '+input_dir+': ')
        csv.readline()
        lines = csv.readlines()
        length = len(lines)
        print('len:', length)
        errs = []
        for i in range(length):
            curr_line = lines[i]
            if curr_line:
                print('line: ', curr_line)
                # print('aaa', curr_line.find(' '), curr_line[:curr_line.find(' ')])
                try:
                    id = curr_line[:curr_line.find('	')]
                    rest_line = curr_line[1 + curr_line.find('	'):]
                    sent_str = rest_line[:rest_line.find('	')]
                    sent = int(sent_str)
                    rest_line = rest_line[1 + rest_line.find('	'):]
                    tweet = rest_line

                    processed_tweet = cleansing(tweet)
                    print('id: %s, sent: %d, processed tweet: %s' % (id, sent, processed_tweet))
                    rand = np.random.randint(1, 10)
                    if not rand == 1:
                        train_output_file.write('%s,%d,%s\n' %
                                           (id, sent, processed_tweet))
                    else:
                        test_output_file.write('%s,%s\n' %
                                          (id, processed_tweet))
                except:
                    errs.append(curr_line.split(',')[0])
    train_output_file.close()
    test_output_file.close()
    # print('Processed tweets saved to: %s, %s' % train_output_dir, test_output_dir)
    return errs


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('File location required!')
    #     exit()
    # input_dir = sys.argv[1]
    # output_dir = input_dir[:-4] + '_pre.csv'
    input_dir = './dataset/data.csv'
    train_output_dir = './dataset/train_pre.csv'
    test_output_dir = './dataset/test_pre.csv'
    train_errs = preprocess(input_dir, train_output_dir, test_output_dir)
    print('train error list: ', train_errs)





