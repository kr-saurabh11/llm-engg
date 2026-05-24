
// Main.java
public class Main {

    /**
     * Calculates a series sum based on the given parameters.
     * This function performs a specific sequence of additions and subtractions
     * involving the reciprocal of terms derived from the iteration index and parameters.
     *
     * @param iterations The number of times to iterate the calculation.
     * @param param1 A double parameter used in calculating terms.
     * @param param2 A double parameter used in calculating terms.
     * @return The final calculated double result.
     */
    public static double calculate(int iterations, double param1, double param2) {
        double result = 1.0;
        // The loop iterates from 1 up to 'iterations' (inclusive).
        for (int i = 1; i <= iterations; i++) {
            // Cast 'i' to double for floating-point arithmetic from the start
            // to avoid potential intermediate integer overflow if 'i * param1'
            // were done with int, although param1 is double here.
            double i_double = (double) i;

            // Calculate the first term and subtract its reciprocal from result
            double j_minus = i_double * param1 - param2;
            result -= (1.0 / j_minus); // Use 1.0 for double division

            // Calculate the second term and add its reciprocal to result
            double j_plus = i_double * param1 + param2;
            result += (1.0 / j_plus); // Use 1.0 for double division
        }
        return result;
    }

    public static void main(String[] args) {
        // Record the start time using System.nanoTime() for high precision.
        long startTime = System.nanoTime();

        // Perform the calculation as specified in the Python code.
        // The literals 4 and 1 are automatically promoted to double during arithmetic.
        double result = calculate(200_000_000, 4.0, 1.0) * 4.0;

        // Record the end time.
        long endTime = System.nanoTime();

        // Calculate the elapsed time in seconds.
        double elapsedTimeSeconds = (endTime - startTime) / 1_000_000_000.0;

        // Print the result formatted to 12 decimal places.
        System.out.printf("Result: %.12f%n", result);
        // Print the execution time formatted to 6 decimal places.
        System.out.printf("Execution Time: %.6f seconds%n", elapsedTimeSeconds);
    }
}
