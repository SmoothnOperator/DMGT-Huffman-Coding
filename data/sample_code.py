import sys
import os
import math

class DataProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def load_data(self):
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"File {self.filename} not found.")
        with open(self.filename, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith('#'):
                    self.data.append(stripped)
        return len(self.data)

    def compute_statistics(self):
        if not self.data:
            return {"count": 0, "mean": 0.0, "variance": 0.0}
        lengths = [len(item) for item in self.data]
        total = sum(lengths)
        mean_val = total / len(lengths)
        variance = sum((x - mean_val) ** 2 for x in lengths) / len(lengths)
        return {
            "count": len(lengths),
            "mean": round(mean_val, 4),
            "std_dev": round(math.sqrt(variance), 4)
        }

    def export_summary(self, output_path):
        stats = self.compute_statistics()
        with open(output_path, 'w', encoding='utf-8') as out:
            for key, val in stats.items():
                out.write(f"{key}: {val}\n")
        print("Summary successfully exported.")

if __name__ == '__main__':
    processor = DataProcessor("input.txt")
    print("Data processing pipeline ready.")
