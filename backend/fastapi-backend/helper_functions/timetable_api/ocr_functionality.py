from paddleocr import PaddleOCR
import json
import re
# import difflib
import tempfile
import cv2
import os
from utils.logger import logger
# def is_monday_variant(text):
#     '''
#     This function checks whether there is around 
#     75% match with Monday (that's) our starting point
#     '''
#     text = text.strip().lower()
#     candidates = ["mon", "monday"]
    
#     best_match = difflib.get_close_matches(text, candidates, n=1, cutoff=0.75)
    
#     return len(best_match) > 0
def is_monday_variant_regex(text: str) -> bool:
    '''
    ^ and $ ensure it matches the full word.
    mon is required.
    (day)? makes the "day" part optional.
    re.IGNORECASE allows any casing: lowercase, uppercase, or mixed.
    '''
    pattern = r'^(mon(day)?)$'
    return bool(re.match(pattern, text.strip(), re.IGNORECASE))
def process_cropped_image(img)->dict:
    ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)

    # Write image temporarily to memory for OCR
    with tempfile.NamedTemporaryFile(suffix=".png",delete=False) as tmp:
        tmp_path = tmp.name
        cv2.imwrite(tmp.name, img)
    try:
        results = ocr.ocr(tmp.name, cls=True)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    logger.info("OCR processing completed.")

    text_entries = []
    text_like_monday_found = False
    for entry in results[0]:
        # top left, top right, bottom right, bottom left format
        bbox, (text, prob) = entry
        if not text_like_monday_found:
            current_text_matched_with_monday = is_monday_variant_regex(text)
            if current_text_matched_with_monday:
                text_like_monday_found = True
            else:
                continue
        x_coords = [point[0] for point in bbox]
        y_coords = [point[1] for point in bbox]
        startX = int(min(x_coords))
        endX = int(max(x_coords))
        startY = int(min(y_coords))
        endY = int(max(y_coords))
        text_entries.append((startX, endX, startY, endY, text))
    rows=[]
    for entry in text_entries:
        startX, endX, startY, endY, text = entry
        placed = False
        for row in rows:
            _, _, ref_startY, ref_endY, _ = row[0]
            if (ref_startY - 20) <= startY <= (ref_endY + 20):
                row.append(entry)
                placed = True
                break
        if not placed:
            rows.append([entry])
    rows.sort(key=lambda row: min(e[2] for e in row))  # sort top to bottom
    for row in rows:
        row.sort(key=lambda x: x[0])  # sort left to right

    # Assume fixed days (make this dynamic if needed)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_headers = rows[0][:]
    

    day_x_ranges = {}
    for day, (startX, endX, _, _, text) in zip(days, day_headers):
        day_x_ranges[day] = (startX, endX)

    timetable_json = {}
    for row in rows[1:]:
        time_slot = row[0][4]  # assuming first element is the time
        timetable_json[time_slot] = {day: "" for day in days}
        for entry in row[1:]:
            startX, endX, _, _, text = entry
            x_center = (startX + endX) // 2
            for day, (day_startX, day_endX) in day_x_ranges.items():
                if day_startX - 10 <= x_center <= day_endX + 10:
                    timetable_json[time_slot][day] = text
                    break

    # print(json.dumps(timetable_json, indent=4))
    with open("timetable.json", "w") as f:
        json.dump(timetable_json, f, indent=4)

    return timetable_json