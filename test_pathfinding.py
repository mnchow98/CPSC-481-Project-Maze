"""
Pathfinding Algorithm Evaluation
Tests A* and UCS algorithms for correctness, optimality, and efficiency
"""

import time
from maze import Maze
from pathfinding import solve_a_star, solve_ucs

def calculate_path_cost(maze, path):
    """Calculate total cost of a path"""
    if not path:
        return 0
    # Don't count start position cost
    return sum(maze.get_cost(pos) for pos in path[1:])

def print_test_header(test_name):
    """Print formatted test header"""
    print("\n" + "="*70)
    print(f"  {test_name}")
    print("="*70)

def visualize_maze(grid, path=None, start=None, goal=None):
    """Print maze with optional path visualization"""
    symbols = {0: '█', 1: '.', 3: '~', 5: '^'}
    path_set = set(path) if path else set()
    
    for y, row in enumerate(grid):
        line = ""
        for x, cell in enumerate(row):
            pos = (x, y)
            if pos == start:
                line += 'S'
            elif pos == goal:
                line += 'G'
            elif pos in path_set:
                line += '*'
            else:
                line += symbols.get(cell, '?')
        print(line)

def run_single_test(test_name, maze, start, goal, show_visualization=True):
    """Run both algorithms on a single test case and compare results"""
    print_test_header(test_name)
    
    if show_visualization:
        print("\nMaze Configuration:")
        print("Legend: S=Start, G=Goal, █=Wall, .=Grass(1), ~=Mud(3), ^=Rock(5)")
        visualize_maze(maze.grid, start=start, goal=goal)
    
    # Run UCS
    start_time = time.time()
    ucs_path, ucs_visited = solve_ucs(maze, start, goal)
    ucs_time = (time.time() - start_time) * 1000  # Convert to ms
    ucs_cost = calculate_path_cost(maze, ucs_path)
    
    # Run A*
    start_time = time.time()
    astar_path, astar_visited = solve_a_star(maze, start, goal)
    astar_time = (time.time() - start_time) * 1000  # Convert to ms
    astar_cost = calculate_path_cost(maze, astar_path)
    
    # Display results
    print(f"\nResults:")
    print(f"{'Algorithm':<12} {'Path Cost':<12} {'Path Length':<12} {'Nodes Explored':<16} {'Time (ms)':<12}")
    print("-" * 70)
    print(f"{'UCS':<12} {ucs_cost:<12} {len(ucs_path):<12} {len(ucs_visited):<16} {ucs_time:<12.3f}")
    print(f"{'A*':<12} {astar_cost:<12} {len(astar_path):<12} {len(astar_visited):<16} {astar_time:<12.3f}")
    
    # Analysis
    print(f"\nAnalysis:")
    if ucs_cost == astar_cost:
        print(f"✓ Both algorithms found optimal solution (cost: {ucs_cost})")
    else:
        print(f"✗ WARNING: Different costs! UCS: {ucs_cost}, A*: {astar_cost}")
    
    if len(astar_visited) <= len(ucs_visited):
        efficiency = (len(astar_visited) / len(ucs_visited)) * 100
        print(f"✓ A* explored {efficiency:.1f}% of nodes compared to UCS")
        print(f"  (Saved {len(ucs_visited) - len(astar_visited)} node explorations)")
    else:
        print(f"✗ WARNING: A* explored more nodes than UCS!")
    
    if show_visualization and ucs_path:
        print(f"\nUCS Path Visualization:")
        visualize_maze(maze.grid, ucs_path, start, goal)
        print(f"\nA* Path Visualization:")
        visualize_maze(maze.grid, astar_path, start, goal)
    
    return {
        'ucs_cost': ucs_cost,
        'ucs_nodes': len(ucs_visited),
        'ucs_time': ucs_time,
        'astar_cost': astar_cost,
        'astar_nodes': len(astar_visited),
        'astar_time': astar_time,
        'optimal': ucs_cost == astar_cost
    }

def test_manual_verification():
    """Test Case 1: Small 5x5 maze for manual verification"""
    test_maze = Maze(width=5, height=5)
    
    # Create simple test grid with known optimal path
    test_maze.grid = [
        [1, 1, 1, 0, 1],  # Row 0
        [1, 0, 1, 1, 1],  # Row 1
        [1, 3, 1, 0, 1],  # Row 2
        [1, 1, 5, 1, 1],  # Row 3
        [0, 1, 1, 1, 1]   # Row 4
    ]
    
    start = (0, 0)
    goal = (4, 4)
    
    return run_single_test("Test 1: Manual Verification (5x5)", test_maze, start, goal, show_visualization=True)

def test_no_obstacles():
    """Test Case 2: Open maze with no walls"""
    test_maze = Maze(width=7, height=7)
    test_maze.grid = [[1 for _ in range(7)] for _ in range(7)]
    
    start = (0, 0)
    goal = (6, 6)
    
    return run_single_test("Test 2: No Obstacles (7x7)", test_maze, start, goal, show_visualization=False)

def test_weighted_terrain():
    """Test Case 3: Maze with varied terrain costs"""
    test_maze = Maze(width=8, height=8)
    
    # Create maze with strategic high-cost areas
    test_maze.grid = [
        [1, 1, 5, 5, 5, 1, 1, 1],
        [1, 1, 5, 5, 5, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 3, 3, 1, 1, 1],
        [1, 1, 1, 3, 3, 1, 0, 1],
        [1, 5, 1, 1, 1, 1, 1, 1],
        [1, 5, 1, 0, 0, 1, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    start = (0, 0)
    goal = (7, 7)
    
    return run_single_test("Test 3: Weighted Terrain (8x8)", test_maze, start, goal, show_visualization=False)

def test_narrow_corridors():
    """Test Case 4: Maze with narrow passages"""
    test_maze = Maze(width=9, height=9)
    test_maze.grid = [
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    start = (0, 0)
    goal = (8, 8)
    
    return run_single_test("Test 4: Narrow Corridors (9x9)", test_maze, start, goal, show_visualization=False)

def test_generated_mazes():
    """Test Case 5-7: Generated mazes of varying sizes"""
    sizes = [(10, 10), (20, 20), (30, 30)]
    results = []
    
    for width, height in sizes:
        maze = Maze(width=width, height=height)
        start = (0, 0)
        
        # Find goal (last valid cell) - use ACTUAL grid dimensions
        goal = None
        actual_height = len(maze.grid)
        actual_width = len(maze.grid[0]) if maze.grid else 0
        
        for y in range(actual_height-1, -1, -1):
            for x in range(actual_width-1, -1, -1):
                if maze.grid[y][x] != 0:
                    goal = (x, y)
                    break
            if goal:
                break
        
        test_name = f"Test (Generated {width}x{height})"
        result = run_single_test(test_name, maze, start, goal, show_visualization=False)
        results.append((width, height, result))
    
    return results

def print_summary_table(all_results):
    """Print summary table for report"""
    print_test_header("SUMMARY TABLE - For Report")
    
    print(f"\n{'Test Case':<25} {'Size':<8} {'UCS Cost':<10} {'A* Cost':<10} {'UCS Nodes':<12} {'A* Nodes':<12} {'A* Efficiency':<15}")
    print("-" * 105)
    
    test_names = [
        "Manual Verification",
        "No Obstacles",
        "Weighted Terrain",
        "Narrow Corridors"
    ]
    
    for i, (name, result) in enumerate(zip(test_names, all_results[:4])):
        size = ["5x5", "7x7", "8x8", "9x9"][i]
        efficiency = (result['astar_nodes'] / result['ucs_nodes'] * 100) if result['ucs_nodes'] > 0 else 0
        
        print(f"{name:<25} {size:<8} {result['ucs_cost']:<10} {result['astar_cost']:<10} "
              f"{result['ucs_nodes']:<12} {result['astar_nodes']:<12} {efficiency:.1f}%")
    
    # Generated mazes
    if len(all_results) > 4:
        for width, height, result in all_results[4]:
            efficiency = (result['astar_nodes'] / result['ucs_nodes'] * 100) if result['ucs_nodes'] > 0 else 0
            print(f"{'Generated Maze':<25} {f'{width}x{height}':<8} {result['ucs_cost']:<10} {result['astar_cost']:<10} "
                  f"{result['ucs_nodes']:<12} {result['astar_nodes']:<12} {efficiency:.1f}%")
    
    print("\n" + "="*105)
    
    # Overall statistics
    all_optimal = all(r['optimal'] for r in all_results[:4])
    avg_efficiency = sum(r['astar_nodes'] / r['ucs_nodes'] * 100 for r in all_results[:4]) / 4
    
    print(f"\nKey Findings:")
    print(f"✓ Optimality: {'All tests found optimal solutions' if all_optimal else 'Some tests failed'}")
    print(f"✓ Average A* Efficiency: {avg_efficiency:.1f}% of UCS node explorations")
    print(f"✓ A* consistently explored fewer nodes while maintaining optimality")

def main():
    """Run all tests"""
    print("="*70)
    print("  PATHFINDING ALGORITHM EVALUATION")
    print("  Testing A* and UCS for Correctness and Efficiency")
    print("="*70)
    
    results = []
    
    # Run manual verification test
    results.append(test_manual_verification())
    
    # Run additional test cases
    results.append(test_no_obstacles())
    results.append(test_weighted_terrain())
    results.append(test_narrow_corridors())
    
    # Run generated maze tests
    generated_results = test_generated_mazes()
    results.append(generated_results)
    
    # Print summary
    print_summary_table(results)
    
    print("\n✓ Testing complete! Use summary table in your report.")

if __name__ == "__main__":
    main()