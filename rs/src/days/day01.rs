use crate::common::*;

pub fn run() {
    let day = 1;
    let input = get_input_strs(&day).unwrap();

    let mut elfs: Vec<i32> = Vec::new();
    let mut s = 0;
    for i in input {
        if i.is_empty() {
            elfs.push(s);
            s = 0;
            continue;
        }
        s += i.parse::<i32>().unwrap()
    }
    // and the last elf total
    if s > 0 {
        elfs.push(s);
    }

    // elfs.sort();
    // let part1 = elfs.last().unwrap();
    // let part2 = &elfs[elfs.len() - 3..].iter().sum::<i32>();
    // print_day_results(&day, part1, part2);

    // or
    // elfs.sort();
    // elfs.reverse();
    // let part1 = elfs[0];
    // let part2 = elfs.iter().take(3).sum::<i32>();
    // print_day_results(&day, &part1, &part2);

    // or
    elfs.sort();
    let part1 = elfs[elfs.len() - 1];
    let part2 = elfs.iter().rev().take(3).sum::<i32>();
    print_day_results(&day, &part1, &part2);

}