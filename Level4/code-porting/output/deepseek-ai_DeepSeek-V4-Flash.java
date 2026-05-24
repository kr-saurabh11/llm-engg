
public class Main {
    public static void main(String[] args) {
        final int iterations = 200_000_000;
        final int param1 = 4;
        final int param2 = 1;

        long startTime = System.nanoTime();
        double result = calculate(iterations, param1, param2);
        result *= 4; // Multiply by 4 as in Python
        long endTime = System.nanoTime();

        System.out.printf("Result: %.12f%n", result);
        System.out.printf("Execution Time: %.6f seconds%n", (endTime - startTime) / 1e9);
    }

    private static double calculate(int iterations, int param1, int param2) {
        double result = 1.0;
        for (int i = 1; i <= iterations; i++) {
            int j = i * param1 - param2;
            result -= 1.0 / j;
            j = i * param1 + param2;
            result += 1.0 / j;
        }
        return result;
    }
}
