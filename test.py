
# array = [1, 2, 3, 4, 5]
# for i in range(len(array)):
#     if array[i] in [2, 4]:
#         array.pop(i)
#         i -= 1
#     print(array)

array = [1, 2, 3, 4, 5]
i = 0
while i < len(array):
    if array[i] in [2, 4]:
        array.pop(i)
        # We do NOT increment i here, because the next item 
        # has shifted into the current spot.
    else:
        # Only move to the next index if we didn't remove anything
        i += 1
    print(array)
    