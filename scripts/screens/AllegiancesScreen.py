import pygame
import pygame_gui

from scripts.cat.cats import Cat
from scripts.game_structure.game_essentials import game, screen_x, screen_y, MANAGER
from scripts.game_structure.ui_elements import (
    UISpriteButton,
    UIImageButton,
    UITextBoxTweaked, 
    AllegiancesCat
)
from scripts.utility import (
    get_text_box_theme, 
    get_button_theme,
    scale,
    get_alive_status_cats,
    shorten_text_to_fit,
    get_alive_clan_queens,
)
from .Screens import Screens
from ..conditions import get_amount_cat_for_one_medic, medical_cats_condition_fulfilled


class AllegiancesScreen(Screens):
    allegiance_list = []

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element in self.names_buttons:
                game.switches["cat"] = event.ui_element.return_cat_id()
                self.change_screen('profile screen')
            else:
                self.menu_button_pressed(event)
                self.mute_button_pressed(event)


    def on_use(self):
        pass

    def screen_switches(self):
        # Heading
        self.heading = pygame_gui.elements.UITextBox(
            f"{game.clan.name}Clan Allegiances",
            scale(pygame.Rect((390, 230), (800, 80))),
            object_id=get_text_box_theme("#text_box_34_horizcenter"),
            manager=MANAGER,
        )

        # Set Menu Buttons.
        self.show_menu_buttons()
        self.show_mute_buttons()
        self.set_disabled_menu_buttons(["allegiances"])
        self.update_heading_text(f"{game.clan.name}Clan")
        allegiance_list = self.get_allegiances_text()

        self.scroll_container = pygame_gui.elements.UIScrollingContainer(
            scale(pygame.Rect((100, 330), (1430, 1000))),
            allow_scroll_x=False,
            manager=MANAGER,
        )

        self.ranks_boxes = []
        self.names_boxes = []
        self.names_buttons = []
        y_pos = 0
        for x in allegiance_list:
            #print(x)
            if(x[0] != ""):
                self.ranks_boxes.append(pygame_gui.elements.UITextBox(x[0],
                                   scale(pygame.Rect((0, y_pos), (300, -1))),
                                   object_id=get_text_box_theme("#text_box_30_horizleft"),
                                   container=self.scroll_container, manager=MANAGER))
                self.ranks_boxes[-1].disable()
            offset = 10
            x_pos = 290
            if game.settings["fullscreen"]:
                offset = screen_y / 225
                x_pos = 293
            self.names_buttons.append(AllegiancesCat(scale(pygame.Rect((x_pos, y_pos+offset), (1060, -1))),
                                    x[1],
                                    object_id=get_button_theme(),
                                    container=self.scroll_container, manager=MANAGER))
            self.names_buttons[-1].set_cat_id(x[2])
            self.names_boxes.append(pygame_gui.elements.UITextBox(x[3],
                                scale(pygame.Rect((300, y_pos), (1060, -1))),
                                object_id=get_text_box_theme("#text_box_30_horizleft"),
                                container=self.scroll_container, manager=MANAGER))
            self.names_boxes[-1].disable()
            
            #self.names_boxes[-1].process_event(pygame_gui.UI_ELEMENT_PRESSED)
            
            y_pos += 1400 * self.names_boxes[-1].get_relative_rect()[3] / screen_y

        self.scroll_container.set_scrollable_area_dimensions(
            (1360 / 1600 * screen_x, y_pos / 1400 * screen_y)
        )

    def exit_screen(self):
        for x in self.ranks_boxes:
            x.kill()
        del self.ranks_boxes
        for x in self.names_boxes:
            x.kill()
        del self.names_boxes
        for x in self.names_buttons:
            x.kill()
        del self.names_buttons
        self.scroll_container.kill()
        del self.scroll_container
        self.heading.kill()
        del self.heading
            
    def generate_one_entry(self, cat, extra_details=""):
        """Extra Details will be placed after the cat description, but before the apprentice (if they have one. )"""
        output = f"{str(cat.name).upper()} - {cat.describe_cat()} {extra_details}"

        if len(cat.apprentice) > 0:
            if len(cat.apprentice) == 1:
                output += "\n      APPRENTICE: "
            else:
                output += "\n      APPRENTICES: "
            output += ", ".join(
                [
                    str(Cat.fetch_cat(i).name).upper()
                    for i in cat.apprentice
                    if Cat.fetch_cat(i)
                ]
            )

        return [str(cat.name).upper(), cat.ID, output]

    def get_allegiances_text(self):
        """Determine Text. Ouputs list of tuples."""

        living_cats = [i for i in Cat.all_cats.values() if not (i.dead or i.outside)]
        living_meds = []
        living_mediators = []
        living_warriors = []
        living_apprentices = []
        living_kits = []
        living_elders = []
        for cat in living_cats:
            if cat.status == "healer":
                living_meds.append(cat)
            elif cat.status == "warrior":
                living_warriors.append(cat)
            elif cat.status == "mediator":
                living_mediators.append(cat)
            elif cat.status in ["apprentice", "healer apprentice", "mediator apprentice"]:
                living_apprentices.append(cat)
            elif cat.status in ["kitten", "newborn"]:
                living_kits.append(cat)
            elif cat.status == "elder":
                living_elders.append(cat)
        if not len(living_meds):
            for cat in living_apprentices:
                if cat.status == "healer apprentice":
                    living_meds.append(cat)
                    living_apprentices.remove(cat)
        if not len(living_mediators):
            for cat in living_apprentices:
                if cat.status == "mediator apprentice":
                    living_mediators.append(cat)
                    living_apprentices.remove(cat)


        living_meds = sorted(living_meds, key=lambda x: x.moons, reverse=True)
        living_mediators = sorted(living_mediators, key=lambda x: x.moons, reverse=True)
        living_warriors = sorted(living_warriors, key=lambda x: x.moons, reverse=True)
        living_apprentices = sorted(living_apprentices, key=lambda x: x.moons, reverse=True)
        living_kits = sorted(living_kits, key=lambda x: x.moons, reverse=True)
        living_elders = sorted(living_elders, key=lambda x: x.moons, reverse=True)

        # Find Queens:
        queen_dict, living_kits = get_alive_clan_queens(living_cats)

        # Remove queens from warrior or elder lists, if they are there.  Let them stay on any other lists.
        for q in queen_dict:
            queen = Cat.fetch_cat(q)
            if not queen:
                continue
            if queen in living_warriors:
                living_warriors.remove(queen)
            elif queen in living_elders:
                living_elders.remove(queen)

        # Clan Leader Box:
        # Pull the Clan leaders
        outputs = []
        if game.clan.leader and not (game.clan.leader.dead or game.clan.leader.outside):
                x = self.generate_one_entry(game.clan.leader)
                outputs.append([
                    '<b><u>LEADER</u></b>',
                    x[0],
                    x[1],
                    x[2]
                ])

        # Deputy Box:
        if game.clan.deputy and not (game.clan.deputy.dead or game.clan.deputy.outside):
            x = self.generate_one_entry(game.clan.deputy)
            outputs.append([
                '<b><u>DEPUTY</u></b>',
                x[0],
                x[1],
                x[2]
            ])

        # Healer Box:
        if living_meds:
            if len(living_meds) == 1:
                _box = ["", "", "", ""]
                _box[0] = '<b><u>HEALER</u></b>'
                x = self.generate_one_entry(living_meds[0])
                _box[1] = x[0]
                _box[2] = x[1]
                _box[3] = x[2]
                outputs.append(_box)
            else:
                for i in range(len(living_meds)):    
                    _box = ["", "", "", ""]
                    if i == 0:    
                        _box[0] = '<b><u>HEALERS</u></b>'
                    else:
                        _box[0] = ""
                    x = self.generate_one_entry(living_meds[i])
                    _box[1] = x[0]
                    _box[2] = x[1]
                    _box[3] = x[2]
            
            #_box[1] = "\n".join([self.generate_one_entry(i) for i in living_meds])
                    outputs.append(_box)
        
        # Mediator Box:
        if living_mediators:
            if len(living_mediators) == 1:
                _box = ["", "", "", ""]
                _box[0] = '<b><u>MEDIATOR</u></b>'
                x = self.generate_one_entry(living_mediators[0])
                _box[1] = x[0]
                _box[2] = x[1]
                _box[3] = x[2]
                outputs.append(_box)
            else:
                for i in range(len(living_mediators)): 
                    _box = ["", "", "", ""]   
                    if i == 0:    
                        _box[0] = '<b><u>MEDIATORS</u></b>'
                    else:
                        _box[0] = ""
                    x = self.generate_one_entry(living_mediators[i])
                    _box[1] = x[0]
                    _box[2] = x[1]
                    _box[3] = x[2]
            
            #_box[1] = "\n".join([self.generate_one_entry(i) for i in living_mediators])
                    outputs.append(_box)

        # Warrior Box:
        if living_warriors:
            if len(living_warriors) == 1:
                box = ["", "", "", ""]
                box[0] = '<b><u>WARRIOR</u></b>'
                x = self.generate_one_entry(living_warriors[0])
                box[1] = x[0]
                box[2] = x[1]
                box[3] = x[2]
                outputs.append(box)
            else:
                for i in range(len(living_warriors)):   
                    box = ["", "", "", ""]
                    if i == 0:    
                        box[0] = '<b><u>WARRIORS</u></b>'
                    else:
                        box[0] = ""
                    x = self.generate_one_entry(living_warriors[i])
                    box[1] = x[0]
                    box[2] = x[1]
                    box[3] = x[2]
                    outputs.append(box)
         # Apprentice Box:
        if living_apprentices:
            if len(living_apprentices) == 1:
                _box = ["", "", "", ""]
                _box[0] = '<b><u>APPRENTICE</u></b>'
                x = self.generate_one_entry(living_apprentices[0])
                _box[1] = x[0]
                _box[2] = x[1]
                _box[3] = x[2]
                outputs.append(_box)
            else:
                for i in range(len(living_apprentices)):   
                    _box = ["", "", "", ""] 
                    if i == 0:    
                        _box[0] = '<b><u>APPRENTICES</u></b>'
                    else:
                        _box[0] = ""
                    x = self.generate_one_entry(living_apprentices[i])
                    _box[1] = x[0]
                    _box[2] = x[1]
                    _box[3] = x[2]
                    outputs.append(_box)
        
         # Queens and Kits Box:
        if queen_dict or living_kits:
            
            # This one is a bit different.  First all the queens, and the kits they are caring for. 
            all_entries = []
            for q in queen_dict:
                queen = Cat.fetch_cat(q)
                if not queen:
                    continue
                kittens = []
                for k in queen_dict[q]:
                    kittens += [f"{k.name} - {k.describe_cat(short=True)}"]
                if len(kittens) == 1:
                    kittens = f" <i>(caring for {kittens[0]})</i>"
                else:
                    kittens = f" <i>(caring for {', '.join(kittens[:-1])}, and {kittens[-1]})</i>"

                all_entries.append(self.generate_one_entry(queen, kittens))

            # Now kittens without carers
            for k in living_kits:
                all_entries.append([str(k.name).upper(), k.ID, f"{str(k.name).upper()} - {k.describe_cat(short=True)}"])
            
            if all_entries:
                for i in range(len(all_entries)):
                    _box = ["", "", "", ""]
                    if i == 0:
                        _box[0] = '<b><u>QUEENS AND KITS</u></b>'
                    else:
                        _box[0] = ''
                    
                    _box[1] = all_entries[i][0]
                    _box[2] = all_entries[i][1]
                    _box[3] = all_entries[i][2]
                    outputs.append(_box)

        # Elder Box:
        if living_elders:
            if len(living_elders) == 1:
                _box = ["", "", "", ""]
                _box[0] = '<b><u>ELDER</u></b>'
                x = self.generate_one_entry(living_elders[0])
                _box[1] = x[0]
                _box[2] = x[1]
                _box[3] = x[2]
                outputs.append(_box)
            else:
                for i in range(len(living_elders)):    
                    _box = ["", "", "", ""]
                    if i == 0:    
                        _box[0] = '<b><u>ELDERS</u></b>'
                    else:
                        _box[0] = ""
                    x = self.generate_one_entry(living_elders[i])
                    _box[1] = x[0]
                    _box[2] = x[1]
                    _box[3] = x[2]
                    outputs.append(_box)

        return outputs
