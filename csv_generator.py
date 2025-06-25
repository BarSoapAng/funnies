#!/usr/bin/env python3
import csv
import sys

def generate_wall_csv(rows: int, cols: int, filename: str):
    """
    Generates a CSV file of size rows x cols with a border of 1's and 0's inside.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for r in range(rows):
            row = []
            for c in range(cols):
                # if on first or last row, or first or last column → wall
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    row.append(1)
                else:
                    row.append(0)
            writer.writerow(row)

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <rows> <cols> <output.csv>")
        sys.exit(1)

    rows = int(sys.argv[1])
    cols = int(sys.argv[2])
    out_file = sys.argv[3]

    if rows < 2 or cols < 2:
        print("Error: rows and cols must both be at least 2 to form a border.")
        sys.exit(1)

    generate_wall_csv(rows, cols, out_file)
    print(f"Wrote {rows}×{cols} CSV with border to '{out_file}'.")

if __name__ == "__main__":
    main()
