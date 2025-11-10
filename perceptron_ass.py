import numpy as np
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

class Perceptron:
    def __init__(self, num_inputs=2, learning_rate=0.7, epochs=10000):
        self.learning_rate = learning_rate
        self.num_inputs = num_inputs
        self.epochs = epochs
        self.weights = 2 * np.random.rand(num_inputs) - 1
        self.bias = np.random.rand(1)

    def sigmoid_func(self, net_input):
        # Clip input to avoid overflow in exp()
        net_input = np.clip(net_input, -500, 500)
        return 1 / (1 + np.exp(-net_input))

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        return self.sigmoid_func(weighted_sum)

    def train(self, training_inputs, training_outputs):
        for epoch in range(self.epochs):
            total_error = 0
            for inputs, target in zip(training_inputs, training_outputs):
                prediction = self.predict(inputs)
                error = target - prediction
                delta = error * prediction * (1 - prediction)
                self.weights += self.learning_rate * delta * inputs
                self.bias += self.learning_rate * delta
                total_error += error ** 2
            
            # Check the scalar value of the total error
            if total_error < 1e-5:
                print(f"Converged early at epoch {epoch}")
                break
        
            if epoch == self.epochs - 1:
                # Print final error if it didn't converge early
                print(f"Total error after training: {total_error}")

if __name__ == "__main__":

    # ✅ Only binary inputs for training
    inputs = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ])
   ##dictionary
    datasets = {
        "OR":   np.array([0, 1, 1, 1]),
        "AND":  np.array([0, 0, 0, 1]),
        "NOR":  np.array([1, 0, 0, 0]),
        "NAND": np.array([1, 1, 1, 0])
    }

    # ✅ Fractional test inputs — only for checking behavior
    custom_inputs = np.array([
        [0.1, 0.3], # Should be (0, 0)
        [0.8, 0.2], # Should be (1, 0)
        [0.1, 0.1], # Should be (0, 0)
        [0.9, 0.7]  # Should be (1, 1)
    ])
    num_pairs = int(input("How many input pairs do you want to test? (Enter 0 to skip): "))
    custom_inputs_list = []
    for i in range(num_pairs):
        val1 = float(input(f"  Enter input 1 for pair {i+1}: "))
        val2 = float(input(f"  Enter input 2 for pair {i+1}: "))
        custom_inputs_list.append([val1, val2])

    for gate_name, outputs in datasets.items():
        
        print(f"\n--- Training for {gate_name} Gate ---")
        perceptron = Perceptron(num_inputs=2, learning_rate=0.7, epochs=200)
        perceptron.train(inputs, outputs)

        print(f"Final Weights: {perceptron.weights}")
        print(f"Final Bias: {perceptron.bias}\n")
        print(f"--- Testing {gate_name} on Custom Inputs ---")

        # --- MODIFICATION: Create lists to store all results ---
       
        all_targets = []
        all_predictions = []
        for test_in in custom_inputs:
            pred_val = perceptron.predict(test_in)

            # Convert fractional inputs to binary (for target generation)
            in1 = 1 if test_in[0] >= 0.5 else 0
            in2 = 1 if test_in[1] >= 0.5 else 0

            # Determine correct target output for this gate
            if gate_name == "AND":
                target = in1 & in2
            elif gate_name == "OR":
                target = in1 | in2
            elif gate_name == "NAND":
                target = int(not (in1 & in2))
            elif gate_name == "NOR":
                target = int(not (in1 | in2))
            else:
                target = None

            # Binary classification output
            pred_label = 1 if pred_val >= 0.5 else 0
            
            print(f"Input: {test_in} ...|... Logical Target: {target} ...|.... Prediction: {pred_label} (Raw: {pred_val[0]:.4f})")
            
            # --- MODIFICATION: Append results to lists ---
            all_targets.append(target)
            all_predictions.append(pred_label)

            # --- MODIFICATION: Print reports AFTER the loop ---
        print(f"\n--- Summary for {gate_name} ---")
    
        # Calculate and print metrics
        acc = accuracy_score(all_targets, all_predictions)
        cm = confusion_matrix(all_targets, all_predictions)
        report = classification_report(all_targets, all_predictions, zero_division=0, target_names=["Class 0", "Class 1"])

        print(f"Accuracy: {acc:.2%}")
        print(f"Confusion Matrix:\n{cm}")
        print(f"Classification Report:\n{report}")
        print("---------------------------------")