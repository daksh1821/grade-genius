import cv2
from logger import logger
import numpy as np
# def auto_crop_table(image_path: str, output_path: str = 'cropped_table.png') -> str:
#     """
#     Automatically detects and crops the main table structure in the image.

#     Args:
#         image_path (str): Path to the input image.
#         output_path (str): Path to save the cropped image.

#     Returns:
#         str: Path to the saved cropped image.
#     """
#     img = cv2.imread(image_path)
#     if img is None:
#         logger.error("User with id $ user-id uploaded none image")
#         raise ValueError("Failed to load image. Check the file path.")
#     # RGB to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # Apply binary thresholding
#     # This converts the image to black and white, enhancing contrast between text/lines and background
#     # cv2.THRESH_BINARY_INV makes text white on black background
#     _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
#     # Perform morphological operations to close small gaps or holes in the image
#     # MORPH_CLOSE helps connect broken parts of lines or characters
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
#     morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#     # Find all external contours in the morph image
#     contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     # Find the largest contour assuming it's the table
#     largest_contour = max(contours, key=cv2.contourArea)

#     # Get bounding box coordinates of the largest contour
#     x, y, w, h = cv2.boundingRect(largest_contour)

#     # Crop the original image using bounding box
#     cropped = img[y:y+h, x:x+w]

#     # Save the cropped image to disk
#     cv2.imwrite(output_path, cropped)

#     return output_path

def auto_crop_table(img) -> np.ndarray:
    """
    Automatically detects and crops the main table structure from an image array.

    Args:
        img: NumPy array representing the image.

    Returns:
        Cropped image as a NumPy array.
    """
    if img is None:
        logger.error("Received None as image input to crop.")
        raise ValueError("Invalid image input.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        logger.error("No contours found for cropping.")
        raise ValueError("Could not find any contours.")

    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped = img[y:y+h, x:x+w]

    logger.info("Cropping completed successfully.")
    return cropped
