import numpy as np
import pandas as pd
import sys

def custom_order(small_boards):
    large_board_length = 96
    blade_width = 0.125
    small_boards.sort(reverse=True)
    board_cuts = []
    current_board_index = 0
    remaining_length = large_board_length
    remaining_lengths = []
    added = False
    for board_length, quantity in small_boards:
        for i in range(quantity):
            if remaining_length >= board_length+blade_width:
                if current_board_index == len(board_cuts):
                    board_cuts.append((current_board_index + 1, [board_length]))
                else:
                    board_cuts[current_board_index][1].append(board_length)
                remaining_length -= board_length
                remaining_length -= blade_width
            else:
                if len(remaining_lengths) < len(board_cuts): # or else it adds the remaining length multiple times
                    remaining_lengths.append(remaining_length+blade_width)
                # check if within remaining lengths if there is enough space to make another cut
                for board, old_space in enumerate(remaining_lengths):
                    if board_length+blade_width <= old_space:
                        board_cuts[board][1].append(board_length)
                        # make updates to remaining_lengths, board_cuts, board_length
                        remaining_lengths[board] = old_space - blade_width - board_length
                        # update board_length, quantity, go to next loop of small_boards
                        added = True
                        # no change to current_board_index, remaining_length 
                            # since we did not do anything with current board
                        break
                if not added:
                    current_board_index += 1
                    if current_board_index == len(board_cuts):
                        board_cuts.append((current_board_index + 1, [board_length]))
                    else:
                        board_cuts[current_board_index][1].append(board_length)
                    remaining_length = large_board_length - blade_width - board_length
                added = False
    remaining_lengths.append(remaining_length+blade_width)
    #print("Remaining lengths (waste) of each large board:")
    #print(remaining_lengths)
    return board_cuts

def check_board_length(board):
    print("The amount of board used: ", sum(board)+(len(board)-1)*0.125)

def main():
    while True:
        tuple_list = []
        num_tuples = int(input("Enter the number of different board lengths: "))
        for i in range(num_tuples):
            first_element = input("\nEnter the board length of board {}: ".format(i + 1))
            second_element = input("Enter the amount of board {}: ".format(i + 1))
            try:
                first_element = float(first_element)
                second_element = int(second_element)
            except ValueError:
                print("Invalid input. Both elements of the tuple must be numbers.")
                break
            tuple_list.append((first_element, second_element))

        validate_message = print("\nIs this your list of board sizes and amounts? ", tuple_list)
        validate_input = input("Type 'y' to confirm or 'n' to restart: ")
        
        if "y" in str.lower(validate_input):
            result = custom_order(tuple_list)
            print("\nAMOUNT OF BOARDS TO ORDER:", len(result))
            print("Small boards cut out of each 96\" board:")
            for large_board_index, boards_cuts in result:
                print(f"Large board {large_board_index}: {boards_cuts}")
                check_board_length(boards_cuts)
            break

if __name__=="__main__":
    main()
