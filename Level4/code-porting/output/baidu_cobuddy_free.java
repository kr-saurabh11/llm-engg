
public class Main {
    public static void main(String[] args) {
        final int iterations = 200_000_000;
        final int param1 = 4;
        final int param2 = 1;

        long startTime = System.nanoTime();

        double result = 1.0;
        for (int i = 1; i <= iterations; i++) {
            double term = i * param1;          // i * 4
            double j1 = term - param2;        // i*4 - 1
            double j2 = term + param2;        // i*4 + 1
            result -= 1.0 / j1;
            result += 1.0 / j2;
        }
        result *= 4;

        long endTime = System.nanoTime();
        double elapsedSeconds = (endTime - startTime) / 1_000_000_000.0;

        System.out.printf("Result: %.12f%n", result);
        System.out.printf("Execution Time: %.6f seconds%n", elapsedSeconds);
    }
}
