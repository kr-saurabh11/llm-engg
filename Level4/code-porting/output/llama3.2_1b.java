
import java.util.Random;
import java.lang.reflect.Method;

public class Main {
    private static final long START_TIME = System.currentTimeMillis();

    public static void main(String[] args) throws NoSuchMethodException, SecurityException {
        // Generate an array of random integers from 0 to 10
        int[] params = new int[4];
        Random rand = new Random();
        for (int i = 0; i < 4; ++i) {
            params[i] = rand.nextInt(11);
        }

        long result = calculate(params, 0, 1, 2);

        // Print the result
        System.out.format("Result: %12f%n", result);

        // Calculate execution time in milliseconds
        int[] iterations = {200_000_000};
        double executionTimeMs = (System.currentTimeMillis() - START_TIME) / 1000.0;

        // Print the execution time
        System.out.printf("Execution Time: %.6f seconds%n", executionTimeMs);
    }

    public static long calculate(int[] params, int iterations, float param1, float param2) {
        long result = 0;
        for (int i = 0; i < iterations; ++i) {
            float j = (float) params[0] * param1 - param2 + 1 / ((float) params[0]);
            if (i == 0) {
                j = (params[0] + param1) * (float) param2 - (float) i;
            }
            result += 1 / j;
        }

        return result;
    }
}
