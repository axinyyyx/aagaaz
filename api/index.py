'''
Developer: RISHABH SAHIL { CODER BHAI 🔥 }
Description: Aagaaz is my platform to share my love for math and puzzles.
             It features Sudoku generators and math quizzes in Mathemania to help sharpen minds.
             I designed it for fun and learning at all levels.
'''

from flask import Flask, render_template, jsonify, request
import random
import copy
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def is_valid(board, row, col, num):
    """Check if placing num at board[row][col] is valid."""
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board):
    """Solve the Sudoku board using backtracking."""
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
    """Validate if the Sudoku board is correct."""
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
    """Generate a Sudoku puzzle with specified difficulty."""
    try:
        clues = {'easy': 50, 'medium': 40, 'hard': 30}.get(level, 40)
        board = [[0 for _ in range(9)] for _ in range(9)]
        solve_sudoku(board)
        solved_board = copy.deepcopy(board)
        cells_to_remove = 81 - clues
        while cells_to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if board[row][col] != 0:
                temp = board[row][col]
                board[row][col] = 0
                temp_board = copy.deepcopy(board)
                if solve_sudoku(temp_board):
                    cells_to_remove -= 1
                else:
                    board[row][col] = temp
        return board, solved_board
    except Exception as e:
        logger.error(f"Error generating Sudoku: {str(e)}")
        raise

def generate_questions(level='easy', num_questions=10):
    """Generate math questions for Mathemania."""
    try:
        # Validate inputs
        if not isinstance(num_questions, int) or num_questions < 1 or num_questions > 50:
            num_questions = 10
        level = level if level in ['easy', 'medium', 'hard'] else 'easy'

        questions = []
        types = ['deductive', 'inductive', 'arithmetic', 'algebra', 'geometry', 'logic', 'reasoning']
        
        for _ in range(num_questions):
            q_type = random.choice(types)
            question = {}

            if q_type == 'deductive':
                p, q = random.choice([(True, True), (True, False), (False, True)])
                q_text = f"If P is {p} and (P implies Q) is True, is Q {q}?"
                options = ['Yes', 'No', 'Cannot determine']
                correct_idx = 0 if q else 1
                question = {'question': q_text, 'options': options, 'correct': correct_idx, 'type': q_type}

            elif q_type == 'inductive':
                if level == 'easy':
                    seq, predicted, pattern = [1, 3, 5, 7], 9, "Sequence of odd numbers (increase by 2)"
                elif level == 'medium':
                    seq, predicted, pattern = [2, 4, 8, 16], 32, "Sequence of powers of 2 (multiply by 2)"
                else:
                    seq, predicted, pattern = [1, 4, 9, 16], 25, "Sequence of squares (1^2, 2^2, 3^2, 4^2, ...)"
                q_text = f"What is next in {seq}? Pattern: {pattern}"
                options = [predicted] + [predicted + random.randint(-5, 5) for _ in range(3)]
                random.shuffle(options)
                question = {'question': q_text, 'options': options, 'correct': options.index(predicted), 'type': q_type}

            elif q_type == 'arithmetic':
                if level == 'easy':
                    a, b = random.randint(1, 20), random.randint(1, 20)
                    op = random.choice(['+', '-', '*', '/'])
                    if op == '/':
                        b = random.choice([1, 2, 4, 5, 10])
                        correct = a // b if a % b == 0 else round(a / b, 2)
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
                else:
                    a, b, c = random.randint(50, 200), random.randint(10, 50), random.randint(5, 20)
                    correct = (a + b) * c - a
                    q_text = f"Compute ({a} + {b}) * {c} - {a}?"
                options = [correct] + [correct + random.randint(-20, 20) for _ in range(3)]
                if isinstance(correct, float):
                    options = [round(o, 2) for o in options]
                random.shuffle(options)
                question = {'question': q_text, 'options': options, 'correct': options.index(correct), 'type': q_type}

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
                    q_text = f"What is ({a} + {b})²?"
                options = [correct] + [correct + random.randint(-10, 10) for _ in range(3)]
                random.shuffle(options)
                question = {'question': q_text, 'options': options, 'correct': options.index(correct), 'type': q_type}

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
                    correct = 2 * (l + w)
                    q_text = f"Perimeter of rectangle {l} x {w}?"
                    options = [correct] + [correct + random.randint(-5, 5) for _ in range(3)]
                random.shuffle(options)
                question = {'question': q_text, 'options': options, 'correct': options.index(correct if not isinstance(correct, float) else round(correct, 2)), 'type': q_type}

            elif q_type == 'logic':
                if level == 'easy':
                    seq, correct = [2, 4, 6, 8], 10
                    q_text = f"Next in sequence: 2, 4, 6, 8, ...?"
                elif level == 'medium':
                    seq, correct = [1, 4, 9, 16], 25
                    q_text = f"Next: 1, 4, 9, 16, ...?"
                else:
                    seq, correct = [3, 6, 9, 12], 15
                    q_text = f"Next: 3, 6, 9, 12, ...?"
                options = [correct] + [correct + random.randint(-5, 5) for _ in range(3)]
                random.shuffle(options)
                question = {'question': q_text, 'options': options, 'correct': options.index(correct), 'type': q_type}

            else:  # reasoning
                if level == 'easy':
                    q_text, correct = "If A is taller than B, and B is taller than C, who is shortest?", "C"
                    options = ["A", "B", "C", "Equal"]
                elif level == 'medium':
                    q_text, correct = "A man has 3 sons. Each son has a sister. How many children?", "4"
                    options = ["3", "4", "6", "7"]
                else:
                    q_text, correct = "What can run but never walks, has a mouth but never talks?", "River"
                    options = ["River", "Wind", "Clock", "Car"]
                question = {'question': q_text, 'options': options, 'correct': options.index(correct), 'type': q_type}

            questions.append(question)

        random.shuffle(questions)
        return questions
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        return []

@app.route('/')
@app.route('/sudoku')
def sudoku():
    try:
        return render_template('sudoku.html')
    except Exception as e:
        logger.error(f"Error rendering sudoku.html: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/generate_sudoku')
def generate_sudoku_route():
    try:
        level = request.args.get('level', 'medium')
        puzzle, solution = generate_sudoku(level)
        return jsonify({'puzzle': puzzle, 'solution': solution, 'level': level})
    except Exception as e:
        logger.error(f"Error in generate_sudoku_route: {str(e)}")
        return jsonify({'error': 'Failed to generate Sudoku'}), 500

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        if not data or 'board' not in data:
            return jsonify({'error': 'Invalid board data'}), 400
        board = [row[:] for row in data['board']]
        solved = solve_sudoku(board)
        return jsonify({'solved': solved, 'board': board})
    except Exception as e:
        logger.error(f"Error in solve route: {str(e)}")
        return jsonify({'error': 'Failed to solve Sudoku'}), 500

@app.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.json
        if not data or 'board' not in data:
            return jsonify({'error': 'Invalid board data'}), 400
        board = [row[:] for row in data['board']]
        is_valid = validate_sudoku(board)
        return jsonify({'valid': is_valid})
    except Exception as e:
        logger.error(f"Error in validate route: {str(e)}")
        return jsonify({'error': 'Failed to validate Sudoku'}), 500

@app.route('/mathemania')
def mathemania():
    try:
        return render_template('mathemania.html')
    except Exception as e:
        logger.error(f"Error rendering mathemania.html: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/generate_questions')
def generate_questions_route():
    try:
        level = request.args.get('level', 'easy')
        num = int(request.args.get('num', 10))
        questions = generate_questions(level, num)
        if not questions:
            return jsonify({'error': 'Failed to generate questions'}), 500
        return jsonify({'questions': questions, 'level': level})
    except ValueError:
        logger.error(f"Invalid num parameter in generate_questions_route")
        return jsonify({'error': 'Invalid number of questions'}), 400
    except Exception as e:
        logger.error(f"Error in generate_questions_route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/about')
def about():
    try:
        return render_template('about.html')
    except Exception as e:
        logger.error(f"Error rendering about.html: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# if __name__ == '__main__':
#     app.run(debug=True)