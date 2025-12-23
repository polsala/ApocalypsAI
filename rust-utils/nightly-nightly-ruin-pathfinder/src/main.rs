use std::env;
use std::fs;
use std::io::{self, Read};
use std::collections::VecDeque;

type Point = (usize, usize);

fn read_map(path_opt: Option<String>) -> io::Result<Vec<Vec<char>>> {
    let mut input = String::new();
    match path_opt {
        Some(p) => {
            input = fs::read_to_string(p)?;
        }
        None => {
            io::stdin().read_to_string(&mut input)?;
        }
    }
    let grid: Vec<Vec<char>> = input.lines().map(|l| l.chars().collect()).collect();
    Ok(grid)
}

fn find_start_end(grid: &Vec<Vec<char>>) -> Option<(Point, Point)> {
    let mut start = None;
    let mut end = None;
    for (y, row) in grid.iter().enumerate() {
        for (x, &c) in row.iter().enumerate() {
            if c == 'S' {
                start = Some((x, y));
            } else if c == 'E' {
                end = Some((x, y));
            }
        }
    }
    match (start, end) {
        (Some(s), Some(e)) => Some((s, e)),
        _ => None,
    }
}

fn bfs(grid: &Vec<Vec<char>>, start: Point, end: Point) -> Option<Vec<Point>> {
    let height = grid.len();
    let width = grid[0].len();
    let mut visited = vec![vec![false; width]; height];
    let mut prev: Vec<Vec<Option<Point>>> = vec![vec![None; width]; height];
    let mut q = VecDeque::new();
    q.push_back(start);
    visited[start.1][start.0] = true;

    let dirs = [(0i32, 1i32), (1, 0), (-1, 0), (0, -1)];
    while let Some((x, y)) = q.pop_front() {
        if (x, y) == end {
            // reconstruct path
            let mut path = Vec::new();
            let mut cur = Some(end);
            while let Some(p) = cur {
                path.push(p);
                cur = prev[p.1][p.0];
            }
            path.reverse();
            return Some(path);
        }
        for (dx, dy) in dirs.iter() {
            let nx = x as i32 + dx;
            let ny = y as i32 + dy;
            if nx >= 0 && ny >= 0 && (nx as usize) < width && (ny as usize) < height {
                let nxu = nx as usize;
                let nyu = ny as usize;
                if !visited[nyu][nxu] && grid[nyu][nxu] != '#' {
                    visited[nyu][nxu] = true;
                    prev[nyu][nxu] = Some((x, y));
                    q.push_back((nxu, nyu));
                }
            }
        }
    }
    None
}

fn mark_path(mut grid: Vec<Vec<char>>, path: &Vec<Point>) -> Vec<Vec<char>> {
    // Skip the first (S) and last (E) points
    for &(x, y) in path.iter().skip(1).take(path.len() - 2) {
        if grid[y][x] == '.' {
            grid[y][x] = '*';
        }
    }
    grid
}

fn print_grid(grid: &Vec<Vec<char>>) {
    for row in grid {
        let line: String = row.iter().collect();
        println!("{}", line);
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let path_opt = if args.len() > 1 { Some(args[1].clone()) } else { None };
    let grid = match read_map(path_opt) {
        Ok(g) => g,
        Err(e) => {
            eprintln!("Failed to read map: {}", e);
            std::process::exit(1);
        }
    };
    let (start, end) = match find_start_end(&grid) {
        Some(se) => se,
        None => {
            eprintln!("Map must contain exactly one 'S' and one 'E'");
            std::process::exit(1);
        }
    };
    match bfs(&grid, start, end) {
        Some(path) => {
            let marked = mark_path(grid, &path);
            print_grid(&marked);
        }
        None => {
            println!("No path found");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_path() {
        let input = vec![
            vec!['S', '.', '.', '#'],
            vec!['.', '#', '#', '.'],
            vec!['.', '.', '.', 'E'],
        ];
        let path = bfs(&input, (0, 0), (3, 2)).expect("path");
        let marked = mark_path(input.clone(), &path);
        let expected = vec![
            vec!['S', '*', '*', '#'],
            vec!['.', '#', '#', '*'],
            vec!['.', '.', '.', 'E'],
        ];
        assert_eq!(marked, expected);
    }

    #[test]
    fn test_no_path() {
        let input = vec![
            vec!['S', '#'],
            vec!['#', 'E'],
        ];
        assert!(bfs(&input, (0, 0), (1, 1)).is_none());
    }
}
