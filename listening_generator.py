import random
def sample():
    data=[
       ("At the Airport","A2","travel","Traveling by plane can be stressful, but planning helps. At the airport, passengers check in, go through security, and wait for boarding."),
       ("Working Remote","B1","work","Remote work allows flexibility and saves commute time. However, it also requires strong self‑discipline and clear online communication."),
       ("Scientific Discovery","C1","science","Breakthroughs in science often come from unexpected results. Modern discoveries rely heavily on data analysis and global collaboration.")
    ]
    return random.choice(data)