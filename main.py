import scripts.rule_sheet
import scripts.idioms

scripts.rule_sheet.create_rule_sheet(json_file_path="game_settings.json", output_file_path="pdf_files/Interpret_That_Idiom_Rule_Sheet.pdf")
scripts.idioms.create_idioms(json_file_path="idioms.json", output_file_path="pdf_files/Interpret_That_Idiom_Cards.pdf")

print("Check the pdf_files folder for the rule sheet and idiom cards.")