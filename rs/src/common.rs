use std::fmt::Display;
use std::io::{
    BufRead
    , BufReader
    //, Read
};
use std::path::Path;

const MAX_SEARCH_LEVEL: i32 = 3;

fn find_input_file(day_no: &i32) -> Option<String> {
    let inname = format!("day{:02}-input", day_no);
    // Start from the current directory
    let mut dir = ".".to_string();
    let mut fname = format!("{}/{}", dir, inname);

    let mut level = 0;
    loop {
        if level > MAX_SEARCH_LEVEL {
            break None;
        }

        // look in dir
        if Path::new(&fname).exists() {
            break Some(fname);
        }

        // look in dir/input
        fname = format!("{}/input/{}", dir, inname);
        if Path::new(&fname).exists() {
            break Some(fname);
        }

        // go up to the parent directory
        dir = format!("{}/..", dir);
        level += 1;
    }
}

// fn get_input_ints_from_file(input_file: &str) -> Option<Vec<i32>> {
//     let mut file = std::fs::File::open(input_file).unwrap();

//     // Read in content
//     let mut content = String::new();
//     file.read_to_string(&mut content).unwrap();
//     // Parse ints from content
//     let mut v: Vec<i32> = Vec::new();
//     for s in content.lines() {
//         v.push(s.parse::<i32>().unwrap());
//     }
//     return Some(v);
// }

fn get_input_strs_from_file(input_file: &str) -> Vec<String> {
    let file = std::fs::File::open(input_file).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

// pub fn get_input_ints(day: &i32) -> Option<Vec<i32>> {
//     let fname: String;
//     let findfile = find_input_file(day);
//     match findfile {
//         Some(s) => fname = s,
//         None => panic!("Cannot find input file for day {}", day),
//     }

//     let vopt = get_input_ints_from_file(&fname);
//     match vopt {
//         Some(v) => return Some(v),
//         None => panic!("Failed to load ints from input file {} for day {}", fname, day),
//     }
// }

pub fn get_input_strs(day: &i32) -> Option<Vec<String>> {
    let fname: String;
    let findfile = find_input_file(day);
    match findfile {
        Some(s) => fname = s,
        None => panic!("Cannot find input file for day {}", day),
    }

    let vopt = get_input_strs_from_file(&fname);
    return Some(vopt);
}

// pub fn print_day_result<T : Display>(day: i32, part_no: i32, result: T) {
//     println!("Day {}", day);
//     println!("  Part {}: {}", part_no, result);
// }

pub fn print_day_results<T: Display>(day: &i32, part1: &T, part2: &T) {
    println!("Day {}", day);
    println!("  Part 1: {}", part1);
    println!("  Part 2: {}", part2);
    println!();
}
