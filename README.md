# Aagaaz

**Aagaaz** is an engaging platform created by **Rishabh Sahil** to fuel your passion for math and puzzles! Enjoy challenging Sudoku puzzles and brain-teasing Mathemania quizzes, designed for all skill levels. Built with Flask, Python, and a modern, responsive UI, Aagaaz is perfect for sharpening your mind while having fun.

## About Aagaaz

Aagaaz, developed by Rishabh Sahil, is a web application featuring two core games: a **Sudoku Solver & Checker** and **Mathemania Quizzes**. With a sleek dark-mode interface, it offers an interactive experience for puzzle enthusiasts and math lovers, powered by Flask and Python.

## Features

- **Sudoku Solver & Checker**: Generate puzzles (Easy, Medium, Hard), solve them instantly, or check your answers with real-time feedback.
- **Mathemania Quizzes**: Test your skills with 10-question sets in arithmetic, algebra, geometry, logic, and reasoning.
- **Progress Tracking**: View your game history and stats for both Sudoku and Mathemania.
- **Responsive Design**: Seamless, animated UI for mobile and desktop devices.
- **Open Source**: Licensed under the [MIT License](LICENSE), welcoming contributions.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/axinyyyx/aagaaz.git
   cd aagaaz
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python index.py
   ```

5. Open `http://localhost:5000` in your browser to start playing!

## Requirements

- Python 3.8+
- Flask
- Dependencies listed in `requirements.txt`

## Deployment

To deploy Aagaaz on Vercel:
1. Push your repository to GitHub.
2. Create a `vercel.json` file in the root directory:
   ```json
   {
       "version": 2,
       "builds": [
           {
               "src": "index.py",
               "use": "@vercel/python"
           }
       ],
       "routes": [
           {
               "src": "/(.*)",
               "dest": "index.py"
           }
       ]
   }
   ```
3. Deploy using the Vercel CLI or GitHub integration:
   ```bash
   vercel
   ```

## About the Developer

I'm **Rishabh Sahil**, a passionate coder and puzzle enthusiast from India. Aagaaz is my creation to share my love for math and logic with the world. When I'm not coding, I'm exploring new tech or crafting brain teasers. Connect with me:

- [GitHub](https://github.com/axinyyyx)
- [Instagram](https://www.instagram.com/rishabhsahill)
- [Facebook](https://www.facebook.com/rishabhsahill)
- [X](https://x.com/rishabhsahill)

## Contributing

Contributions are welcome! Fork the repository, submit issues, or create pull requests to enhance Aagaaz.

## License

This project is licensed under the [MIT License](LICENSE).

---

Built with 💻 by Rishabh Sahil
