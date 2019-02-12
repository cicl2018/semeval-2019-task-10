import json

# extract question with tag "open" from file with different questions and write them to another file
def only_open_questions(input_file, output_file):
	with open(input_file) as file:
		questions = json.load(file)

	open_questions = []
	for question in questions:
		if question["tags"] == ["open"]:
			open_questions.append(question)

	with open(output_file, "w") as file:
		json.dump(open_questions, file, indent=4)

# extract questions with tag "open" from sat.train.json and write them to open.train.json
only_open_questions("./files/sat.test.json", "./files/open.test.json")