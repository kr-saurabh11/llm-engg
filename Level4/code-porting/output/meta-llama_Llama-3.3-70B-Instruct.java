
// Main.java

public class Main {
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        double result = calculate(200_000_000, 4, 1) * 4;
        long endTime = System.nanoTime();

        System.out.printf("Result: %.12f%n", result);
        System.out.printf("Execution Time: %.6f seconds%n", (endTime - startTime) / 1e9);
    }

    public static double calculate(long iterations, double param1, double param2) {
        double result = 1.0;
        // unroll loop to reduce overhead of repeated calculations
        for (int i = 1; i <= iterations; i++) {
            double j1 = i * param1 - param2;
            double j2 = i * param1 + param2;
            result -= (1 / j1);
            result += (1 / j2);
        }
        return result;
    }
}
