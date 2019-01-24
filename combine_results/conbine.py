import json

with open("sat.test.json", "r") as f:
    all_questions = json.load(f)

with open("xuefeng_0.json", "r") as f:
    xuefeng = json.load(f)

with open("alina_test.json", "r") as f:
    alina = json.load(f)

final_json = []

for data in all_questions:
    final = dict()
    final["id"] = data['id']

    xuefeng_ans = next((item for item in xuefeng if item["id"] == data['id']), False)

    if xuefeng_ans:
        final["answer"] = xuefeng_ans["answer"]
        # final["system"] = "xuefeng"
        final_json.append(final)
        continue

    alina_ans = next((item for item in alina if item["id"] == data['id']), False)

    if alina_ans:
        final["answer"] = alina_ans["answer"]
        #final["system"] = "alina"
        final_json.append(final)
        continue

    final["answer"] = "A"
   # final["system"] = "guess"
    final_json.append(final)

with open("final.json", "w+") as f:
    final_output = json.dumps(final_json, indent=4)
    f.write(final_output)
