class KitchenEnvironment:
    def __init__(self):
        self.state = {
            "fridge_open": False,
            "milk_grabbed": False,
            "bread_grabbed": False,
            "toaster_on": False,
            "plate_out": False,
            "butter_grabbed": False,
            "kettle_on": False,
            "cup_out": False,
        }

    def reset(self):
        for key in self.state:
            self.state[key] = False

    def act(self, action: str) -> tuple[str, bool]:
        if action == "open_fridge":
            self.state["fridge_open"] = True
            return "Fridge is now open.", True

        elif action == "grab_milk":
            if self.state["fridge_open"]:
                self.state["milk_grabbed"] = True
                return "Grabbed the milk from the fridge.", True
            else:
                return "Can't grab milk — fridge is closed.", False

        elif action == "grab_bread":
            self.state["bread_grabbed"] = True
            return "Grabbed the bread from the counter.", True

        elif action == "turn_on_toaster":
            if self.state["bread_grabbed"]:
                self.state["toaster_on"] = True
                return "Toaster is on and bread is toasting.", True
            else:
                return "No bread to toast.", False

        elif action == "get_plate":
            self.state["plate_out"] = True
            return "Got a plate out.", True

        elif action == "grab_butter":
            if self.state["fridge_open"]:
                self.state["butter_grabbed"] = True
                return "Grabbed the butter from the fridge.", True
            else:
                return "Can't grab butter — fridge is closed.", False

        elif action == "turn_on_kettle":
            self.state["kettle_on"] = True
            return "Kettle is now boiling.", True

        elif action == "get_cup":
            self.state["cup_out"] = True
            return "Got a cup out.", True

        else:
            return f"Unknown action: {action}", False