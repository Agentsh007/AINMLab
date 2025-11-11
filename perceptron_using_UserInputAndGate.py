import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class Perceptron:
    def __init__(self, num_inputs=2, learning_rate=0.7, epochs=10000):
        self.learning_rate = learning_rate
        self.num_inputs = num_inputs
        self.epochs = epochs
        self.weights = 2 * np.random.rand(num_inputs) - 1
        self.bias = np.random.rand(1)
    
    def sigmoid(self, net_inputs):
        
        net_inputs = np.clip(net_inputs, -500, 500)
        return 1 / (1 + np.exp(-net_inputs))

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights) + self.bias
        return self.sigmoid(weighted_sum)

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
            
           
            if total_error < 1e-5:
                print(f"Converged early at epoch {epoch}")
                break
        
            if epoch == self.epochs - 1:
               
                print(f"Total error after training: {total_error}")

            


def main():
    input_size = 2
    training_inputs = np.array(
        [
            [0, 0], [0, 1], [1, 0], [1, 1]
        ]
    )
    
    gate_outputs = {
        "OR": np.array([0, 1, 1, 1]),
        "AND": np.array([0, 0, 0, 1]),
        "NAND": np.array([1, 1, 1, 0]), 
        "NOR": np.array([1, 0, 0, 0])  
    }
    
    perceptron = Perceptron(input_size,0.4,10000)
    
    while True:
        gate = input("Enter the gate name (AND, OR, NAND, NOR): ").upper().strip()
        if gate in gate_outputs:
            break
        print("Invalid gate name. Please try again.")
  
    target = gate_outputs[gate]
    print(f"---Training for {gate} gate----")
    perceptron.train(training_inputs, target)
    
    print(f"Final weights: {perceptron.weights}")
    print(f"Final bias: {perceptron.bias}")
    
    prediction = perceptron.predict(training_inputs)
    
    prediction_labels = np.round(prediction)
    
    print(f"\n--- Model Evaluation on Training Set ---")
    print(f"Accuracy: {accuracy_score(target, prediction_labels):.2%}")
    print(f"Classification Report: \n{classification_report(target, prediction_labels)}")
    print(f"Confusion Matrix: \n{confusion_matrix(target, prediction_labels)}")
    
    print("\n--- Test with user Inputs ---")
    while True:
            test_input = []
            val1 = float(input("Enter input 1: "))
            val2 = float(input("Enter input 2: "))
            test_input = np.array([val1, val2])
            
            pred_val = perceptron.predict(test_input)
            pred_label = np.round(pred_val)
            
            print(f"Input: {test_input} -> Raw: {pred_val}  -> Prediction: {pred_label}")
            
            toQuit = input("To quit enter 'q' (or press Enter to continue): ")
            if toQuit == 'q':
                return
if __name__ == "__main__":
    main()