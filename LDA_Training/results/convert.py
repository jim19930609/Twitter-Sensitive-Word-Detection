import os

topic_list = []
with open("topics.txt", "rb") as f:
  for lines in f:
    lines = lines.strip()
    sp = lines.split(" ")
    topic_list.append(sp)

sensitive_set = set()
for filename in os.listdir("../sensitive_words"):
  with open("../sensitive_words/" + filename, "rb") as f:
    for line in f:
      line = line.strip().decode('ascii', 'ignore').encode('utf-8', 'ignore')
      sensitive_set.add(line)

with open("topic_levels.txt", "a") as f:
  index = 0
  for topic in topic_list:
    counts = 0
    for words in topic:
      if words in sensitive_set:
        counts += 1
    # Threshold for LDA Levels
    if counts >= 2:
      f.write(str(index) + " " + "red")
    elif counts < 2 and counts >= 1:
      f.write(str(index) + " " + "yellow")
    else:
      f.write(str(index) + " " + "green")
    index += 1
    f.write("\n")

