#!bin/sh

# Set variables
DATA_DIR="data"
TRAIN_SET_URL="https://inclass.kaggle.com/c/detroit-blight-ticket-compliance/download/test.csv"
TEST_SET_URL="https://inclass.kaggle.com/c/detroit-blight-ticket-compliance/download/train.csv"

# Check for data directory. If it doesn't exist, make it.
if [ ! -d $DATA_DIR ]; then
    echo "Creating data directory at $(pwd)/$DATA_DIR ..."
    mkdir -p $DATA_DIR
fi


echo "Downloading the train and test sets ..."
curl "$TRAIN_SET_URL" -o "$DATA_DIR/train.csv" &> /dev/null
if [ $? -eq 0 ]; then
    echo "\ttrain.csv downloaded successfully!"
else
    echo "\tFailed to download train.csv from $TRAIN_SET_URL"
    echo "\tCheck TRAIN_SET_URL"
fi

curl "$TEST_SET_URL" -o "$DATA_DIR/test.csv" &> /dev/null
if [ $? -eq 0 ]; then
    echo "\ttest.csv downloaded successfully!"
else
    echo "\tFailed to download test.csv from $TEST_SET_URL"
    echo "\tCheck TEST_SET_URL"
fi
echo "Finished!"
