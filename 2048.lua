math.randomseed(os.time())

-- Initialize the 4x4 grid with zeros
grid = {}
for i = 1, 4 do
    grid[i] = {0, 0, 0, 0}
end

-- Function to print the grid
function print_grid()
    for i = 1, 4 do
        for j = 1, 4 do
            io.write(string.format("%4d", grid[i][j]))
        end
        print()
    end
    print()
end

-- Function to add a new random tile (2 or 4)
function place_random_tile()
    local empty = {}
    for i = 1, 4 do
        for j = 1, 4 do
            if grid[i][j] == 0 then
                table.insert(empty, {i, j})
            end
        end
    end
    if #empty > 0 then
        local pos = empty[math.random(#empty)]
        grid[pos[1]][pos[2]] = (math.random() < 0.9) and 2 or 4
    end
end

-- Slide and merge function
function move_left()
    local moved = false
    for i = 1, 4 do
        local new_row = {}
        for j = 1, 4 do
            if grid[i][j] ~= 0 then
                table.insert(new_row, grid[i][j])
            end
        end
        
        for j = 1, #new_row - 1 do
            if new_row[j] == new_row[j + 1] then
                new_row[j] = new_row[j] * 2
                table.remove(new_row, j + 1)
            end
        end
        
        while #new_row < 4 do
            table.insert(new_row, 0)
        end
        
        for j = 1, 4 do
            if grid[i][j] ~= new_row[j] then
                moved = true
            end
            grid[i][j] = new_row[j]
        end
    end
    return moved
end

function move_right()
    for i = 1, 4 do
        grid[i] = {grid[i][4], grid[i][3], grid[i][2], grid[i][1]}
    end
    local moved = move_left()
    for i = 1, 4 do
        grid[i] = {grid[i][4], grid[i][3], grid[i][2], grid[i][1]}
    end
    return moved
end

function move_up()
    local transposed = {}
    for i = 1, 4 do
        transposed[i] = {}
        for j = 1, 4 do
            transposed[i][j] = grid[j][i]
        end
    end
    grid = transposed
    local moved = move_left()
    transposed = {}
    for i = 1, 4 do
        transposed[i] = {}
        for j = 1, 4 do
            transposed[i][j] = grid[j][i]
        end
    end
    grid = transposed
    return moved
end

function move_down()
    local transposed = {}
    for i = 1, 4 do
        transposed[i] = {}
        for j = 1, 4 do
            transposed[i][j] = grid[j][i]
        end
    end
    grid = transposed
    local moved = move_right()
    transposed = {}
    for i = 1, 4 do
        transposed[i] = {}
        for j = 1, 4 do
            transposed[i][j] = grid[j][i]
        end
    end
    grid = transposed
    return moved
end

-- Check for win condition
function check_win()
    for i = 1, 4 do
        for j = 1, 4 do
            if grid[i][j] == 2048 then
                return true
            end
        end
    end
    return false
end

-- Check for game over
function check_game_over()
    for i = 1, 4 do
        for j = 1, 4 do
            if grid[i][j] == 0 then
                return false
            end
            if j < 4 and grid[i][j] == grid[i][j + 1] then
                return false
            end
            if i < 4 and grid[i][j] == grid[i + 1][j] then
                return false
            end
        end
    end
    return true
end

-- Main game loop
place_random_tile()
place_random_tile()
while true do
    print_grid()
    print("Use WASD to move (w=up, s=down, a=left, d=right). Enter 'q' to quit.")
    local move = io.read()
    local valid_move = false
    
    if move == "a" then
        valid_move = move_left()
    elseif move == "d" then
        valid_move = move_right()
    elseif move == "w" then
        valid_move = move_up()
    elseif move == "s" then
        valid_move = move_down()
    elseif move == "q" then
        print("Goodbye!")
        break
    end
    
    if valid_move then
        place_random_tile()
    end
    
    if check_win() then
        print("Congratulations! You reached 2048!")
        break
    elseif check_game_over() then
        print("Game Over!")
        break
    end
end
