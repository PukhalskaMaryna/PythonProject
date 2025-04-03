with open('C:/Users/puhal/Desktop/adventofcode/2.txt', 'r') as file:
    content = {
        # цикл наповнення словника словників
        int(i.split(":")[0].replace("Game ","")):i.split(":")[-1].strip() for i in file.read().splitlines()
    }

content = {game_id:
               {round_id:
                    {color.strip().split(" ")[-1]:int(color.strip().split(" ")[0])
                     for color in content.get(game_id).split(";")[round_id].strip().split(",")}
                for round_id in range(0,len(content.get(game_id).split(";")))}
           for game_id in content}

dic = {'red' : 12, 'green' : 13, 'blue' : 14}
exception = set()

for game_id,rounds in content.items():
    for round_id in rounds:
        # прогін через any за кольорами, чи є такий, к-ть якого вище за можливу
        if any(content.get(game_id).get(round_id).get(color, 0) > cnt for color,cnt in dic.items()):
            exception.add(game_id)
            break

print(sum(i for i in content.keys() if i not in exception))
