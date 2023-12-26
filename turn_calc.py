import cv2
import numpy as np
result = cv2.imread('result1.jpg')
height, width, _ = result.shape
left_half = result[:, :-40 +width // 2]
right_half = result[:,40+ width // 2:]


left_sum = np.sum(left_half)
right_sum = np.sum(right_half)
print(right_sum)
print(left_sum)