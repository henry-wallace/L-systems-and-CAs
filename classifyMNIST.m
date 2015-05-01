
% Images and labels

train_images = loadMNISTImages('train-images-idx3-ubyte');
train_labels = loadMNISTLabels('train-labels-idx1-ubyte');
test_images = loadMNISTImages('t10k-images-idx3-ubyte');
test_labels = loadMNISTLabels('t10k-labels-idx1-ubyte');

%format labels
train_labels = train_labels';
train_labels = [train_labels; zeros(9, length(train_labels))];
for i=1:length(train_labels)
    x=zeros(10,1);
    x(train_labels(1,i)+1)=1;
    train_labels(:,i)=x;
end

test_labels = test_labels';
% test_labels = [test_labels; zeros(9, length(test_labels))];
% for i=1:length(test_labels)
%     x=zeros(10,1);
%     x(test_labels(1,i)+1)=1;
%     test_labels(:,i)=x;
% end

% Setting up the neural net

layer_number = 200;
net = fitnet(layer_number);

%change the type of training
net.trainFcn = 'trainscg';

%set epochs
epoch=400;
net.trainParam.epochs=epoch;

%train the net!
net=train(net, train_images, train_labels);

%check how well it does
net_test_results = net(test_images);
test_results=zeros(1,length(net_test_results));
% performance = perform(net, test_labels, test_results)
for i=1:length(test_results)
    test_results(i)=find(test_results(:,i)==max(test_results(:,i)))-1;
end
num_wrong=sum(test_results ~= test_labels);
percent_wrong=num_wrong/length(test_labels);
percent_wrong
