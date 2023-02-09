# just testing the code

def analyze_lottery_numbers(numbers, drawn_numbers):
    matches = 0
    for number in numbers:
        if number in drawn_numbers:
            matches += 1
    return matches

# Example usage:

winning_numbers = [5, 12, 19, 24, 33, 47]
my_numbers = [5, 12, 19, 24, 33, 47]

matching_numbers = analyze_lottery_numbers(my_numbers, winning_numbers)

if matching_numbers == 6:
    print("Congratulations! You have won the jackpot!")
elif matching_numbers == 5:
    print("You have won a prize!")
else:
    print("Better luck next time. You have matched", matching_numbers, "numbers.")