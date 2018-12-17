from nn.neuralnetwork import NeuralNetwork
from nn.math_ import output2binary, normalize
from data.code.readImage import load_data
import matplotlib.pyplot as plt
import sys
import argparse


DEFAULT_DUMP_FILE = 'trained_model.pkl'  # default model file name
SHOW_PLOT = False  # show graph of chane in accuracy and loss over epochs


def parameter_parse(argv):
    """
    parses given commandline arguments and flags
    :param argv: command line argument
    :return: path to data
    """
    parser = argparse.ArgumentParser('Train a neural network')
    parser.add_argument('--data_path', '-d', required=True,
                        dest='data_path', type=str, nargs=1, help='Path to the training data')
    parser.add_argument('--model_name', '-m', type=str, nargs=1, default=DEFAULT_DUMP_FILE,
                        dest='model_name', help='name for model, if not given default name will be used')
    parser.add_argument('--template_path', '-t', required=False, type=str, nargs=1, default='model.json',
                        dest='template_path', help='template from file, if not given default path will be used')

    # TODO: add model training from json file

    return vars(parser.parse_args(argv))


if __name__ == '__main__':

    # parse command line arguments
    args = parameter_parse(sys.argv[1:])
    template_path = args['template_path'] if isinstance(args['template_path'], str) else args['template_path'][0]

    # prepare data
    train = load_data(args['data_path'][0])
    train_x = [normalize(x, 255) for x in train['x']]
    train_y = output2binary(train['y'][0])

    # build model from template
    NN = NeuralNetwork.create(template_path)

    # log the data for graph
    losses = []
    accuracies = []

    for epoch in range(NN.epochs):

        NN.fit(train_x, train_y)

        # get results
        print("Current epoch: %d" % epoch)
        print("Learning rate: %f" % NN.l_rate)
        print("Loss: %f" % (NN.out_layer.cost / len(train_x)))
        print("Accuracy: %f" % ((NN.hit_count / len(train_x)) * 100))
        print("Last Prediction: {}".format(NN.out_layer.predicted))
        print("Expected: {}".format(train_y[-1]))
        print("Hit count: %d" % NN.hit_count)
        print("-"*20+"\n")

        # accumulate the graph data
        losses.append(NN.out_layer.cost / len(train_x))
        accuracies.append((NN.hit_count / len(train_x)))

        NN.clean()

        # save model to file
        NN.dump(args['model_name'][0])

    if SHOW_PLOT:
        # graph accuracy and loss
        plt.plot([i for i in range(NN.epochs)], losses, label='Loss')
        plt.plot([i for i in range(NN.epochs)], accuracies, label='Accuracy')
        plt.legend()
        plt.show()