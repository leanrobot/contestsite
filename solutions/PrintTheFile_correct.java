import java.io.File;
import java.util.Scanner;
import java.io.FileNotFoundException;

public class PrintTheFile_correct {
	public static void main(String [] args) throws FileNotFoundException {
		File file = new File("printthefile.txt");
		Scanner in = new Scanner(file);

		while(in.hasNextLine()) {
			System.out.println(in.nextLine());
		}
	}
}