import csv
from PIL import Image, ImageDraw, ImageFont
import uuid

class Card:
    def __init__(self, questions, responses):
        self.id = uuid.uuid4()
        self.questions = questions
        self.responses = responses

    def __repr__(self):
        return f"Card(id={self.id}, questions={self.questions}, responses={self.responses})"

    def draw_card(self):
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
        draw_q.rounded_rectangle([10, 10, width - 10, height - 10], 10, fill=None, outline="black", width=3)
        draw_r.rounded_rectangle([10, 10, width - 10, height - 10], 10, fill=None, outline="black", width=3)

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
        im = get_concat_h(image_q, image_r)
        # Save the image
        im.save("card.png")
        # Show the image
        im.show()


csv_file = "QR.csv"
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')

    # Skip the header row
    next(reader)

    # Read the CSV file and store the themes, questions, and responses in lists
    themes = []
    questions = []
    responses = []
    for row in reader:
        themes.append(row[0])
        questions.append(row[1])
        responses.append(row[2])
    # Create a dictionary to store the questions and responses for each theme
    theme_dict = {}
    for i in range(len(themes)):
        if themes[i] not in theme_dict:
            theme_dict[themes[i]] = {"questions": [], "responses": []}
        theme_dict[themes[i]]["questions"].append(questions[i])
        theme_dict[themes[i]]["responses"].append(responses[i])
    print(theme_dict)

card = Card(questions, responses)
print(card)
card.draw_card()