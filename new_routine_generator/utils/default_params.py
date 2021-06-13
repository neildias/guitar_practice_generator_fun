from datetime import datetime
from pprint import pprint


# accuracte time: year, month, day, hour, minute, second
today = datetime.now()
today_time = str(today.time())[:8].replace(":", "_")
today_date = str(today.date()).replace("-", "_")
todays_full_date = today_date + "_" + today_time

path = "C:\\Users\\Neil\\guitar_practice_tracker\\"
backup_path = "E:\\guitar_practice_tracker\\"
cloud_path = "P:\\guitar_practice_tracker\\"

main_file_name = "guitar_practice_tracker.xlsx"
record_log = "record_log.txt"
#today = main_file_name + "_" + today_date + "_" + today_time + \
                   #".xlsx"

def dict_total(data_dict: dict):
  """
  Simple function to compute total of all int / float values in a dict
  :param data_dict:
  :return: int
  """
  total_value = 0
  for _, value in data_dict.items():
    if isinstance(value, int) or isinstance(value, float):
      total_value += value
  return int(total_value)


topics = {
    # Theory and sight reading / playing
    "Music_Theory Rhythm": 0,
    "Music_Theory Melody": 0,
    "Music_Theory SongWriting": 0,
    "Sight Reading Classical": 0,
    "Sight Reading_App": 0,
    "Ear Training Melody": 0,
    "Ear Training Rhythm": 0,
    "Sight Playing Classical Pieces": 0,
    "Sight Playing Graded": 0,
    "Sight Playing Others": 0,
    "Kitharologus": 0,
    "Jamming with Other": 0,

    # Practical Rhythm
    "Chord_Changing": 0,
    "Chord_Progression_Families": 0,
    "Caged Chords": 0,
    "Arpeggiate Chords": 0,
    "Two-Voice Chords": 0,
    "Chords with Pick": 0,
    "Chords with Rasgeo": 0,
    "Chords with Rumba": 0,
    "Chords with Fan": 0,
    "Palm Beat Chords": 0,
    "Other Percussion Chords": 0,
    "Caged System (Other)":0,

    # FB Mastery
    "FB Mastery Find Tonic": 0,
    "FB Mastery Find Tonic": 0,

    # Creative Musical
    "Soloing on Key from Scratch": 0,
    "Improvising with Chords": 0,
    "Improvising existing Melody": 0,
    "Song Writing": 0,
    "Rhythm Song Playing": 0,
    "Lead Playing NFN": 0,

    # Scales WO
    "Caged Scale":0,
    "Scale Shapes": 0,
    "Scale Modes (Sound)": 0,
    "2 Octave Scales": 0,
    "3 Octave Scales": 0,
    "Scales with Vibrato": 0,
    "Scales with Bends": 0,
    "Scales with Slides": 0,
    "Pentatonic Scales": 0,
    "Exotic Scales": 0,
    "Fast Picking": 0,
    "Economy Picking": 0,

    # dedicated technical practice
    "Slurs": 0,
    "Vibrato": 0,
    "Slide": 0,
    "Bends": 0,
    "Picado": 0,
    "Rasgeo": 0,
    "Pulgar": 0,
    "Alzapua": 0,
    "Golpe": 0,
    "Natural Harmonics": 0,
    "Artificial Harmonics": 0,
    "Slap Harmonics": 0,
    "Harp Harmonics": 0,
    "Tremelo": 0,
    "Alternate Picking":0,
    "Sweep Picking": 0,
    "Hybrid Picking": 0,
    "Tapping": 0,
    "Percussive": 0,
    "Whammy bar": 0,
    "Pedals": 0,

    # flamenco
    "Solea": 0,
    "Alegrias": 0,
    "Tangos": 0,
    "Seguiriya": 0,
    "Tarantas": 0,
    "Granainas": 0,
    "Bulerias": 0,
    "Flamenco RH": 0,
    "Flamenco LH": 0,
  }

# lessons

lesson_1 = {
    # Classical
    # lesson 1 total 30 mins
    "Spider Warmup": 5,
    "Ear Training Melody": 5,
    "Sight Playing Graded": 40,
    "Picado": 10,
}

lesson_2 = {
    # Scales 40
    "Scale Shapes": 15,
    "Scale Modes (Sound)": 15,
    "2 Octave Scales": 15,
    "Economy Picking": 15,
}

lesson_3 = {
    # technical workout 60 mins
    "Kitharologus": 15,
    "Natural Harmonics": 5,
    "Slurs": 15,
    "Vibrato": 10,
    "Slide": 5,
    "Bends": 10,
    "Tremelo": 10,
}

# add chord workout on even days of the week
# add_chord_workout = "Strum Chords" if today.day % 2 == 0 else "Arpeggiate
# Chords"

lesson_4 = {
    # Chords
    # doubles the strum chord time if add_chord_workout = 'Strum Chords'
    "Chord_Changing": 15,
    "Chord_Progression_Families": 10,
    "Caged Chords": 10,
    "Arpeggiate Chords": 10,
    "Chords with Rasgeo": 10,
    "Ear Training Rhythm": 5,
}

# choose Improvisation on even days of the week
# creative_workout = "Improvisation" if today.day % 2 == 0 else "Rhythm (
# Song) Practice"

lesson_5 = {

    # technical workout - others
    # Improvise on even days, else play rhythm songs
    "Soloing on Key from Scratch": 20,
    "Rhythm Song Playing": 20,

}

lesson_6 = {
    "Music_Theory Rhythm": 10,
    "Music_Theory Melody": 10,
    "Sight Reading_App": 10,
    "FB Mastery Find Tonic": 10,
}


# consolidating the above lessons
total_lessons = {

    "Classical Studies" : lesson_1,
    "Scales": lesson_2,
    "Technical": lesson_3,
    "Chords": lesson_4,
    "Creative": lesson_5,
    "Music Theory": lesson_6,


}

lessons_key = {

    1 : "Classical Studies",
    2 : "Scales" ,
    3 : "Technical",
    4 : "Chords",
    5 : "Creative",
    6 : "Music Theory",

}

practice_lesson_header_message = f"""\n

     PRACTICE LESSON HEADERS
     =======================\n
                                 Original Time
                                 -------------
        1. Classical Studies - \t\t{dict_total(lesson_1)} mins
        
            {lesson_1}
            
        2. Scales            - \t\t{dict_total(lesson_2)} mins 
            
            {lesson_2}
            
        3. Technical         - \t\t{dict_total(lesson_3)} mins
            
            {lesson_3}
            
        4. Chords            - \t\t{dict_total(lesson_4)} mins
        
            {lesson_4}
            
        5. Creative          - \t\t{dict_total(lesson_5)} mins
        
            {lesson_5}
            
        6. Music Theory      - \t\t{dict_total(lesson_6)} mins
        
            {lesson_6}

    """

note_duration = ("\nNote duration for each beat? "
                 "\nOptions:"
                 "\n-------"
                 "\nNo Notes         0/0   (0)"
                 "\nDouble           8/1   (1)"
                 "\nWhole            4/1   (2)"
                 "\nHalf             4/2   (3)"
                 "\nQuarter          4/4   (4)"
                 "\nEighth           4/8   (5)"
                 "\nSixteenth        4/16  (6)"
                 "\nThirtySecondth   4/32  (7)"
                 "\nSixtyFourth      4/64  (8)")

note_duration_dict = {
    0: "None",
    1: "Double",
    2: "Whole",
    3: "Half",
    4: "Quarter",
    5: "Eighth",
    6: "Sixteenth",
    7: "ThirtySecondth",
    8: "SixtyFourth",
}
