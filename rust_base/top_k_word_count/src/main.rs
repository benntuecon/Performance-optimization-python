use rayon::prelude::*;
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, prelude::*, SeekFrom};
use std::env;
use std::time::Instant;

use num_cpus;
use sys_info;



use std::collections::HashSet;

fn read_stop_words() -> io::Result<HashSet<String>> {
    let stopwords_path = std::env::current_dir()?.join("stopwords.txt");
    let mut file = File::open(stopwords_path)?;
    let mut buffer = Vec::new();

    file.read_to_end(&mut buffer)?;

    let mut stopwords = HashSet::new();
    let mut current_word = String::new();

    for &byte in &buffer {
        if byte.is_ascii_whitespace() {
            if !current_word.is_empty() {
                stopwords.insert(current_word);
                current_word = String::new();
            }
        } else if byte.is_ascii_alphanumeric() || byte.is_ascii_punctuation() {
            current_word.push((byte as char).to_lowercase().next().unwrap());
        }
    }

    if !current_word.is_empty() {
        stopwords.insert(current_word);
    }

    Ok(stopwords)
}



fn count_words(path: &str, start: u64, end: u64, stopwords: &HashSet<String>) -> io::Result<HashMap<String, u32>> {
    let mut file = File::open(path)?;
    file.seek(SeekFrom::Start(start))?;
    let reader = file.take(end - start);
    let mut buf_reader = io::BufReader::new(reader);
    let mut contents = Vec::new();

    buf_reader.read_to_end(&mut contents)?;

    let mut freqs = HashMap::new();
    let mut current_word = String::new();

    for &byte in &contents {
        if byte.is_ascii_whitespace() {
            if !current_word.is_empty() && !stopwords.contains(&current_word) {
                *freqs.entry(current_word.clone()).or_insert(0) += 1;
            }
            current_word.clear();
        } else if byte.is_ascii_alphanumeric() || byte.is_ascii_punctuation() {
            current_word.push((byte as char).to_lowercase().next().unwrap());
        }
    }

    if !current_word.is_empty() && !stopwords.contains(&current_word) {
        *freqs.entry(current_word.clone()).or_insert(0) += 1;
    }

    Ok(freqs)
}



fn print_top_k(freqs: Vec<HashMap<String, u32>>, k: usize) {
    let mut total_freqs: HashMap<String, u32> = HashMap::new();
    for freq in freqs {
        for (word, count) in freq {
            *total_freqs.entry(word).or_insert(0) += count;
        }
    }

    let mut words: Vec<_> = total_freqs.drain().collect();
    words.sort_unstable_by_key(|&(_, v)| std::cmp::Reverse(v));

    for (word, freq) in words.into_iter().take(k) {
        print!("{}: {}      ", word, freq);
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <file> <k>", args[0]);
        return;
    }

    let start_time = Instant::now();
    let path = &args[1];
    let k: usize = args[2].parse().unwrap_or(0);

    let metadata = File::open(path).unwrap().metadata().unwrap();
    let file_size = metadata.len();

    let cores = num_cpus::get() as u64;
    let ram_in_kb = sys_info::mem_info().unwrap().avail; // use available memory
    let ram_in_bytes = ram_in_kb * 1024;
    const PROPORTION_OF_RAM_FOR_CHUNKS: f64 = 0.8;  // Adjust this as needed

    // calculate the total chunk size, as a proportion of available RAM
    let total_chunk_size = (ram_in_bytes as f64 * PROPORTION_OF_RAM_FOR_CHUNKS) as u64;

    // Start with a multiplier of 1, and increment if needed
    let mut multiplier = 1;

    while file_size / (cores * multiplier) > total_chunk_size / cores {
        multiplier += 1;
    }

    let chunk_size = file_size / (cores * multiplier);


    println!("CPU cores: {}", cores);
    println!("Available RAM: {} KB", ram_in_kb);
    println!("File size: {} bytes", file_size);
    println!("Chinking multiplier: {}", multiplier);
    println!("Optimized chunk size: {} bytes", chunk_size);
    println!("##############################################\n\n");

    let chunk_starts: Vec<u64> = (0..file_size).step_by(chunk_size as usize).collect();

    let stopwords = read_stop_words().unwrap();
    

    let freqs: Vec<_> = chunk_starts
        .par_iter()
        .map(|&start| {
            let end = std::cmp::min(start + chunk_size, file_size);
            count_words(path, start, end, &stopwords).unwrap()
        })
        .collect();

    print_top_k(freqs, k);

    let duration = start_time.elapsed();
    println!("\nTime elapsed is: {:?}\n\n", duration);
}
