from flask import Flask, render_template, jsonify, request
import random
import copy

# Install: pip install reasoning-library
from reasoning_library.core import ReasoningChain
from reasoning_library.deductive import apply_modus_ponens
from reasoning_library.inductive import predict_next_in_sequence, find_pattern_description

app = Flask(__name__)

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def validate_sudoku(board):
    # Check rows, columns, subgrids
    for i in range(9):
        row = [board[i][j] for j in range(9) if board[i][j] != 0]
        col = [board[j][i] for j in range(9) if board[j][i] != 0]
        if len(set(row)) != len(row) or len(set(col)) != len(col):
            return False
    
    for box in range(9):
        start_row, start_col = (box // 3) * 3, (box % 3) * 3
        subgrid = [board[start_row + i][start_col + j] for i in range(3) for j in range(3) if board[start_row + i][start_col + j] != 0]
        if len(set(subgrid)) != len(subgrid):
            return False
    return True

def generate_sudoku(level='medium'):
    clues = {'easy': 50, 'medium': 40, 'hard': 30}[level]
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(board)
    solved_board = copy.deepcopy(board)
    cells_to_remove = 81 - clues
    while cells_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:
            temp = board[row][col]
            board[row][col] = 0
            temp_board = copy.deepcopy(board)
            if solve_sudoku(temp_board):
                cells_to_remove -= 1
            else:
                board[row][col] = temp
    return board, solved_board

def generate_questions(level, num_questions=10):
    questions = []
    chain = ReasoningChain()
    types = ['deductive', 'inductive', 'arithmetic', 'algebra', 'geometry', 'logic', 'reasoning']
    for _ in range(num_questions):
        q_type = random.choice(types)
        if q_type == 'deductive':
            p, q = random.choice([(True, True), (True, False), (False, True)])
            chain.clear()
            result = apply_modus_ponens(p, q, reasoning_chain=chain)
            q_text = f"If P is {p} and (P implies Q) is True, is Q {q}?"
            options = ['Yes', 'No', 'Cannot determine']
            correct_idx = 0 if result == q else 1
            questions.append({'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type})
        elif q_type == 'inductive':
            if level == 'easy':
                seq = [1, 3, 5, 7]
            elif level == 'medium':
                seq = [2, 4, 8, 16]
            else:
                seq = [1, 4, 9, 16]
            chain.clear()
            predicted = predict_next_in_sequence(seq, reasoning_chain=chain)
            pattern = find_pattern_description(seq, reasoning_chain=chain)
            q_text = f"What is next in {seq}? Pattern: {pattern}"
            options = [predicted] + [predicted + random.randint(-5, 5) for _ in range(3)]
            random.shuffle(options)
            correct_idx = options.index(predicted)
            questions.append({'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type})
        elif q_type == 'arithmetic':
            if level == 'easy':
                a, b = random.randint(1, 20), random.randint(1, 20)
                op = random.choice(['+', '-', '*', '/'])
                if op == '/': b = random.choice([1,2,4,5,10]); correct = a // b if a % b == 0 else a / b
                elif op == '+': correct = a + b
                elif op == '-': a, b = max(a, b), min(a, b); correct = a - b
                else: correct = a * b
                q_text = f"What is {a} {op} {b}?"
            elif level == 'medium':
                a, b = random.randint(20, 100), random.randint(5, 20)
                op = random.choice(['+', '-', '*', '/'])
                if op == '/': correct = round(a / b, 2)
                elif op == '+': correct = a + b
                elif op == '-': correct = a - b
                else: correct = a * b
                q_text = f"What is {a} {op} {b}?"
            else:  # hard
                a, b, c = random.randint(50, 200), random.randint(10, 50), random.randint(5, 20)
                correct = (a + b) * c - a
                q_text = f"Compute ({a} + {b}) * {c} - {a}?"
            options = [correct] + [correct + random.randint(-20, 20) for _ in range(3)] 
            if isinstance(correct, float): options = [round(o, 2) for o in options]
            random.shuffle(options)
            correct_idx = options.index(correct)
            questions.append({'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type})
        elif q_type == 'algebra':
            if level == 'easy':
                x = random.randint(1, 10)
                correct = 2 * x + 5
                q_text = f"If x = {x}, what is 2x + 5?"
            elif level == 'medium':
                x = random.randint(5, 20)
                correct = x**2 - 3*x + 2
                q_text = f"Solve x² - 3x + 2 for x = {x}?"
            else:
                a, b = random.randint(2, 10), random.randint(1, 5)
                correct = a**2 + 2*a*b + b**2
                q_text = f"What is ( {a} + {b} )² ?"
            options = [correct] + [correct + random.randint(-10, 10) for _ in range(3)]
            random.shuffle(options)
            correct_idx = options.index(correct)
            questions.append({'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type})
        elif q_type == 'geometry':
            if level == 'easy':
                r = random.randint(1, 10)
                correct = 3.14 * r**2
                q_text = f"Area of circle with radius {r} (use π=3.14)?"
                options = [round(correct, 2)] + [round(correct + random.uniform(-5, 5), 2) for _ in range(3)]
            elif level == 'medium':
                s = random.randint(5, 15)
                correct = s**2
                q_text = f"Area of square with side {s}?"
                options = [correct] + [correct + random.randint(-10, 10) for _ in range(3)]
            else:
                l, w = random.randint(10, 20), random.randint(5, 10)
                correct = 2*(l + w)
                q_text = f"Perimeter of rectangle {l} x {w}?"
                options = [correct] + [correct + random.randint(-5, 5) for _ in range(3)]
            random.shuffle(options)
            correct_idx = options.index(correct if not isinstance(correct, float) else round(correct, 2))
            questions.append({'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type})
        elif q_type == 'logic':
            if level == 'easy':
                seq = [2, 4, 6, 8]
                correct = 10
                q_text = f"Next in sequence: 2, 4, 6, 8, ...?"
            elif level == 'medium':
                seq = [1, 4, 9, 16]
                correct = 25
                q_text = f"Next: 1, 4, 9, 16, ...?"
            else:
                seq = [3, 6, 9, 12]
                correct = 15
                q_text = f"Next: 3, 6, 9, 12, ...?"
            options = [correct] + [correct + random.randint(-5, 5) for _ in range(3)]
            random.shuffle(options)
            correct_idx = options.index(correct)
            questions.append({'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type})
        else:  # reasoning
            if level == 'easy':
                q_text = "If A is taller than B, and B is taller than C, who is shortest?"
                correct = "C"
                options = ["A", "B", "C", "Equal"]
            elif level == 'medium':
                q_text = "A man has 3 sons. Each son has a sister. How many children?"
                correct = "4"
                options = ["3", "4", "6", "7"]
            else:
                q_text = "What can run but never walks, has a mouth but never talks?"
                correct = "River"
                options = ["River", "Wind", "Clock", "Car"]
            correct_idx = options.index(correct)
            questions.append({'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type})
    random.shuffle(questions)
    return questions

@app.route('/')
@app.route('/sudoku')
def sudoku():
    return render_template('sudoku.html')

@app.route('/generate_sudoku')
def generate_sudoku_route():
    level = request.args.get('level', 'medium')
    puzzle, solution = generate_sudoku(level)
    return jsonify({'puzzle': puzzle, 'solution': solution, 'level': level})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    board = [row[:] for row in data['board']]
    solved = solve_sudoku(board)
    return jsonify({'solved': solved, 'board': board})

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    board = [row[:] for row in data['board']]
    is_valid = validate_sudoku(board)
    return jsonify({'valid': is_valid})

@app.route('/mathemania')
def mathemania():
    return render_template('mathemania.html')

@app.route('/generate_questions')
def generate_questions_route():
    level = request.args.get('level', 'easy')
    num = int(request.args.get('num', 10))
    questions = generate_questions(level, num)
    return jsonify({'questions': questions, 'level': level})

@app.route('/about')
def about():
    return render_template('about.html')

# if __name__ == '__main__':
#     app.run(debug=True)
