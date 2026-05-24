//An extremely fast C++ implementation of the Python code using multi-threading (optimized for the 4 performance cores of the Apple M2) and compiler-vectorized loops.


#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <iomanip>
#include <functional>

// Worker function for each thread
void worker(int start, int end, double param1, double param2, double& out_sum) {
    double sum = 0.0;
    
    // Explicitly hint the compiler to vectorize this loop
    #pragma clang loop vectorize(enable)
    for (int i = start; i <= end; ++i) {
        double ip = (double)i * param1;
        double j1 = ip - param2;
        double j2 = ip + param2;
        sum += (1.0 / j2 - 1.0 / j1);
    }
    
    // Write to the output reference only once to avoid false sharing
    out_sum = sum;
}

double calculate(int iterations, double param1, double param2) {
    // Apple M2 has 4 high-performance cores. Spawning 4 threads avoids 
    // scheduling on the slower efficiency cores and maximizes throughput.
    const int num_threads = 4;
    std::vector<std::thread> threads;
    std::vector<double> partial_sums(num_threads, 0.0);
    
    int chunk_size = iterations / num_threads;
    for (int t = 0; t < num_threads; ++t) {
        int start = 1 + t * chunk_size;
        int end = (t == num_threads - 1) ? iterations : (t + 1) * chunk_size;
        threads.emplace_back(worker, start, end, param1, param2, std::ref(partial_sums[t]));
    }
    
    double result = 1.0;
    for (int t = 0; t < num_threads; ++t) {
        threads[t].join();
        result += partial_sums[t];
    }
    return result;
}

int main() {
    auto start_time = std::chrono::high_resolution_clock::now();
    
    double result = calculate(200000000, 4.0, 1.0) * 4.0;
    
    auto end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> diff = end_time - start_time;
    
    std::cout << std::fixed << std::setprecision(12);
    std::cout << "Result: " << result << std::endl;
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "Execution Time: " << diff.count() << " seconds" << std::endl;
    
    return 0;
}
