
public class Main {
    public static void main(String[] args) {
        final int N = 200_000_000;
        long start = System.nanoTime();
        double result = 1.0;
        int p = 4; // 4 * 1
        // Unrolled by 8 to reduce loop overhead and help the CPU pipeline divisions
        for (int i = 0; i < N; i += 8) {
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
            result = result - 1.0 / (p - 1) + 1.0 / (p + 1); p += 4;
        }
        result *= 4.0;
        long end = System.nanoTime();
        double elapsed = (end - start) / 1_000_000_000.0;
        System.out.printf("Result: %.12f%n", result);
        System.out.printf("Execution Time: %.6f seconds%n", elapsed);
    }
}
