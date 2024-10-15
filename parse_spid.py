from enum import StrEnum
import re

class FormType(StrEnum):
	SPELL = "Spell"
	PERK = "Perk"
	ITEM = "Item"
	SHOUT = "Shout"
	PACKAGE = "Package"
	KEYWORD = "Keyword"
	OUTFIT = "Outfit"
	SLEEP_OUTFIT = "SleepOutfit"
	FACTION = "Faction"
	SKIN = "Skin"

class TraitFilters(StrEnum):
	FEMALE = "F"
	MALE = "M"
	UNIQUE = "U"
	SUMMONABLE = "S"
	CHILD = "C"
	LEVELED = "L"
	TEAMMATE = "T"


class Form:
	def __init__(self, form_type, formid, string_filters=None, form_filters=None, level_filters=None, trait_filters=None, count=None, chance=None):
		self.form_type = form_type
		self.formid = formid
		self.string_filters = string_filters
		self.form_filters = form_filters
		self.level_filters = level_filters
		self.trait_filters = trait_filters
		self.count = count
		self.chance = chance

def parse_distr(filename)->list[Form]:
	if not filename.endswith("_DISTR.ini"):
		return []
	
	form_pattern = re.compile(r"(Spell|Perk|Item|Shout|Package|Keyword|Outfit|SleepOutfit|Faction|Skin)"
	+ r"([^\S\r\n]*)=([^\S\r\n]*)([a-zA-Z0-9~.]+)((\|([a-zA-Z0-9,/\-\+]|(\([0-9]+/[0-9]+\)))*)*)")
	#form_pattern = re.compile(r"([a-zA-Z]+)([^\S\r\n]*)=([^\S\r\n]*)([a-zA-Z0-9~.]+)((\|[a-zA-Z0-9,]*)*)")
	forms = []
	with open(filename) as distr_file:
		for line in distr_file:
			if line.startswith(";"):
				continue

			parse_form = re.match(form_pattern, line)
			if parse_form:
				form_type = parse_form.group(0).partition("=")[0].strip()
				filters = parse_form.group(0).partition("=")[2].split("|")
				if form_type not in FormType:
					print("Warning: Invalid form type: " + form_type)
				#filters = filters.split("|")
				formid = filters[0].strip()
				string_filters = None
				form_filters = None
				level_filters = None
				trait_filters= None
				count = None
				chance = None
				try:
					string_filters = filters[1].split(',')
					form_filters = filters[2].split(',')
					level_filters = filters[3]
					trait_filters = filters[4]
					count = filters[5]
					chance = filters[6]
				except IndexError:
					print("Reached end of filter list")
				
				form = Form(form_type, formid, string_filters, form_filters, level_filters, trait_filters, count, chance)
				forms.append(form)
	return forms

if __name__=="__main__":
	parsed_distr = parse_distr("./BladeAndBlunt_DISTR.ini")
	print("___________________________")
	with open("./output.txt", "w") as output_file:
		for form in parsed_distr:
			output_file.write(f"{form.form_type} = {form.formid}")
			if form.string_filters:
				output_file.write(f"|{','.join(form.string_filters)}")
			if form.form_filters:
				output_file.write(f"|{','.join(form.form_filters)}")
			if form.level_filters:
				output_file.write(f"|{form.level_filters}")
			if form.trait_filters:
				output_file.write(f"|{form.trait_filters}")
			if form.count:
				output_file.write(f"{form.count}")
			if form.chance:
				output_file.write(f"{form.chance}")
			output_file.write("\n")
			print("Distributed Form")
			print(f"\tType: {form.form_type}")
			print(f"\tForm or Editor ID: {form.formid}")
			print(f"\tString Filters: {form.string_filters}")
			print(f"\tForm Filters: {form.form_filters}")
			print(f"\tLevel Filters: {form.level_filters}")
			print(f"\tTrait Filters: {form.trait_filters}")
			print(f"\tCount or Package Index: {form.count}")
			print(f"\tChance: {form.chance}")
			print()
