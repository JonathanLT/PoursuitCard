import os
import csv
import hashlib
from PIL import Image, ImageDraw, ImageFont

class Card:
    def __init__(self, id: int, questions: list, responses: list):
        self.questions = questions
        self.responses = responses
        self.hash = self.__hash_card__()
        self.id = id
        self.image = None

    def __repr__(self):
        return f"Card(id={self.id}, hash={self.hash})"

    def __hash_card__(self):
        hs = hashlib.sha1(",".join(self.questions+self.responses).encode()).hexdigest()
        return hs

    def create_card(self):
        # Function to create a gradient image
        def gradient(size, start, stop):
            im = Image.new("RGB", size)
            for x in range(im.width):
                progress = x / (im.width - 1)
                color = tuple(int(start[i] * (1 - progress) + stop[i] * progress) for i in range(3))
                for y in range(im.height):
                    im.putpixel((x, y), color)
            return im

        # Function to concatenate two images horizontally
        def get_concat_h(im1, im2):
            dst = Image.new('RGB', (im1.width + im2.width, im1.height))
            dst.paste(im1, (0, 0))
            dst.paste(im2, (im1.width, 0))
            return dst

        # Card dimensions
        width, height = 400, 250

        # Create two images for questions and responses
        image_q = gradient((width, height), (150, 255, 217), (255, 153, 204))
        image_r = gradient((width, height), (150, 255, 217), (255, 153, 204))

        # Draw on the images
        draw_q = ImageDraw.Draw(image_q)
        draw_r = ImageDraw.Draw(image_r)
        # Add rounded rectangles
        draw_q.rounded_rectangle([5, 5, width - 5, height - 5], 10, fill=None, outline="black", width=1)
        draw_r.rounded_rectangle([5, 5, width - 5, height - 5], 10, fill=None, outline="black", width=1)

        # Define colors for the cards
        COLORS = {
            "pink": (255, 192, 203),
            "yellow": (255, 251, 0),
            "orange": (255, 165, 0),
            "green": (0, 128, 0),
            "blue": (0, 0, 255),
            "purple": (128, 0, 128),
        }

        # Add titles to the questions card
        text = "Questions"
        font_size = 25
        font = ImageFont.truetype("Arial Unicode.ttf", font_size)
        draw_q.text((width/2 - 60, 5), text, fill="black", font=font)
        # Add titles to the responses card
        text = "Réponses"
        font_size = 25
        font = ImageFont.truetype("Arial Unicode.ttf", font_size)
        draw_r.text((width/2 - 60, 5), text, fill="black", font=font)

        # Add the ID to the questions card
        text = f"ID: {self.id}"
        font_size = 10
        font = ImageFont.truetype("Arial Unicode.ttf", font_size)
        draw_q.text((width-50, height-20), text, fill="gray", font=font)
        draw_r.text((width-50, height-20), text, fill="gray", font=font)

        for i, color in enumerate(COLORS.values()):
            # Add triangles to the question line
            draw_q.polygon([(20, 45 + (i * 33)), (30, 50 + (i * 33)), (30, 40 + (i * 33))], fill=color)
            # Add text for the question
            text = self.questions[i]
            font_size = 10
            font = ImageFont.truetype("Arial Unicode.ttf", font_size)

            # Calculate the width of the text
            words = text.split()
            length = 0
            for word in words:
                length += len(word)
                # If the text is too long, split it into two lines
                if length > 60:
                    text = " ".join(words[:words.index(word)]) + "\n" + " ".join(words[words.index(word):])
                    break
            draw_q.multiline_text((40, 40 + (i * 33)), text, font=font, fill="black", spacing=1, align="left")

        for i, color in enumerate(COLORS.values()):
            # Add triangles to the question line
            draw_r.polygon([(20, 45 + (i * 33)), (30, 50 + (i * 33)), (30, 40 + (i * 33))], fill=color)
            # Add text for the question
            text = self.responses[i]
            font_size = 10
            font = ImageFont.truetype("Arial Unicode.ttf", font_size)

            # Calculate the width of the text
            words = text.split()
            length = 0
            for word in words:
                length += len(word)
                # If the text is too long, split it into two lines
                if length > 60:
                    text = " ".join(words[:words.index(word)]) + "\n" + " ".join(words[words.index(word):])
                    break
            draw_r.multiline_text((40, 40 + (i * 33)), text, font=font, fill="black", spacing=1, align="left")

        # Merge the two images horizontally
        self.image = get_concat_h(image_q, image_r)

    def save_card(self, path=None):
        # If no path is provided, save in the current directory
        if path is None:
            path = "."
        # Save the card image
        self.image.save(os.path.join(path, f"card_{self.id}.png"))

    def display_card(self):
        # Display the card image
        self.image.show()


if __name__ == "__main__":
    csv_file = "QR.csv"
    nb_questions = 0
    theme_dict = {}

    # Read the CSV file
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')

        # Skip the header row
        next(reader)
        themes = []
        questions = []
        responses = []

        # Read the CSV file and store the themes, questions, and responses in lists
        for row in reader:
            themes.append(row[0])
            questions.append(row[1])
            responses.append(row[2])
        # Create a dictionary to store the questions and responses for each theme
        nb_questions = len(questions)
        for i in range(len(themes)):
            if themes[i] not in theme_dict:
                theme_dict[themes[i]] = {"questions": [], "responses": []}
            theme_dict[themes[i]]["questions"].append(questions[i])
            theme_dict[themes[i]]["responses"].append(responses[i])

    card_id = 0
    while nb_questions > 0:
        card_id += 1
        # Create a card for each theme
        card_questions = []
        card_responses = []
        for theme in theme_dict.keys():
            # Pop a question and response from the theme
            questions = theme_dict[theme]["questions"]
            responses = theme_dict[theme]["responses"]
            if questions and responses:
                card_questions.append(questions.pop())
                card_responses.append(responses.pop())
                nb_questions -= 1
        # Create a card object
        card = Card(card_id, card_questions, card_responses)
        card.create_card()
        card.save_card("./output")
        print(f"Card created: {card}")
