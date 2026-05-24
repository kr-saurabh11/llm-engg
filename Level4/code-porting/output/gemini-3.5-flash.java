// An elegant and high-performance Java 17 implementation of the Python code.
//
// To maximize execution speed while producing an identical output down to the last decimal place, this implementation unrolls the loop. This allows the CPU to pipeline the independent floating-point division operations, significantly reducing execution time.
//

import java.util.Locale;

public class Main {

    public static void main(String[] args) {
        long startTime = System.nanoTime();
        double result = calculate(200_000_000, 4, 1) * 4;
        long endTime = System.nanoTime();

        System.out.printf(Locale.US, "Result: %.12f%n", result);
        System.out.printf(Locale.US, "Execution Time: %.6f seconds%n", (endTime - startTime) / 1e9);
    }

    public static double calculate(int iterations, int param1, int param2) {
        double result = 1.0;
        double p1 = param1;
        double p2 = param2;
        
        int i = 1;
        // Unroll the loop by 4 to parallelize the independent divisions in CPU pipelines
        int limit = iterations - 3;
        for (; i <= limit; i += 4) {
            double ip1_0 = i * p1;
            double ip1_1 = (i + 1) * p1;
            double ip1_2 = (i + 2) * p1;
            double ip1_3 = (i + 3) * p1;

            double d0_1 = 1.0 / (ip1_0 - p2);
            double d0_2 = 1.0 / (ip1_0 + p2);
            double d1_1 = 1.0 / (ip1_1 - p2);
            double d1_2 = 1.0 / (ip1_1 + p2);
            double d2_1 = 1.0 / (ip1_2 - p2);
            double d2_2 = 1.0 / (ip1_2 + p2);
            double d3_1 = 1.0 / (ip1_3 - p2);
            double d3_2 = 1.0 / (ip1_3 + p2);

            // Accumulate in exact same sequential order to guarantee identical precision
            result -= d0_1;
            result += d0_2;
            result -= d1_1;
            result += d1_2;
            result -= d2_1;
            result += d2_2;
            result -= d3_1;
            result += d3_2;
        }
        
        // Clean up remaining iterations
        for (; i <= iterations; i++) {
            double ip1 = i * p1;
            result -= 1.0 / (ip1 - p2);
            result += 1.0 / (ip1 + p2);
        }
        
        return result;
    }
}
