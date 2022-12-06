from functions import *

# get_input_and_solve(True)

board = get_board_from_user()
print_board(board)
elapsed, solution = solve1(board)
print(f"\n\nsolved after: {elapsed}\n")
print_board(solution)

# random_board = generate_random_board(15)
# defined_size = 30
# sample_size = 100
# result = [[None for y in range(sample_size)] for x in range(defined_size)]
# for defined in range(defined_size, -1, -1):
#     for sample in range(sample_size):
#         print("defined: ", defined, "\t", "sample: ", sample)
#         random_board = generate_random_board(defined)
#         try:
#             elapsed_f, board_f = solve1(random_board)
#             elapsed_b, board_b = solve2(random_board)
#             result[defined][sample] = check_for_differences(board_f, board_b)
#         except:
#             print("unsolvable")
#             continue
# with open("results.txt", "w") as file:
#     for row in result:
#         print(row)
#         file.write(",".join([print_result(item) for item in row]))
#         file.write("\n")
#     file.close()

# defined_size = 30
# sample_size = 100
# result = [[0 for y in range(sample_size)] for x in range(defined_size)]
# for defined in range(defined_size):
#     for sample in range(sample_size):
#         print("defined: ", defined, "\t", "sample: ", sample)
#         random_board = generate_valid_random_board(defined)
#         print_board(random_board)
#         try:
#             elapsed_f, board_f = solve1(random_board)
#             elapsed_b, board_b = solve2(random_board)
#             result[defined][sample] = check_for_differences(board_f, board_b)
#         except:
#             print("unsolvable")
#             continue
#
# with open("results_2.txt", "w") as file:
#     for row in result:
#         print(row)
#         file.write(",".join(row))
#     file.close()
