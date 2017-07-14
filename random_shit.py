import random

time = random.randint(0,24)
zip = random.randint(20101, 26886)
file = open("things.csv",'w')
new = open("schools.txt",'r')

schools = []

for item in new:
    schools.append(item.split(",")[0])

for i in range(2000):
    school = random.choice(schools)
    zip = random.randint(20101, 26886)
    time = random.randint(10, 19)

    players = random.choice(range(6, 12, 2))
    game = random.choice(["Soccer","Basketball","Football","Tennis"])
    half = random.randint(0,1)
    half *=30
    padded = str(half).zfill(2)
    prev = time
    if(time >= 12):
        cool = " PM"
        time %=12
        if time == 0:
            time = 12
    else:
        cool = " AM"


    string = str(time) + ":" + padded + cool
    print(string,zip,players,game)
    file.write(school + "," +game + "," + str(players) + "," + string + "," + str(zip) + "\n")

