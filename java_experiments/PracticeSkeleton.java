import java.util.Scanner;

public class PracticeSkeleton {

    public  static void main(String[] args) {

        System.out.println("Welcome to the Guitar Trainer Program!");

        // values notes
        String [] noteValue = new String[] {
                "Double",
                "Whole",
                "Half",
                "Quarter",
                "Eighth",
                "Sixteenth",
                "ThirtySecond",
                "SixtyFourth",
                "OneTwentyEighth",
        };

        // values - Headers
        String[] practiceHeads = new String[] {
                "Music Theory",
                "Technical WO",
                "Scales",
                "Chords",
                "SongWriting",
                "FretboardMastery",
                "Improvisation",
                "PlayByEar",
                "EarTraining",
                "SongPlayingTutorial",
        };


        // get first name and last name
        // first name
        System.out.println("Please enter your first name: ");
        Scanner input = new Scanner(System.in);
        String userFirstName = input.next();

        System.out.println("Please enter your last name: ");
        input = new Scanner(System.in);
        String userLastName = input.next();


        System.out.printf("Hello " + userFirstName + " " + userLastName + "! You need to choose from below options: ");

        // show what is needed to practice,

        for (int i = 0; i < practiceHeads.length; i++) {
            System.out.println("\n");
            System.out.printf(practiceHeads[i]);
            //System.out.printf("\n");
        }
        //
        // advanced option - let the user enter option, extend array
        // ask user to choose
        System.out.printf("\n\nSo which of those do you want to practice? ");
        input = new Scanner(System.in);
        String userChoice = input.next();

        // advanced check membership in array else append
        System.out.println("\nYou chose : " + userChoice + ". Now let's practice!");

        Boolean practiceTime = true;

        while (practiceTime) {
            System.out.println("Practice time of activity "+ userChoice + " begun.");
            System.out.println("You may stop. Practice time has expired. Good work!");
            System.out.printf("Do you want to practice it again? 1 for yes, else 0");
            input = new Scanner(System.in);
            int practiceAgain = input.nextInt();
            // if chosen 'n' break the loop
            if (practiceAgain == 0) {
                practiceTime = false;
            }
        }
        // ask for tempo (0-300)
        System.out.printf("\nAt what tempo did you practice your last session (eg. 20)?");
        input = new Scanner(System.in);
        int tempo = input.nextInt();

        while (tempo < 0 | tempo > 300) {
            System.out.println("\nChoose value between 0 and 300\n");
            input = new Scanner(System.in);
            tempo = input.nextInt();
        }

        // ask for notes (double to 128th)
        // print congratulatory output message
        System.out.println("\nCongratulations. You have successfully finished your guitar practice!");

    }
}
