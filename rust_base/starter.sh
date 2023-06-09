#!/bin/bash
# Name of the new Cargo project
PROJECT_NAME="top_k_word_count"
# Rust source file name
RUST_FILE="wordcount.rs"
# Stopwords file name
STOPWORDS_FILE="stopwords.txt"
DATA_PATH="../../dataset/"
DATA_300MB="data_300MB.txt"
DATA_2500MB="data_2.5GB.txt"
DATA_16GB="data_3GB.txt"

rm -rf $PROJECT_NAME

# Create a new binary cargo project
cargo new --bin $PROJECT_NAME

# Copy the Rust source file into the new project
cp $RUST_FILE $PROJECT_NAME/src/main.rs

# Copy the stopwords file into the new project
cp $STOPWORDS_FILE $PROJECT_NAME/

# Navigate into the new project directory
cd $PROJECT_NAME

# Add the rayon dependency to the Cargo.toml file
echo 'rayon = "1.5.1"' >> Cargo.toml
echo 'num_cpus = "1.13.0"' >> Cargo.toml
echo 'sys-info = "0.9.1"' >> Cargo.toml

rustup target add aarch64-apple-darwin

# Build the project
cargo build --release --target aarch64-apple-darwin
# Run the built executable with provided arguments
# $1 is the file to analyze, $2 is the number of top frequent words to display
# echo "running" $DATA_PATH$1
# ./target/release/$PROJECT_NAME $DATA_PATH$DATA_300MB 10
# echo "running" $DATA_PATH$2
# ./target/release/$PROJECT_NAME $DATA_PATH$DATA_2500MB 10
# echo "running" $DATA_PATH$3
# ./target/release/$PROJECT_NAME $DATA_PATH$DATA_16GB 10

