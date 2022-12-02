use crate::common::*;

fn get_points(a: &str) -> i32 {
    match a {
        "A" | "X" => 1,
        "B" | "Y" => 2,
        "C" | "Z" => 3,
        _ => panic!("WTF")
    }
}

fn get_score(a: &str, b: &str) -> i32 {
    let pa = get_points(a);
    let pb = get_points(b);
    let is_win = pb % 3 == (pa + 1) % 3;

    if pa == pb { 3 + pb } else if is_win { 6 + pb } else { pb }
}

pub fn run() {
    let day = 2;
    let input = get_input_strs(&day).unwrap();
    let mut part1 = 0;
    let mut part2 = 0;
    for i in input {
        let spl: Vec<&str> = i.split(' ').collect();
        part1 += get_score(spl[0], spl[1]);

        // Part 2
        let pp1 = get_points(spl[0]);
        match spl[1] {
            "X" => part2 += ((pp1 + 1) % 3) + 1,  // Lose
            "Y" => part2 += 3 + pp1,              // Draw
            "Z" => part2 += 6 + ((pp1 % 3) + 1),  // Win
            _ => panic!("WTF")
        }
    }
    print_day_results(&day, &part1, &part2);
}