import numpy as np

class Perceptron:
    """
    A single-layer perceptron model.

    This class encapsulates the weights, bias, and the learning functions
    (activation, prediction, and training).
    """

    def __init__(self, num_inputs=2, learning_rate=0.7, epochs=10000):
        """
        Initializes the Perceptron.
        
        Args:
            num_inputs (int): Number of input features (2 for our logic gates).
            learning_rate (float): The 'coeff' (eta) from the PDF.
            epochs (int): The maximum number of training iterations.
        """
        self.learning_rate = learning_rate
        self.epochs = epochs
        
        # Initialize weights with small random values.
        # We need one weight for each input (e.g., W1, W2).
        self.weights = np.random.rand(num_inputs) 
        
        # Initialize bias. The PDF suggests -1, but a small random
        # value is also a common and effective practice.
        self.bias = np.random.rand(1)

    def sigmoid(self, net_input):
        """
        The Sigmoid activation function as requested by the assignment.
        It squashes any value into a range between 0 and 1.
        
        Equation: out = 1 / (1 + e^(-y))  (where y is net_input)
        """
        return 1 / (1 + np.exp(-net_input))

    def predict(self, inputs):
        """
        Calculates the perceptron's output (prediction) for given inputs.
        This is the "feed-forward" process.
        
        Equation: Net = (x1*w1 + x2*w2) + b
        """
        # Calculate the weighted sum: (x1*w1 + x2*w2)
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        
        # Pass the sum through the activation function
        return self.sigmoid(weighted_sum)

    def train(self, training_inputs, training_outputs):
        """
        The main training loop where the perceptron learns.
        It adjusts weights and bias based on the error.
        """
        # Loop for the maximum number of epochs (our "safety net")
        for epoch in range(self.epochs):
            
            total_error = 0
            
            # Loop through each of the 4 patterns (e.g., [0,0] -> 0)
            for inputs, target in zip(training_inputs, training_outputs):
                
                # 1. Get the perceptron's current prediction
                prediction = self.predict(inputs)

                # 2. Calculate the error (how far off we are)
                # This is (y_target - y) from the PDF
                error = target - prediction
                
                # 3. Calculate the "Delta" (the adjustment amount)
                # This is the "Delta Rule" for a sigmoid neuron.
                # delta = error * (derivative of sigmoid)
                # derivative = prediction * (1 - prediction)
                delta = error * prediction * (1 - prediction)
                
                # 4. Update the weights and bias
                # w_new = w_old + (learning_rate * delta * input)
                self.weights += self.learning_rate * delta * inputs
                self.bias += self.learning_rate * delta
                
                # Keep track of the squared error for this epoch
                total_error += error**2

            # 5. Check for convergence
            # If the total error is very small (or 0), we are done!
            if total_error == 0:
                print(f"   Converged early at epoch {epoch}!")
                break # Exit the training loop


# --- Main part of the script ---

if __name__ == "__main__":
    
    # --- 1. Define the datasets for the logic gates ---
    
    # All gates use the same 4 input patterns
    inputs = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
    
    # Define the target outputs for each gate
    datasets = {
        "OR": np.array([0, 1, 1, 1]),
        "AND": np.array([0, 0, 0, 1]),
        "NAND": np.array([1, 1, 1, 0]),
        "NOR": np.array([1, 0, 0, 0])
    }
    
    # --- 2. Train and Test each logic gate ---
    
    for gate_name, outputs in datasets.items():
        
        print(f"\n--- Training Perceptron for {gate_name} Gate ---")
        
        # Create a new, fresh perceptron for this gate
        perceptron = Perceptron(num_inputs=2, learning_rate=0.7)
        
        # Train the perceptron
        perceptron.train(inputs, outputs.T) # .T transposes to a column vector
        
        # Print the final learned parameters
        print(f"   Final Weights: {perceptron.weights}")
        print(f"   Final Bias: {perceptron.bias}")
        
        # --- 3. Test the trained perceptron ---
        print("\n   Testing Trained Model:")
        for i, input_pattern in enumerate(inputs):
            prediction = perceptron.predict(input_pattern)
            target = outputs[i]
            
            # We round the output (e.g., 0.999 -> 1) to see the final decision
            print(f"   Input: {input_pattern}  Target: {target}  Prediction: {prediction} prediction (rounded): {prediction.round()}")