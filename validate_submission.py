#!/usr/bin/env python3
"""
validate_submission.py — India Runs Hackathon: Track 01 Submission Validation
Usage: python validate_submission.py your_team_id.csv
"""

import csv
import re
import sys
from pathlib import Path

def validate_csv(csv_path: Path):
    print(f"==================================================")
    print(f"[VALIDATING] Track 01 Submission: {csv_path.name}")
    print(f"==================================================")

    if not csv_path.exists():
        print(f"[ERROR] File does not exist: {csv_path}")
        return False

    required_headers = ["candidate_id", "rank", "score", "reasoning"]
    
    errors = []
    warnings = []

    try:
        with open(csv_path, "r", encoding="utf-8", newline="") as f:
            # Check for empty file
            first_char = f.read(1)
            if not first_char:
                print("[ERROR] File is empty.")
                return False
            f.seek(0)

            reader = csv.DictReader(f)
            
            # Check CSV headers exactly
            if not reader.fieldnames:
                print("[ERROR] No headers found.")
                return False
                
            headers_cleaned = [h.strip() for h in reader.fieldnames]
            if len(headers_cleaned) != len(required_headers) or any(h1 != h2 for h1, h2 in zip(headers_cleaned, required_headers)):
                errors.append(f"Header mismatch. Expected {required_headers}, found {reader.fieldnames}")

            candidate_set = set()
            previous_rank = 0
            row_count = 0
            
            for line_no, row in enumerate(reader, start=2):
                row_count += 1
                
                # Check column count
                if len(row) != len(required_headers):
                    errors.append(f"Row {line_no}: Incorrect column count (expected 4, found {len(row)})")
                    continue
                
                cid = row.get("candidate_id")
                rank_str = row.get("rank")
                score_str = row.get("score")
                reasoning = row.get("reasoning")
                
                # 1. Validate Candidate ID
                if not cid:
                    errors.append(f"Row {line_no}: candidate_id is missing or empty.")
                else:
                    cid = cid.strip()
                    if not re.match(r"^CAND_\d+$", cid):
                        errors.append(f"Row {line_no}: Invalid candidate_id pattern '{cid}' (expected 'CAND_' followed by digits)")
                    
                    if cid in candidate_set:
                        errors.append(f"Row {line_no}: Duplicate candidate_id found: '{cid}'")
                    candidate_set.add(cid)
                
                # 2. Validate Rank
                if not rank_str:
                    errors.append(f"Row {line_no}: rank is missing or empty.")
                else:
                    try:
                        rank_val = int(rank_str.strip())
                        if rank_val <= 0:
                            errors.append(f"Row {line_no}: Rank must be a positive integer, found '{rank_str}'")
                        elif rank_val != previous_rank + 1:
                            errors.append(f"Row {line_no}: Discontinuous rank sequence. Expected {previous_rank + 1}, found {rank_val}")
                        previous_rank = rank_val
                    except ValueError:
                        errors.append(f"Row {line_no}: Rank is not a valid integer: '{rank_str}'")

                # 3. Validate Score
                if not score_str:
                    errors.append(f"Row {line_no}: score is missing.")
                else:
                    try:
                        score_val = float(score_str.strip())
                        if not (0.0 <= score_val <= 1.0):
                            errors.append(f"Row {line_no}: Score '{score_val}' is out of valid bounds [0.0, 1.0]")
                        
                        # Check rounding (four decimal places)
                        decimal_part = score_str.split('.')[-1] if '.' in score_str else ''
                        if len(decimal_part) > 4:
                            warnings.append(f"Row {line_no}: Score '{score_str}' has more than 4 decimal places. It will be rounded down during evaluation.")
                    except ValueError:
                        errors.append(f"Row {line_no}: Score is not a valid float: '{score_str}'")

                # 4. Validate Reasoning
                if not reasoning:
                    errors.append(f"Row {line_no}: Reasoning explanation is missing.")
                else:
                    reasoning_strip = reasoning.strip()
                    if len(reasoning_strip) < 15:
                        warnings.append(f"Row {line_no}: Reasoning explanation is abnormally brief ({len(reasoning_strip)} characters)")
                    if ";" not in reasoning_strip:
                        warnings.append(f"Row {line_no}: Reasoning lacks standard semicolons parsing format (recommend candidate title + exp + skills).")

            # Check row count
            if row_count == 0:
                errors.append("CSV has zero validation data rows.")
            elif row_count != 100:
                warnings.append(f"Total entries: {row_count}. The competition evaluation standard recommends exactly 100 candidate recommendations.")

    except Exception as e:
        print(f"[FATAL ERROR] during read: {e}")
        return False

    # Output report
    if errors:
        print(f"\n[FAILED] Found {len(errors)} errors and {len(warnings)} warnings.")
        for err in errors[:10]:
            print(f" - [ERROR] {err}")
        if len(errors) > 10:
            print(f" ... and {len(errors) - 10} more errors.")
        return False
    else:
        print(f"\n[SUCCESS] File '{csv_path.name}' is highly compliant with Track 01 rules!")
        if warnings:
            print(f"[WARNINGS] ({len(warnings)}):")
            for warn in warnings[:5]:
                print(f" - [WARNING] {warn}")
            if len(warnings) > 5:
                print(f" ... and {len(warnings) - 5} more warnings.")
        else:
            print("No warnings found. Pristine submission format.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_submission.py <submission_csv_path>")
        sys.exit(1)
        
    csv_input = Path(sys.argv[1])
    success = validate_csv(csv_input)
    sys.exit(0 if success else 1)
