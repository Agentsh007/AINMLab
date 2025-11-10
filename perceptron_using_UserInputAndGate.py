import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class Perceptron:
    def __init__(self, learning_rate=0.2, num_inputs=2):
        self.learning_rate = learning_rate
        self.num_inputs = num_inputs
        # FIX 1: Bias should be a single scalar value, not a vector
        self.weights = 2 * np.random.rand(num_inputs) - 1
        self.bias = np.random.rand(1) # Was: np.random.rand(num_inputs)

    # FIX 2: Corrected spelling
    def sigmoid(self, net_inputs):
        # Clip to avoid overflow in exp()
        net_inputs = np.clip(net_inputs, -500, 500)
        return 1 / (1 + np.exp(-net_inputs))

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        return self.sigmoid(weighted_sum)

    def train(self, training_inputs, training_outputs, max_error, max_epochs=10000):
        avg_error = 1e10 # Start with a high error
        epoch = 0

        # FIX 3: Loop condition was backward. 
        # We must loop WHILE error is GREATER than max_error
        while avg_error > max_error:
            total_error = 0
            for inputs, target in zip(training_inputs, training_outputs):
                pred_val = self.predict(inputs)
                error = target - pred_val
                delta = error * pred_val * (1 - pred_val)
                
                self.weights += self.learning_rate * delta * inputs
                self.bias += self.learning_rate * delta
                total_error += abs(error)
            
            # FIX 4: Average error should be over the number of *examples*
            avg_error = total_error / len(training_inputs)
            epoch += 1
            
            # Optional: Print progress
            if epoch % 1000 == 0:
                print(f"Epoch {epoch}, Avg Error: {avg_error:}") 
            if epoch == max_epochs:
                print(f"Warning: Reached max epochs ({max_epochs}) without converging.")
                break
        
        print(f"Converged in {epoch} epochs.")
            


def main():
    input_size = 2
    training_inputs = np.array(
        [
            [0, 0], [0, 1], [1, 0], [1, 1]
        ]
    )
    
    # FIX 5: Corrected logic gates
    gate_outputs = {
        "OR": np.array([0, 1, 1, 1]),
        "AND": np.array([0, 0, 0, 1]),
        "NAND": np.array([1, 1, 1, 0]), # Was "NOT" and was incorrect
        "NOR": np.array([1, 0, 0, 0])  # Was incorrect (had [1,1,1,0])
    }
    
    perceptron = Perceptron(0.4, input_size)
    
    # Add a loop to ensure valid gate is entered
    while True:
        gate = input("Enter the gate name (AND, OR, NAND, NOR): ").upper().strip()
        if gate in gate_outputs:
            break
        print("Invalid gate name. Please try again.")
        
    target = gate_outputs[gate]
    print(f"---Training for {gate} gate----")
    # Pass 0.01 as the max_error target
    perceptron.train(training_inputs, target, 0.01)
    
    print(f"Final weights: {perceptron.weights}")
    print(f"Final bias: {perceptron.bias}")
    
    # --- Evaluation on Training Data ---
    prediction = perceptron.predict(training_inputs)
    
    # FIX 6: Must round probabilities to 0 or 1 *before* checking accuracy
    # Your old `for` loop did not modify the `prediction` array
    prediction_labels = np.round(prediction)
    
    print(f"\n--- Model Evaluation on Training Set ---")
    # Use the new `prediction_labels` for metrics
    print(f"Accuracy: {accuracy_score(target, prediction_labels):.2%}")
    print(f"Classification Report: \n{classification_report(target, prediction_labels)}")
    print(f"Confusion Matrix: \n{confusion_matrix(target, prediction_labels)}")
    
    # --- Custom Test Loop ---
    print("\n--- Test with user Inputs ---")
    while True:
            test_input = []
            # FIX 7: Clearer prompts for user
            val1 = float(input("Enter input 1: "))
            val2 = float(input("Enter input 2: "))
            test_input = np.array([val1, val2])
            
            pred_val = perceptron.predict(test_input)
            # Round the final fractional output to 0 or 1
            pred_label = np.round(pred_val)
            
            print(f"Input: {test_input} -> Raw: {pred_val}  -> Prediction: {pred_label}")
            
            # FIX 8: Must *call* the .lower() method with ()
            toQuit = input("To quit enter 'q' (or press Enter to continue): ")
            if toQuit == 'q':
                return
if __name__ == "__main__":
    main()