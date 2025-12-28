import random

def run_simulator():
    while True:
        # Number of qubits to send
        num_qubits = 100

        # STEP 1 & 2: Initial Setup (Moved inside loop for fresh data each run)
        alice_bits = [random.randint(0, 1) for _ in range(num_qubits)]
        alice_bases = [random.randint(0, 1) for _ in range(num_qubits)]
        bob_bases = [random.randint(0, 1) for _ in range(num_qubits)]

        # Pre-calculate matching positions for both scenarios
        matching_positions = [i for i in range(num_qubits) if alice_bases[i] == bob_bases[i]]

        print("\n" + "="*60)
        print("            QKD EAVESDROPPING DETECTION SIMULATOR")
        print("="*60)
        print("1. Transmission WITHOUT Eve")
        print("2. Transmission WITH Eve")
        print("3. Conclusion & Comparison")
        print("4. Exit Program")
        print("="*60)

        choice = input("Enter Simulation Number: ")

        if choice == '1':
            print("\nSCENARIO 1: SECURE TRANSMISSION (No Eve)")
            received_bits_no_eve = alice_bits.copy()
            
            errors_no_eve = 0
            for pos in matching_positions:
                if alice_bits[pos] != received_bits_no_eve[pos]:
                    errors_no_eve += 1
            
            error_rate_no_eve = (errors_no_eve / len(matching_positions)) * 100
            
            print(f" - Matching bases: {len(matching_positions)}")
            print(f" - Errors detected: {errors_no_eve}")
            print(f" - Error rate: {error_rate_no_eve:.2f}%")
            print(" - Status: SECURE")

        elif choice == '2':
            print("\nSCENARIO 2: WITH EAVESDROPPER (Eve Present)")
            eve_bases = [random.randint(0, 1) for _ in range(num_qubits)]
            received_bits_with_eve = alice_bits.copy()
            
            for i in range(num_qubits):
                if alice_bases[i] != eve_bases[i]:
                    if random.random() < 0.5:
                        received_bits_with_eve[i] = 1 - alice_bits[i]
            
            errors_with_eve = 0
            for pos in matching_positions:
                if alice_bits[pos] != received_bits_with_eve[pos]:
                    errors_with_eve += 1
            
            error_rate_with_eve = (errors_with_eve / len(matching_positions)) * 100
            
            print(f" - Matching bases: {len(matching_positions)}")
            print(f" - Errors detected: {errors_with_eve}")
            print(f" - Error rate: {error_rate_with_eve:.2f}%")
            
            if error_rate_with_eve > 15: # Standard threshold for detection
                print(" - Status: ALERT! EAVESDROPPING DETECTED!")
            else:
                print(" - Status: SECURE")

        elif choice=='3':
            print("\n============================================================")
            print("COMPARISON & CONCLUSION")
            print("============================================================")
            print(f"\nWithout Eve: {error_rate_no_eve:.2f}% error rate")
            print(f"With Eve:    {error_rate_with_eve:.2f}% error rate")
            print(f"\nError increase: {error_rate_with_eve - error_rate_no_eve:.2f}%")

        elif choice == '4':
            print("\nExiting Simulator. Stay secure!")
            break # This exits the while loop
        
        else:
            print("Invalid input. Please enter 1, 2, 3 or 4.")

        input("\nPress Enter to return to the menu...")

if __name__ == "__main__":
    run_simulator()