import datetime
class SRSEngine:
    def __init__(self):
        self.cards = {}

    def add_card(self, cid, data):
        self.cards[cid] = {
            "data": data,
            "ef": 2.5,
            "interval": 1,
            "last_review": None,
            "due": datetime.date.today()
        }

    def review(self, cid, quality):
        c = self.cards[cid]
        if quality < 3:
            c["interval"] = 1
        else:
            c["ef"] = max(1.3, c["ef"] + 0.1 - (5-quality)*(0.08+(5-quality)*0.02))
            if c["last_review"] is None:
                c["interval"] = 1
            else:
                c["interval"] = int(c["interval"] * c["ef"])
        c["last_review"] = datetime.date.today()
        c["due"] = datetime.date.today() + datetime.timedelta(days=c["interval"])
        return c["due"]

    def get_due_cards(self):
        today = datetime.date.today()
        return {cid:v for cid,v in self.cards.items() if v["due"] <= today}