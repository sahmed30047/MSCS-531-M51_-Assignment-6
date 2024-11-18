#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define VECTOR_SIZE 1000000  // Size of the vectors
#define NUM_THREADS 4        // Number of threads

// Global variables
double *x, *y;
double a = 2.0;  // Scalar value

// Function for each thread to execute
void *daxpy_thread(void *arg) {
    int thread_id = *(int *)arg;
    int chunk_size = VECTOR_SIZE / NUM_THREADS;
    int start = thread_id * chunk_size;
    int end = start + chunk_size;

    for (int i = start; i < end; i++) {
        y[i] = a * x[i] + y[i];
    }
    return NULL;
}

int main() {
    x = (double *)malloc(VECTOR_SIZE * sizeof(double));
    y = (double *)malloc(VECTOR_SIZE * sizeof(double));

    // Initialize vectors
    for (int i = 0; i < VECTOR_SIZE; i++) {
        x[i] = i * 0.01;
        y[i] = i * 0.02;
    }

    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];

    // Create and execute threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i;
        pthread_create(&threads[i], NULL, daxpy_thread, &thread_ids[i]);
    }

    // Wait for all threads to complete
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    // Print the first 10 results for verification
    for (int i = 0; i < 10; i++) {
        printf("y[%d] = %f\n", i, y[i]);
    }

    // Cleanup
    free(x);
    free(y);

    return 0;
}
