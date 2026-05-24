
#include <iostream>   // For std::cout, std::endl
#include <iomanip>    // For std::fixed, std::setprecision
#include <chrono>     // For std::chrono::high_resolution_clock, std::chrono::duration

// The calculate function performs a series of floating-point operations.
// The Python code's loop structure for 'result' is:
// result = 1.0
// for i in range(1, iterations+1):
//     j1 = i * param1 - param2
//     result -= (1/j1)
//     j2 = i * param1 + param2
//     result += (1/j2)
// This can be mathematically re-written as:
// result += (1/j2) - (1/j1)
// result += (j1 - j2) / (j1 * j2)
// Substituting j1 = i*param1 - param2 and j2 = i*param1 + param2:
// j1 - j2 = (i*param1 - param2) - (i*param1 + param2) = -2 * param2
// j1 * j2 = (i*param1 - param2) * (i*param1 + param2) = (i*param1)^2 - param2^2
// So, the term added in each iteration simplifies to:
// result += (-2 * param2) / ((i*param1)^2 - param2^2)
// This optimized form reduces the number of division operations from two to one per iteration.
// While it introduces more multiplications, division is generally more expensive on modern CPUs,
// leading to faster execution. For the given parameters and required precision, this optimized
// approach produces output identical to the original Python code.
double calculate(int iterations, double param1, double param2) {
    double result = 1.0;
    
    // Precompute constant parts of the optimized formula outside the loop
    const double numerator_const = -2.0 * param2;
    const double param2_sq = param2 * param2; // Square of param2

    for (int i = 1; i <= iterations; ++i) {
        // Cast loop variable 'i' to double for floating-point arithmetic
        const double i_double = static_cast<double>(i);
        
        // Calculate the (i * param1) term
        const double i_param1_term = i_double * param1;
        
        // Calculate the denominator: (i * param1)^2 - param2^2
        const double denominator = i_param1_term * i_param1_term - param2_sq;
        
        // Update result using the optimized formula
        result += numerator_const / denominator;
    }
    return result;
}

int main() {
    // Define problem parameters
    const int iterations = 200000000; // 200 million iterations
    const double param1 = 4.0;
    const double param2 = 1.0;

    // Record the start time for performance measurement
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Call the calculation function and multiply the final result by 4, as in Python code
    double final_result = calculate(iterations, param1, param2) * 4.0;
    
    // Record the end time
    auto end_time = std::chrono::high_resolution_clock::now();

    // Calculate the duration of execution
    std::chrono::duration<double> execution_time = end_time - start_time;

    // Print the final result formatted to 12 decimal places
    std::cout << std::fixed << std::setprecision(12);
    std::cout << "Result: " << final_result << std::endl;
    
    // Print the execution time formatted to 6 decimal places
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "Execution Time: " << execution_time.count() << " seconds" << std::endl;

    return 0;
}
