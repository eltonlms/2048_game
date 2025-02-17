<?php

define("SIZE", 4);
$grid = [];

// ANSI color codes for different tile values
$colors = [
    0 => "\e[90m",      // Gray for empty cells
    2 => "\e[37m",      // White
    4 => "\e[36m",      // Cyan
    8 => "\e[34m",      // Blue
    16 => "\e[32m",     // Green
    32 => "\e[33m",     // Yellow
    64 => "\e[31m",     // Red
    128 => "\e[35m",    // Purple
    256 => "\e[36;1m",  // Bright Cyan
    512 => "\e[34;1m",  // Bright Blue
    1024 => "\e[32;1m", // Bright Green
    2048 => "\e[33;1m", // Bright Yellow
    "reset" => "\e[0m"  // Reset color
];

/**
 * Initialize the game board with two starting tiles
 */
function init_grid() {
    global $grid;
    $grid = array_fill(0, SIZE, array_fill(0, SIZE, 0));
    add_tile();
    add_tile();
}

/**
 * Add a new tile (2 or 4) to an empty space
 */
function add_tile() {
    global $grid;
    $empty = [];

    for ($y = 0; $y < SIZE; $y++) {
        for ($x = 0; $x < SIZE; $x++) {
            if ($grid[$y][$x] === 0) {
                $empty[] = [$y, $x];
            }
        }
    }

    if (count($empty) > 0) {
        [$y, $x] = $empty[array_rand($empty)];
        $grid[$y][$x] = (rand(0, 9) < 9) ? 2 : 4;
    }
}

/**
 * Print the grid with ANSI colors
 */
function print_grid() {
    global $grid, $colors;
    
    system('clear'); // Clear the terminal screen (use 'cls' on Windows)
    echo "\n\e[1;37m2048 Game in PHP (Colored CLI Version)\e[0m\n";
    echo "Use \e[1;32mW/A/S/D\e[0m to move, \e[1;31mQ\e[0m to quit\n\n";

    foreach ($grid as $row) {
        echo "+------+------+------+------+\n"; // Table border
        foreach ($row as $cell) {
            $color = $colors[$cell] ?? "\e[0m"; // Default color if not in array
            $value = $cell ?: "."; // Show "." for empty cells
            echo "| {$color}" . str_pad($value, 4, " ", STR_PAD_BOTH) . "\e[0m ";
        }
        echo "|\n";
    }
    echo "+------+------+------+------+\n"; // Bottom border
}

/**
 * Slide and merge a row to the left
 */
function slide_merge_row($row) {
    $new_row = array_values(array_filter($row)); // Remove zeros
    while (count($new_row) < SIZE) {
        $new_row[] = 0;
    }

    for ($i = 0; $i < SIZE - 1; $i++) {
        if ($new_row[$i] !== 0 && $new_row[$i] === $new_row[$i + 1]) {
            $new_row[$i] *= 2;
            $new_row[$i + 1] = 0;
        }
    }

    return array_values(array_filter($new_row)) + array_fill(0, SIZE, 0);
}

/**
 * Move the grid in the given direction
 */
function move_grid($direction) {
    global $grid;
    $old_grid = $grid;

    if ($direction === "left") {
        for ($y = 0; $y < SIZE; $y++) {
            $grid[$y] = slide_merge_row($grid[$y]);
        }
    } elseif ($direction === "right") {
        for ($y = 0; $y < SIZE; $y++) {
            $grid[$y] = array_reverse(slide_merge_row(array_reverse($grid[$y])));
        }
    } elseif ($direction === "up") {
        for ($x = 0; $x < SIZE; $x++) {
            $col = array_column($grid, $x);
            $col = slide_merge_row($col);
            for ($y = 0; $y < SIZE; $y++) {
                $grid[$y][$x] = $col[$y];
            }
        }
    } elseif ($direction === "down") {
        for ($x = 0; $x < SIZE; $x++) {
            $col = array_reverse(array_column($grid, $x));
            $col = slide_merge_row($col);
            $col = array_reverse($col);
            for ($y = 0; $y < SIZE; $y++) {
                $grid[$y][$x] = $col[$y];
            }
        }
    }

    if ($grid !== $old_grid) {
        add_tile();
    }
}

/**
 * Check if there are no moves left (game over)
 */
function check_game_over() {
    global $grid;

    // Check for empty tiles
    foreach ($grid as $row) {
        if (in_array(0, $row, true)) {
            return false;
        }
    }

    // Check for adjacent matching tiles
    for ($y = 0; $y < SIZE; $y++) {
        for ($x = 0; $x < SIZE; $x++) {
            if (($x < SIZE - 1 && $grid[$y][$x] === $grid[$y][$x + 1]) ||
                ($y < SIZE - 1 && $grid[$y][$x] === $grid[$y + 1][$x])) {
                return false;
            }
        }
    }

    return true;
}

/**
 * Main game loop
 */
function game_loop() {
    init_grid();

    while (true) {
        print_grid();

        // Check for game over
        if (check_game_over()) {
            echo "\n\e[1;31mGame Over! No more moves available.\e[0m\n";
            break;
        }

        echo "\nMove (\e[1;32mW/A/S/D\e[0m) or Quit (\e[1;31mQ\e[0m): ";
        $input = strtolower(trim(fgets(STDIN)));

        if ($input === 'q') {
            echo "\e[1;31mExiting game.\e[0m\n";
            break;
        } elseif (in_array($input, ['w', 'a', 's', 'd'])) {
            $direction = ['w' => "up", 'a' => "left", 's' => "down", 'd' => "right"][$input];
            move_grid($direction);
        }
    }
}

// Run the game
game_loop();

?>
