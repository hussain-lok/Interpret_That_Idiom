from fpdf import FPDF
from pathlib import Path
import json

# Create a new PDF for the rule sheet
class RuleSheetPDF(FPDF):
    def header(self):
        # Title header with color
        self.set_font("Helvetica", "B", 20)
        self.set_text_color(0, 102, 204)  # Deep blue
        self.cell(0, 12, "Interpret That Idiom! Rule Sheet", ln=True, align="C")
        self.ln(4)
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, "A game of nonsense, creativity, and wildly incorrect guesses.", ln=False, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section(self, title, body):
        self.set_text_color(0, 51, 102)
        self.set_font("Helvetica", "B", 14)
        self.multi_cell(0, 8, f"\n{title}")
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, body)
        self.ln(2)


def create_rule_sheet(json_file_path, output_file_path):
    json_path = Path(json_file_path)
    with open(json_path, "r") as f:
        game_settings = json.load(f)

    points_to_win = game_settings["points_to_win"]
    round_time_in_minutes = game_settings["round_time_in_minutes"]
    time_to_guess_definition_in_seconds = game_settings["time_to_guess_definition_in_seconds"]
    lightning_round_starting_points = game_settings["lightning_round"]["starting_points"]
    lightning_round_time_in_minutes = game_settings["lightning_round"]["round_time_in_minutes"]
    bonus_categories = game_settings["bonus_categories"]
    bonus_categories_total_points = sum(category["points"] for category in bonus_categories) + game_settings["bonus_points_for_winning_all_categories"]

    bonus_points = "".join([f"- {category['name']}: {category['points']} bonus point\n" for category in bonus_categories])

    # Create PDF
    pdf = RuleSheetPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Sections
    pdf.add_section("Goal",
        f"Be the first player to reach {points_to_win} points by creating the most convincing and creative phrases " +
        f"and definitions using absurd idioms.")

    pdf.add_section("Setup",
        "- Each round, every player receives a different idiom.\n" +
        f"- Set a timer for {round_time_in_minutes} minutes.\n" +
        "- Each player must write:\n" +
        "  - 2-3 example phrases using their idiom in context.\n" +
        "  - 1 definition or interpretation of what they believe their idiom means.")
    pdf.set_font("Helvetica", "BI", 12)
    pdf.cell(0, 8, "Tip: Don't overthink it - sometimes flying by the seat of your pants works best!", ln=True)
    pdf.set_font("Helvetica", "", 12)

    pdf.add_section("Round Process",
        "1. Presentation:\n   Each player shares their phrases and interpretation.\n" +
        f"2. Test Your Skills:\n   All other players have {time_to_guess_definition_in_seconds} seconds to write down what they think the idiom means.\n" +
        "3. Scoring:\n" +
        "   - The Phrasemaker (player who shared the idiom) earns 1 point for each player who guesses their intended definition.\n" +
        "   - Players who correctly guess The Phrasemaker's definition earn 1 point each.")

    pdf.add_section("Lightning Rounds",
        f"When any player reaches {lightning_round_starting_points} points, enter Lightning Mode:\n" +
        f"- Only {lightning_round_time_in_minutes} minute to write phrases and interpretations.")
    pdf.set_font("Helvetica", "I", 12)
    pdf.multi_cell(0, 8, "Time flies when you're having fun! Don't blink or you'll miss it!\n\n\n\n")
    pdf.set_font("Helvetica", "", 12)

    pdf.add_section("Bonus Scoring", bonus_points)
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 8, "- You cannot vote for yourself - no tooting your own horn!", ln=True)
    pdf.set_font("Helvetica", "BI", 12)
    pdf.cell(0, 8, f"Double Trouble: Win all bonus categories? Earn {bonus_categories_total_points} bonus points total!", ln=True)
    pdf.set_font("Helvetica", "", 12)

    pdf.add_section("Winning the Game",
        f"The first player to reach {points_to_win} points wins!")

    # Output the file
    pdf.output(output_file_path)
