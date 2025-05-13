# PoursuitCard

PoursuitCard is a Python-based project designed to generate visually appealing cards containing questions and responses. These cards are created from a CSV file and can be saved as images for use in quizzes, games, or educational purposes.

## Features

- Reads questions and responses from a CSV file.
- Generates cards with a gradient background and styled text.
- Supports themes for categorizing questions and responses.
- Saves the generated cards as PNG images.
- Displays the cards directly from the application.

## Requirements

- Python 3.x
- Required Python libraries:
  - `Pillow`
  - `csv`
  - `hashlib`
  - `os`

## How to Use

1. Prepare a CSV file named `QR.csv` with the following structure:
   ```
   Theme;Question;Response
   Theme1;What is Python?;A programming language
   Theme2;What is AI?;Artificial Intelligence
   ```

2. Run the script:
   ```bash
   python main.py
   ```

3. The generated cards will be saved in the `output` directory.

## Example Output

The cards will have a gradient background with questions on one side and responses on the other. Each card is uniquely identified by a hash ID.

## License

This project is open-source and available under the MIT License.

