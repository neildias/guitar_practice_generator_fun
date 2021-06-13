from tkinter import *
from time import sleep

root = Tk()

root.title("The Complete Music Practice Trainer. ")

practice_time = Entry(root, width=10, borderwidth=10)
tempo = Entry(root, width=10, borderwidth=10)


#e.pack()
practice_time.grid(row=0, column=5, columnspan=1, padx=10, pady=5)
tempo.grid(row=0, column=6, columnspan=1, padx=10, pady=5)


main_schedule_dict = {}
main_temp_sch_dict = {}
# this will be used to add practice head to practice schedule
# the last clicked practice header will populate this variable
# and the timer will then use this var to create the key: value pair
temp_practice_head_variable = ""


def click(what):
  try:

    if what == "time":
      time_input_button['state'] = 'disabled'
      prac_input = int(practice_time.get())
      # todo : write to a dictionary
      main_schedule_dict[temp_practice_head_variable] = prac_input

    else:
      tempo_input_button['state'] = 'disabled'
      prac_input = int(tempo.get())
      main_temp_sch_dict[temp_practice_head_variable] = prac_input

  except:
    pass

  if what=="time":
    practice_time.delete(0, END)
    practice_time.insert(0, "Enter 0-10")
  else:
    tempo.delete(0, END)
    tempo.insert(0, "Enter 0-10")

  print(main_schedule_dict)
  print(main_temp_sch_dict)



def reset_display():
  pass


def process_click(practice_head):
  # TODO: make tempo and timer active
  time_input_button['state'] = 'normal'
  tempo_input_button['state'] = 'normal'
  # TODO: capture practice head and timer in dict
  global temp_practice_head_variable
  temp_practice_head_variable = practice_head
  main_schedule_dict[practice_head] = 10       # default values
  main_temp_sch_dict[practice_head] = 60  # default values
  print(main_schedule_dict)
  print(main_temp_sch_dict)


def show_items():
  row_counter = 4
  label_counter = 0
  if main_schedule_dict:
    for practice_header, time in main_schedule_dict.items():
      print(practice_header, time )
      #temp_label = f"TEMP_LABEL_{label_counter}"
      c = Label(root, text= f"{practice_header} : {time} mins at "
                                     f"{main_temp_sch_dict[practice_header]} BPM")

      c.grid(row=row_counter, column=8, rowspan=1, columnspan=1, padx=10,
                           pady=5)
      row_counter+=2


def start_practicing():
  # TODO: run the dictionary created in the above function
  # TODO: and display timer
  pass


time_input_button = Button(root,
                           text="Enter Time",
                           padx=10, pady=5,
                           state=DISABLED,
                           command=lambda: click("time"))
# button_1 = Button(root, text="1", padx=40, pady=20,
#                   command=lambda: button_click(1))
time_input_button.grid(row=1, column=5, rowspan=1, columnspan=1, padx=10,
                       pady=5)

tempo_input_button = Button(root,
                            text="Enter Tempo",
                            padx=10, pady=5,
                            state=DISABLED,
                            command=lambda: click("tempo"))
tempo_input_button.grid(row=1, column=6, rowspan=1, columnspan=1, padx=10,
                       pady=5)

# countdown
practicing_head = Label(root, text="P R A C T I C I N G  T H I S")
practicing_head.grid(row=0, column=0, rowspan=2, columnspan=3, padx=10, pady=5)

countdown_timer = Label(root, text="C O U N T D O W N   T I M E R")
countdown_timer.grid(row=0, column=3, rowspan=2, columnspan=2, padx=10, pady=5)

status = Label(root, text="Show Practice Ite")
status.grid(row=0, column=8, rowspan=1, columnspan=2, padx=10, pady=5)
show_practice_items_bt = Button(root, height=1, text="Show Items",
                                  padx=12, pady=5, command=show_items)
show_practice_items_bt.grid(row=1, column=8, rowspan=1, columnspan=1, padx=5,
                                pady=3)
# button 9 rows and 7 columns
# Musical section
# # main heading
musical_section_label = Label(root, text="M  U  S  I C  A  L     M  "
                                           "A  S  T  E  R  Y     S  E  C  T  "
                                           "I  O  N")
musical_section_label.grid(row=3, column=0, rowspan=1, columnspan=7, padx=10,
                           pady=5)
# sub headings
# my_label_1 = Label(root, width=90, text="this is the first text")
# my_label_1 = Label(root, width=90, text="this is the first text")
# my_label_1 = Label(root, width=90, text="this is the first text")
# my_label_1 = Label(root, width=90, text="this is the first text")
cmd1 = "lambda: process_click('ear_training_interval')"
cmd2 = "lambda: process_click('ear_training_melody')"
cmd3 = "lambda: process_click('ear_training_harmony')"
cmd4 = "lambda: process_click('ear_training_play_ear')"

ear_training_interval_bt = Button(root, height=1, text="ET Interval",
                                  padx=12, pady=5,
                                  command=eval(cmd1))
ear_training_melody_bt = Button(root, height=1,text="ET Melody", padx=11,
                                pady=5, command=eval(cmd2))
ear_training_harmony_bt = Button(root, height=1,text="ET Harmony", padx=7,
                                 pady=5, command=eval(cmd3))
ear_training_play_ear_bt = Button(root, height=1,text="Play by Ear",
                                  padx=10, pady=5, command=eval(cmd4))

ear_training_interval_bt.grid(row=4, column=0, rowspan=1, columnspan=1, padx=5,
                                pady=3)
ear_training_melody_bt.grid(row=6, column=0, rowspan=1, columnspan=1,padx=5,
                                pady=3)
ear_training_harmony_bt.grid(row=8, column=0, rowspan=1, columnspan=1,padx=5,
                                pady=3)
ear_training_play_ear_bt.grid(row=10, column=0, rowspan=1, columnspan=1,padx=5,
                                pady=3)

# music theory button
music_theory_bt = Button(root, width=10, height=4, text="Music Theory",
                                                        padx=10, pady=5)
song_writing_bt = Button(root, width=10, height=4, text="Song Writing",
                                                        padx=10, pady=5)
music_theory_bt.grid(row=4, column=1, rowspan=4, columnspan=1, padx=5,
                                pady=5)
song_writing_bt.grid(row=8, column=1, rowspan=4, columnspan=1, padx=5,
                                pady=5)

# Improvisation buttons
improvising_bt = Button(root, width=10,height=4, text="Improvise", padx=10,
                        pady=5)
soloing_bt = Button(root, width=10,height=4, text="Soloing", padx=10, pady=5)
improvising_bt.grid(row=4, column=2, rowspan=4, columnspan=1, padx=5, pady=5)
soloing_bt.grid(row=8, column=2, rowspan=4, columnspan=1, padx=5, pady=5)

# songs
song_lead_bt = Button(root, width=10,height=4, text="Song Lead", padx=5,
                        pady=5)
song_rhythm_bt = Button(root, width=10,height=4, text="Song Rhythm", padx=5,
                       pady=5)
song_lead_bt.grid(row=4, column=3, rowspan=4, columnspan=1,padx=5, pady=5)
song_rhythm_bt.grid(row=8, column=3, rowspan=4, columnspan=1,padx=5, pady=5)


# scales
octave_scale_bt = Button(root, height=1, text="Octatonic Scale",
                                  padx=12, pady=5)
flamenco_scale_bt = Button(root, height=1,text="Flamenco Scale", padx=11,
                                pady=5)
pentatonic_scale_bt = Button(root, height=1,text="Pentatonic", padx=23,
                                 pady=5)
other_scale_bt = Button(root, height=1,text="Other Scale",
                                  padx=22, pady=5)

octave_scale_bt.grid(row=4, column=4, rowspan=1, columnspan=1, padx=10,
                                pady=3)
flamenco_scale_bt.grid(row=6, column=4, rowspan=1, columnspan=1,padx=10,
                                pady=3)
pentatonic_scale_bt.grid(row=8, column=4, rowspan=1, columnspan=1,padx=10,
                                pady=3)
other_scale_bt.grid(row=10, column=4, rowspan=1, columnspan=1,padx=10,
                                pady=3)

# chords

common_chords_bt = Button(root, height=1, text="Common Chords",
                                  padx=10, pady=10)
caged_chords_bt = Button(root, height=1,text="Caged Chords", padx=19,
                                pady=10)
special_chords_bt = Button(root, height=1,text="Special Chords", padx=18,
                                 pady=10)
chord_progression_bt = Button(root, height=1,text="Chord Progression",
                                  padx=10, pady=10)

common_chords_bt.grid(row=4, column=5, rowspan=1, columnspan=1,
                                pady=3)
caged_chords_bt.grid(row=6, column=5, rowspan=1, columnspan=1,
                                pady=3)
special_chords_bt.grid(row=8, column=5, rowspan=1, columnspan=1,
                                pady=3)
chord_progression_bt.grid(row=10, column=5, rowspan=1, columnspan=1,
                                pady=3)


# fretboard mastery

# chords

fretboard_tonic_bt = Button(root, height=1, text="fretboard_tonic",
                                  padx=10, pady=10)
fretboard_monic_bt = Button(root, height=1,text="fretboard_tonic", padx=10,
                                pady=10)
fretboard_bonic_bt = Button(root, height=1,text="fretboard_tonic", padx=10,
                                 pady=10)
fretboard_fonic_bt = Button(root, height=1,text="fretboard_tonic",
                                  padx=10, pady=10)

fretboard_tonic_bt.grid(row=4, column=6, rowspan=1, columnspan=1,
                                pady=3)
fretboard_monic_bt.grid(row=6, column=6, rowspan=1, columnspan=1,
                                pady=3)
fretboard_bonic_bt.grid(row=8, column=6, rowspan=1, columnspan=1,
                                pady=3)
fretboard_fonic_bt.grid(row=10, column=6, rowspan=1, columnspan=1,
                                pady=3)


technical_section_label = Label(root, text="T  E  C  H  N  I  C  A  L     M  "
                                           "A  S  T  E  R  Y     S  E  C  T  "
                                           "I  O  N", pady=10)
technical_section_label.grid(row=12, column=0, rowspan=1, columnspan=7, padx=10,
                           pady=10)

# col 1   creative
hammer_ons_bt = Button(root, height=1, text="Hammer On", pady=5)
pull_offs_bt = Button(root, height=1,text="Pull-off",padx=15,pady=5)
tapping_bt = Button(root, height=1,text="Tapping",padx=14,pady=5)
slides_bt = Button(root, height=1,text="Slides",padx=20,pady=5)
vibrato_bt = Button(root, height=1, text="Vibrato",padx=17,pady=5)
bends_bt = Button(root, height=1,text="Bending",padx=14,pady=5)
finger_slide_bt = Button(root, height=1,text="Finger Slide",padx=5,pady=5)

hammer_ons_bt.grid(row=13, column=0, rowspan=1, columnspan=1, padx=10,
                                pady=3)
pull_offs_bt.grid(row=15, column=0, rowspan=1, columnspan=1,padx=10,
                                pady=3)
tapping_bt.grid(row=17, column=0, rowspan=1, columnspan=1,padx=10,
                                pady=3)
slides_bt.grid(row=19, column=0, rowspan=1, columnspan=1,padx=10,
                                pady=3)
vibrato_bt.grid(row=21, column=0, rowspan=1, columnspan=1,padx=10,
                                pady=3)
bends_bt.grid(row=23, column=0, rowspan=1, columnspan=1,padx=10,
                                pady=3)
finger_slide_bt.grid(row=25, column=0, rowspan=1, columnspan=1,padx=10,
                                pady=3)


# # col2   electric
effects_bt = Button(root, height=1, text="Effects",
                                  padx=23, pady=5)
whammy_bar_bt = Button(root, height=1,text="WhammyBar", padx=7,
                                 pady=5)
pedals_bt = Button(root, height=1,text="Pedals",
                                  padx=25, pady=5)


effects_bt.grid(row=13, column=1, rowspan=1, columnspan=1, padx=5,
                                pady=3)

whammy_bar_bt.grid(row=17, column=1, rowspan=1, columnspan=1,padx=5,
                                pady=3)
pedals_bt.grid(row=19, column=1, rowspan=1, columnspan=1,padx=5,
                                pady=3)


# col 3   # melody
alternate_picking_bt = Button(root, height=1, text="Alt. Picking",
                                  padx=20, pady=5)
hybrid_picking_bt = Button(root, height=1,text="Hybrid Picking", padx=11,
                                pady=5)
sweep_picking_bt = Button(root, height=1,text="Sweep Picking", padx=13,
                                 pady=5)
finger_picking_bt = Button(root, height=1,text="Finger Picking",
                                  padx=13, pady=5)

pulgar_bt = Button(root, height=1,text="  Pulgar  ",
                                  padx=27, pady=5)
alpazua_bt = Button(root, height=1,text="  Alpazua  ",
                                  padx=24, pady=5)
string_skipping_bt = Button(root, height=1,text="String Skipping",
                                  padx=10, pady=5)

alternate_picking_bt.grid(row=13, column=2, rowspan=1, columnspan=1, padx=5,
                                pady=3)
hybrid_picking_bt.grid(row=15, column=2, rowspan=1, columnspan=1,padx=5,
                                pady=3)
sweep_picking_bt.grid(row=17, column=2, rowspan=1, columnspan=1,padx=5,
                                pady=3)
finger_picking_bt.grid(row=19, column=2, rowspan=1, columnspan=1,padx=5,
                                pady=3)
pulgar_bt.grid(row=21, column=2, rowspan=1, columnspan=1,padx=5,
                                pady=3)
alpazua_bt.grid(row=23, column=2, rowspan=1, columnspan=1,padx=5,
                                pady=3)
string_skipping_bt.grid(row=25, column=2, rowspan=1, columnspan=1,padx=5,
                                pady=3)

# col 4   # rhythm
rasgeo_bt = Button(root, height=1, text="Rasgeo",
                                  padx=25, pady=5)
rumba_bt = Button(root, height=1,text="Rumba", padx=25,
                                pady=5)
# other_bt = Button(root, height=1,text="Other", padx=7,
#                                  pady=5)
strumming_bt = Button(root, height=1,text="Strumming", padx=15,
                                 pady=5)
finger_arpeggio_bt = Button(root, height=1,text="Fin. Arpeggio",
                                  padx=11, pady=5)
pick_arpeggio_bt = Button(root, height=1,text="Pick Arpeggio",
                                  padx=10, pady=5)
# other3_bt = Button(root, height=1,text="Arpeggio",
#                                   padx=10, pady=5)

rasgeo_bt.grid(row=13, column=3, rowspan=1, columnspan=1, padx=5,
                                pady=3)
rumba_bt.grid(row=15, column=3, rowspan=1, columnspan=1,padx=5,
                                pady=3)
# other_bt.grid(row=17, column=3, rowspan=1, columnspan=1,padx=5,
#                                 pady=3)
strumming_bt.grid(row=19, column=3, rowspan=1, columnspan=1,padx=26,
                                pady=3)
finger_arpeggio_bt.grid(row=21, column=3, rowspan=1, columnspan=1,padx=10,
                                pady=3)
pick_arpeggio_bt.grid(row=23, column=3, rowspan=1, columnspan=1,padx=5,
                                pady=3)
# other3_bt.grid(row=25, column=3, rowspan=1, columnspan=1,padx=5,
#                                 pady=3)

# col 5 Percussion
string_mute_bt = Button(root, height=1, text="String Mute",
                                  padx=14, pady=5)
string_slap_bt = Button(root, height=1,text="String Slap", padx=18,
                                pady=5)
palm_beats_bt = Button(root, height=1,text="Palm Beats", padx=18,
                                 pady=5)
soundbox_tap_bt = Button(root, height=8,text="SoundBox Tap",
                                  padx=10, pady=5)

string_mute_bt.grid(row=13, column=4, rowspan=1, columnspan=1, padx=5,
                                pady=3)
string_slap_bt.grid(row=15, column=4, rowspan=1, columnspan=1,padx=5,
                                pady=3)
palm_beats_bt.grid(row=17, column=4, rowspan=1, columnspan=1,padx=5,
                                pady=3)
soundbox_tap_bt.grid(row=19, column=4, rowspan=8, columnspan=1,padx=5,
                                pady=3)
# vibrato_bt.grid(row=21, column=0, rowspan=1, columnspan=1,padx=5,
#                                 pady=3)
# bends_bt.grid(row=23, column=0, rowspan=1, columnspan=1,padx=5,
#                                 pady=3)
# finger_slide_bt.grid(row=25, column=0, rowspan=1, columnspan=1,padx=5,
#                                 pady=3)
# col 6 Harmonics
natural_harmonics_bt = Button(root, height=1, text="Nat. Harmonics",
                                  padx=12, pady=5)
artificial_harmonics_bt = Button(root, height=1,text="Arti. Harmonics",
                                 padx=13, pady=5)

harp_harmonics_bt = Button(root, height=1, text="Harp Harmonics", padx=12,
                           pady=5)
slap_harmonics_bt = Button(root, height=1,text="Slap Harmonics", padx=15,
                                pady=5)
kith_rout1_bt = Button(root, height=1,text="Kitharologus R1", padx=15,
                                 pady=5)
kith_rout2_bt = Button(root, height=1,text="Kitharologus R2",
                                  padx=15, pady=5)
kith_rout3_bt = Button(root, height=1,text="Kitharologus R3",
                                  padx=15, pady=5)

natural_harmonics_bt.grid(row=13, column=5, rowspan=1, columnspan=1, padx=5,
                                pady=3)
artificial_harmonics_bt.grid(row=15, column=5, rowspan=1, columnspan=1,padx=5,)

harp_harmonics_bt.grid(row=17, column=5, rowspan=1, columnspan=1, padx=5,
                                pady=3)
slap_harmonics_bt.grid(row=19, column=5, rowspan=1, columnspan=1,padx=5,
                                pady=3)
kith_rout1_bt.grid(row=21, column=5, rowspan=1, columnspan=1,padx=5,
                                pady=3)
kith_rout2_bt.grid(row=23, column=5, rowspan=1, columnspan=1,padx=5,
                                pady=3)
kith_rout3_bt.grid(row=25, column=5, rowspan=1, columnspan=1,padx=5,
                                pady=3)
#
#
# col 7
alegrias_bt = Button(root, height=1, text="Alegrias",
                                  padx=20, pady=5)
solea_bt = Button(root, height=1,text='Solea', padx=27,
                                pady=5)
tangos_bt = Button(root, height=1,text="Tangos", padx=22,
                                 pady=5)
sequiriya_bt = Button(root, height=1,text="Sequiriya",
                                  padx=17, pady=5)
tarantas_bt = Button(root, height=1,text="Tarantas", padx=19,
                                pady=5)
granainas_bt = Button(root, height=1,text="Granainas", padx=16,
                                 pady=5)
buleria_bt = Button(root, height=1,text="Buleria",
                                  padx=24, pady=5)

alegrias_bt.grid(row=13, column=6, rowspan=1, columnspan=1, padx=5,
                                pady=3)
solea_bt.grid(row=15, column=6, rowspan=1, columnspan=1,padx=5,
                                pady=3)
tangos_bt.grid(row=17, column=6, rowspan=1, columnspan=1,padx=5,
                                pady=3)
sequiriya_bt.grid(row=19, column=6, rowspan=1, columnspan=1,padx=5,
                                pady=3)
tarantas_bt.grid(row=21, column=6, rowspan=1, columnspan=1,padx=5,
                                pady=3)
granainas_bt.grid(row=23, column=6, rowspan=1, columnspan=1,padx=5,
                                pady=3)
buleria_bt.grid(row=25, column=6, rowspan=1, columnspan=1,padx=5,
                                pady=3)


root.mainloop()