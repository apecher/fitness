import csv, sys
import argparse, os  # added

# replaced: from fitparse import FitFile
try:
    from fitparse import FitFile
except ImportError:
    print("Missing dependency 'fitparse'. Install it with: python3 -m pip install fitparse")
    sys.exit(1)

def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Convert a FIT file or a directory of FIT files to CSV.")
    p.add_argument("input", help="Path to input .fit file or directory")
    p.add_argument("output", nargs="?", help="Output CSV path (default: input.csv). For directory input, this must be a directory.")
    # If no CLI args, show help and prompt interactively for convenience
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        p.print_help()
        print("\nExamples:")
        print("  python3 fit2csv.py activity.fit")
        print("  python3 fit2csv.py activity.fit output.csv")
        print("  python3 fit2csv.py /path/to/folder/with/fits")
        print("  python3 fit2csv.py /path/to/folder/with/fits /path/to/output_folder\n")
        try:
            user_input = input("Enter path to .fit file or directory (or press Enter to exit): ").strip()
        except EOFError:
            user_input = ""
        if not user_input:
            sys.exit(2)
        argv = [user_input]
    return p.parse_args(argv)

def convert_fit_to_csv(in_path: str, out_path: str) -> bool:
    """Convert a single FIT file to CSV. Returns True on success, False on failure."""
    rows = []
    try:
        ff = FitFile(in_path)
    except Exception as e:
        print(f"Failed to read FIT file '{in_path}': {e}")
        return False
    for m in ff.get_messages("record"):
        row = {}
        for d in m:
            row[d.name] = d.value
        rows.append(row)
    if rows:
        try:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=sorted({k for r in rows for k in r}))
                w.writeheader()
                w.writerows(rows)
            print(f"Wrote {len(rows)} records to {out_path}")
            return True
        except Exception as e:
            print(f"Failed to write CSV '{out_path}': {e}")
            return False
    else:
        try:
            open(out_path, "w").close()
            print(f"No 'record' messages found. Created empty file: {out_path}")
            return True
        except Exception as e:
            print(f"Failed to create empty CSV '{out_path}': {e}")
            return False

def main():
    args = parse_args()
    in_path = args.input
    out_arg = args.output

    # Directory input: batch convert all .fit files in the directory (non-recursive).
    if os.path.isdir(in_path):
        fits = [os.path.join(in_path, f) for f in os.listdir(in_path) if f.lower().endswith(".fit")]
        if not fits:
            print(f"No .fit files found in directory: {in_path}")
            sys.exit(1)
        # If output provided, it must be a directory.
        if out_arg and not os.path.isdir(out_arg):
            print("When input is a directory, the 'output' argument must be a directory.")
            sys.exit(2)
        out_dir = out_arg or in_path
        successes = 0
        for fpath in sorted(fits):
            fname = os.path.splitext(os.path.basename(fpath))[0] + ".csv"
            out_path = os.path.join(out_dir, fname)
            if convert_fit_to_csv(fpath, out_path):
                successes += 1
        print(f"Converted {successes}/{len(fits)} files into: {out_dir}")
        sys.exit(0 if successes == len(fits) else 1)

    # File input: validate then convert.
    if not os.path.exists(in_path):
        print(f"Input path does not exist: {in_path}")
        sys.exit(1)
    if os.path.isdir(in_path):
        # Shouldn't reach here, but guard anyway.
        print(f"Input is a directory, expected a .fit file: {in_path}")
        sys.exit(2)
    # Default output for single file if not provided.
    out_path = out_arg or os.path.splitext(in_path)[0] + ".csv"
    ok = convert_fit_to_csv(in_path, out_path)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
